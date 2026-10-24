# Nordea Context Cabinet: Multi-Agent AI Banking Prototype

This repository contains the prototype for the **Nordea Context Cabinet (Lauri Scenario)**, developed for the AI Agents Hackathon. The system demonstrates a privacy-first, multi-agent architecture that intelligently extracts, filters, and utilizes customer context from raw transaction data to provide highly personalized financial advice.

## Ecosystem Overview

The ecosystem is built to balance proactive AI assistance with strict data privacy and customer autonomy. It features a multi-agent backend powered by **LangGraph** and high-speed **Groq** inference (`openai/gpt-oss-20b`), consisting of the following core components:

*   **Inference Engine (Agent 1):** Analyzes uncategorized raw transaction streams to infer life events, financial habits, and milestones. It dynamically assigns risk tiers (`HIGH` for lifestyle assumptions/goals, `LOW` for basic mathematical facts).
*   **Safety Gate (Agent 2):** An AI Ethics board that strictly filters extracted facts against Nordea's privacy guidelines. It automatically blocks legally protected or sensitive data (medical, religious, political) from ever entering the bank's context memory, logging specific rejection reasons.
*   **Context Cabinet:** A persistent JSON-based storage system (`cabinet_db.json`) that manages the lifecycle of all customer facts (`PENDING`, `ACTIVE`, `BLOCKED`, `MUTED`).
*   **Trust Layer & Suppression List:** A customer-controlled governance layer. If a customer rejects an AI-proposed assumption, it is permanently `MUTED` and the Inference Engine will never propose it again.
*   **Attention Budget Orchestrator:** A UI routing mechanism that prevents notification fatigue by limiting the customer review queue to a maximum of 3 high-risk items per session.
*   **Banking Agent (Customer-Facing):** An advisory AI that strictly relies on `ACTIVE` context to answer customer questions (e.g., "Am I on track to buy a flat?"), ensuring advice is grounded in verified, approved facts.

## Project Structure

```text
├── agent/
│   └── banking_agent.py      # Customer-facing conversational AI using Active Context
├── cabinet/
│   ├── storage.py            # Context Cabinet DB logic, state management, and Mute List
│   └── cabinet_db.json       # Auto-generated persistent database
├── data/
│   └── mock_transactions.py  # 6-month transaction dataset (includes baseline, high-risk, and blocked events)
├── inference/
│   └── pipeline.py           # LangGraph multi-agent flow (Inference -> Safety Gate)
├── test_backend.py           # Main execution script simulating the full ecosystem lifecycle
└── README.md

## Prototype Scope vs. Full Enterprise Architecture

This repository represents a functional, scaled-down prototype of the Banking Context Cabinet. It is designed to demonstrate the core multi-agent loop shown in the simplified overview, **cabinet-simple-for-team.pdf**[cite: 2]:
* **Step 1 & 5:** Customer goals become instantly ACTIVE, and the AI Banking Agent reads only approved items to provide personal answers[cite: 2].
* **Step 2:** The Inference Engine extracts guesses from transactions, which are filtered by the Safety Gate and stored as PENDING[cite: 2].
* **Step 3:** The Trust Layer allows the customer to approve, edit, or reject (mute) these pending items[cite: 2].

However, the ultimate vision for this ecosystem is a much larger enterprise architecture, as detailed in the comprehensive flow diagram, **v3-clear-flow_2.pdf**[cite: 3]. While the current prototype implements foundational AI inference and smart routing, the full-scale design includes advanced components that are out-of-scope for this hackathon:
* **Enterprise Governance:** An append-only audit ledger with payload encryption, a separate key management service, and a deletion orchestrator for crypto-shredding[cite: 3].
* **Advanced Maintenance:** A fully realized Staleness and Contradiction Engine that continuously calculates freshness scores and generates decay prompts (e.g., "is this still true?")[cite: 3].
* **Serving Layer:** A Deterministic Offer Policy Engine that applies hard rules (e.g., debt ratio limits) before allowing the AI to route users to a standard offer screen outside the chat[cite: 3].
* **Expanded Inputs:** Conversational extraction to turn voice and chat into proposed items, and household entity management requiring dual approvals and legal review[cite: 3].
