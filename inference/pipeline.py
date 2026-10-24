import os
import json
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Dict

load_dotenv()
llm = ChatGroq(model="openai/gpt-oss-20b")

class InferenceState(TypedDict):
    transactions: str
    active_context: str
    muted_facts: List[str]
    proposed_facts: List[Dict[str, str]]
    safe_facts: List[Dict[str, str]]
    blocked_facts: List[Dict[str, str]]

def inference_engine_node(state: InferenceState):
    """Agent 1: Extracts facts and assigns risk, strictly following Nordea guidelines."""
    prompt = f"""You are the Nordea Core Banking Inference Engine. Your job is to analyze raw transaction streams to identify life events, financial habits, and milestones to help Nordea serve the customer better.
    
    ACTIVE CONTEXT (Customer Goals & Profile): 
    {state['active_context']}
    
    SUPPRESSION LIST (NEVER propose these facts, the customer already rejected them): 
    {state['muted_facts']}
    
    INSTRUCTIONS:
    1. Extract inferred facts from the transactions.
    2. Rank each fact's risk level as 'HIGH' or 'LOW':
       - HIGH risk: Assumptions about lifestyle (e.g., eating out a lot), life events (e.g., moving, having a baby, getting a new job), or facts heavily tied to their active goals.
       - LOW risk: Basic, mathematically obvious financial observations (e.g., salary amounts, rent amounts, subscription costs).
    
    Transactions: {state['transactions']}
    
    Output ONLY a raw JSON list of objects: [{{"fact": "...", "risk": "HIGH"}}]
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content
    raw_text = content[0].get("text", "").strip() if isinstance(content, list) else str(content).strip()
    
    if "```json" in raw_text:
        raw_text = raw_text.split("```json")[1].split("```")[0].strip()
    elif "```" in raw_text:
        raw_text = raw_text.split("```")[1].split("```")[0].strip()
        
    try:
        facts = json.loads(raw_text)
        facts = [f for f in facts if f.get("fact") not in state["muted_facts"]]
    except:
        facts = []
        
    return {"proposed_facts": facts}

def safety_gate_node(state: InferenceState):
    """Agent 2: AI Ethics Board Safety Gate with explicit Nordea banking rules."""
    if not state["proposed_facts"]:
        return {"safe_facts": [], "blocked_facts": []}

    facts_to_review = [item["fact"] for item in state["proposed_facts"]]
    
    prompt = f"""You are the Nordea AI Ethics Safety Gate. Your job is to filter out legally protected or highly sensitive data from entering the bank's context cabinet.
    
    Customer's ACTIVE CONTEXT:
    {state['active_context']}
    
    RULES FOR CLASSIFICATION:
    - SAFE: Income, salary, rent, mortgage, utilities, retail shopping, groceries, dining, travel, and standard banking transactions. (This is a bank, financial data is ALWAYS SAFE).
    - BLOCKED: Medical/health conditions, oncology, clinics, pharmacies, religious affiliations, political donations, trade union membership, sexual orientation, or racial/ethnic inferences.
    
    Facts to evaluate: {json.dumps(facts_to_review)}
    
    Reply ONLY with raw JSON mapping fact strings to an object containing 'status' ('SAFE' or 'BLOCKED') and 'reason' (a short explanation if blocked, otherwise empty string).
    Example:
    {{
        "Visited Helsinki Oncology Center": {{"status": "BLOCKED", "reason": "Medical data is strictly prohibited by AI ethics guidelines."}},
        "Received a salary of 4500": {{"status": "SAFE", "reason": ""}}
    }}
    """
    
    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content
    raw_text = content[0].get("text", "").strip() if isinstance(content, list) else str(content).strip()
    
    if "```json" in raw_text:
        raw_text = raw_text.split("```json")[1].split("```")[0].strip()
    elif "```" in raw_text:
        raw_text = raw_text.split("```")[1].split("```")[0].strip()
        
    safe = []
    blocked = []
    
    try:
        evaluations = json.loads(raw_text)
        for item in state["proposed_facts"]:
            fact_str = item["fact"]
            eval_data = evaluations.get(fact_str, {"status": "SAFE", "reason": ""})
            status = eval_data.get("status", "SAFE").upper()
            
            if status == "BLOCKED":
                blocked.append({"fact": fact_str, "reason": eval_data.get("reason", "Flagged by internal safety guidelines.")})
            else:
                safe.append(item)
    except:
        safe = state["proposed_facts"]
            
    return {"safe_facts": safe, "blocked_facts": blocked}

workflow = StateGraph(InferenceState)
workflow.add_node("inference", inference_engine_node)
workflow.add_node("safety", safety_gate_node)
workflow.add_edge(START, "inference")
workflow.add_edge("inference", "safety")
workflow.add_edge("safety", END)

inference_pipeline = workflow.compile()