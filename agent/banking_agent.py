from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

llm = ChatGroq(model="openai/gpt-oss-20b")

def get_agent_response(customer_query: str, active_context: str) -> str:
    """Injects the context cabinet and invokes the conversational agent."""
    
    system_prompt = f"""You are a professional, empathetic Nordea Financial Advisor AI. 
    You are assisting a customer (e.g., Lauri) with their financial goals.
    
    CRITICAL RULES:
    1. Base your advice STRICTLY on the facts in the [ACTIVE CONTEXT CABINET].
    2. Never reference or assume any information that is not in the active context.
    3. If the context shows they have a specific goal (e.g., buying a flat, saving for a car), prioritize answering how their current financial status impacts that goal.
    4. Keep your tone helpful, transparent, and concise. Do not use robotic jargon.
    
    [ACTIVE CONTEXT CABINET]
    {active_context}
    """
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=customer_query)
    ]
    
    return llm.invoke(messages).content