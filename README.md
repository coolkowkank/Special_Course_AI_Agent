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
