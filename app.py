import streamlit as st
import os
from rag_pipeline import ask, retrieve_chunks, generate_answer
from safety_layer import check_query

# Page config
st.set_page_config(
    page_title="Medical Report Q&A",
    page_icon="⚕️",
    layout="centered"
)

# Header
st.title("⚕️ Medical Report Q&A")
st.markdown("Ask questions about your medical test results in plain English.")
st.warning("⚠️ This tool is for educational purposes only. Always consult your doctor for medical advice.")

# Sidebar
with st.sidebar:
    st.header("📋 About")
    st.markdown("""
    This tool helps you understand:
    - Blood test results (CBC, Glucose, Ferritin)
    - Urine test results
    - Hormone tests (Thyroid)
    
    **What it won't do:**
    - Diagnose conditions
    - Recommend medicines
    - Replace your doctor
    """)
    st.markdown("---")
    st.markdown("**Knowledge base:**")
    st.markdown("- MedlinePlus / NIH references")
    st.markdown("- 5 medical documents")
    st.markdown("- 18 indexed chunks")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about your medical results..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Searching medical references..."):
            # Safety check
            is_safe, message = check_query(prompt)
            
            if not is_safe:
                response = f"🚫 {message}"
            else:
                # Retrieve chunks
                retrieved = retrieve_chunks(prompt)
                
                # Show sources
                with st.expander("📚 Sources used"):
                    for i, chunk in enumerate(retrieved):
                        st.markdown(f"**{i+1}. {chunk['source']}** (category: {chunk['category']})")
                        st.text(chunk['text'][:200] + "...")
                
                # Generate answer
                response = generate_answer(prompt, retrieved)
            
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})