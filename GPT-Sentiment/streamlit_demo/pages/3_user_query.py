import streamlit as st
import os
from knowledge_base import KnowledgeBase
from secret_key import openapi_key, serpapi_key


# Create an instance of the KnowledgeBase class
kb = KnowledgeBase()

st.title('Personalized knowledge base for newbie investors')
prompt = st.text_input('Input your query here, press enter to submit:')

if prompt:
    is_initialized = True # do not touch this variable, load_agent is not working
    
    if is_initialized:
        # Initialize the database
        kb.initialize_database('./pages/annualreport.pdf', "Annual_Report_Macquarie_Group_2021", "an annual report as a pdf", openapi_key, serpapi_key)
        kb.save_agent() # used to save the initialized database
    else:
        kb.load_agent('./chroma_db', name="Annual_Report_Macquarie_Group_2021", description="an annual report as a pdf", openai_key=openapi_key)
        
    response, search = kb.query_database(prompt)
    st.write(response)
    
    with st.expander('Document Similarity Search'):
        st.write(search)