import streamlit as st
from cabinet.storage import ContextCabinet
from inference.pipeline import inference_pipeline
from agent.banking_agent import get_agent_response
from data.mock_transactions import fetch_user_transactions

st.set_page_config(layout="wide", page_title="Nordea Context Cabinet")

# Initialize Cabinet in Session State
if "cabinet" not in st.session_state:
    st.session_state.cabinet = ContextCabinet()

cabinet = st.session_state.cabinet

# --- SIDEBAR: BACKEND SIMULATION & APPROVAL UI ---
with st.sidebar:
    st.header("⚙️ Bank Inference (Side B)")
    
    if st.button("Run Transaction Inference API"):
        with st.spinner("Multi-Agent Pipeline Running..."):
            transactions = fetch_user_transactions()
            result = inference_pipeline.invoke({"transactions": str(transactions)})
            
            # Add safe facts to pending
            for fact in result.get("safe_facts", []):
                cabinet.add_item("BANK_INFERENCE", fact, status="PENDING")
            # Log blocked facts silently
            for fact in result.get("blocked_facts", []):
                cabinet.add_item("SAFETY_GATE", fact, status="BLOCKED")
        st.success("Inference complete!")

    st.divider()
    
    st.header("🛡️ Customer Approval UI")
    pending_items = cabinet.get_items_by_status("PENDING")
    
    if not pending_items:
        st.write("No pending inferences.")
    else:
        for item in pending_items:
            st.info(f"**Suggested:** {item['content']}")
            col1, col2 = st.columns(2)
            if col1.button("Approve", key=f"app_{item['id']}"):
                cabinet.update_status(item["id"], "ACTIVE")
                st.rerun()
            if col2.button("Reject", key=f"rej_{item['id']}"):
                cabinet.update_status(item["id"], "ARCHIVED")
                st.rerun()

    st.divider()
    st.header("🔒 Audit Log (Blocked by AI)")
    for item in cabinet.get_items_by_status("BLOCKED"):
        st.error(f"Blocked Sensitive Data: {item['content']}")

# --- MAIN CHAT INTERFACE ---
st.title("Nordea Banking Agent")

# Show active context directly above chat for demo transparency
st.subheader("Your Active Context Cabinet")
st.text(cabinet.get_active_context_string())

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask: 'Am I on track to buy a flat?'"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Analyzing context..."):
            active_context = cabinet.get_active_context_string()
            response = get_agent_response(prompt, active_context)
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})