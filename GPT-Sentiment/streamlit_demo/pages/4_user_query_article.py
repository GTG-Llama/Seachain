import streamlit as st
import os
from knowledge_base import KnowledgeBase
from secret_key import openapi_key, serpapi_key


# Create an instance of the KnowledgeBase class
kb = KnowledgeBase()

st.title('Personalized knowledge base for newbie investors')
query = st.text_input('Input you query here:')
title = st.text_input('Input the title of the article here:')
article = st.text_area('Input the article here:')

all_entered = query and title and article

if all_entered:
    is_initialized = True # do not touch this variable, load_agent is not working
    
    if is_initialized:
        # Initialize the database
        kb.initialize_database('./pages/annualreport.pdf', "Annual_Report_Macquarie_Group_2021", "an annual report as a pdf", openapi_key, serpapi_key)
        kb.save_agent() # used to save the initialized database
    else:
        kb.load_agent('./chroma_db', name="Annual_Report_Macquarie_Group_2021", description="an annual report as a pdf", openai_key=openapi_key)
        
    response = kb.query_database_with_article(query,article,title)
    st.write(response)
    