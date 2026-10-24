import os
from data.mock_transactions import fetch_user_transactions
from cabinet.storage import ContextCabinet, DB_FILE
from inference.pipeline import inference_pipeline
from agent.banking_agent import get_agent_response

if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

print("--- 1. LOADING CONTEXT CABINET ---")
cabinet = ContextCabinet()
active_context = cabinet.get_active_context_string()
muted_facts = cabinet.get_muted_facts()
print(active_context)

print("\n--- 2. RUNNING CONTEXT-AWARE INFERENCE ---")
transactions = fetch_user_transactions()
print(" -> [Status] Sending transactions, context, and mute list to AI...")

final_state = None
inputs = {
    "transactions": str(transactions), 
    "active_context": active_context,
    "muted_facts": muted_facts
}

for event in inference_pipeline.stream(inputs):
    for node_name, node_state in event.items():
        print(f" -> [Status] {node_name.capitalize()} Agent finished processing.")
        final_state = node_state

for item in final_state.get("safe_facts", []):
    cabinet.add_item("BANK_INFERENCE", item["fact"], status="PENDING", risk=item["risk"])

print("\n[Safety Gate Review]")
blocked_items = final_state.get("blocked_facts", [])
for item in blocked_items:
    cabinet.add_item("SAFETY_GATE", item["fact"], status="BLOCKED", risk="HIGH", reason=item["reason"])
    print(f" - [BLOCKED] {item['fact']}")
    print(f"   ↳ Reason: {item['reason']}")
print(f"\n - System secured: {len(blocked_items)} sensitive fact(s) permanently blocked.")

print("\n--- 3. ATTENTION BUDGET & TRUST LAYER ---")
pending_items = cabinet.get_items_by_status("PENDING")

session_items = pending_items[:3]
print(f"Queue: {len(pending_items)} items pending. Routing {len(session_items)} to customer UI.\n")

for i, item in enumerate(session_items):
    if item.get("risk") == "LOW":
        cabinet.update_status(item["id"], "ACTIVE")
        print(f"[Auto-Approved] Low Risk: {item['content']}")
    elif item.get("risk") == "HIGH":
        if i == 0:
            print(f"[Customer REJECTED] Muting: '{item['content']}'")
            cabinet.update_status(item["id"], "MUTED")
        else:
            print(f"[Customer APPROVED] Activating: '{item['content']}'")
            cabinet.update_status(item["id"], "ACTIVE")

print("\n--- 4. TESTING THE CUSTOMER AGENT ---")
updated_context = cabinet.get_active_context_string()
query = "Am I on track to buy a flat?"
print(f"User: {query}\n")

response = get_agent_response(query, updated_context)
print(f"Agent: {response}")