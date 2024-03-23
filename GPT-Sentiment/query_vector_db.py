# OpenAI Agent
import os
from secret_key import openapi_key 
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.callbacks import get_openai_callback

# Prompt engineering
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Import PDF document loaders and vector store
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma

# Import vector store agent 
from langchain.agents.agent_toolkits import (
    create_vectorstore_agent,
    VectorStoreToolkit,
    VectorStoreInfo
)

'''input variables for the vector store and document'''
article_path = 'annualreport.pdf'
vector_store_name = "Annual Report Macquarie Group 2021"
vector_store_description = "a annual report as a pdf"
''''''

os.environ['OPENAI_API_KEY'] = openapi_key

# Create instance of OpenAI LLM
llm = OpenAI(temperature=0.1, verbose=True, model="gpt-3.5-turbo-instruct")
embeddings = OpenAIEmbeddings()

# Create and load PDF Loader
loader = PyPDFLoader(article_path)
pages = loader.load_and_split() # Split pages from pdf 
# Load documents into vector database aka ChromaDB
store = Chroma.from_documents(pages, embeddings, collection_name='annualreport.pdf')

# Create vectorstore info object - metadata repo?
vectorstore_info = VectorStoreInfo(
    name=vector_store_name ,
    description= vector_store_description,
    vectorstore=store
)
# Convert the document store into a langchain toolkit
toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)

# Add the toolkit to an end-to-end LC
agent_executor = create_vectorstore_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)


# example usage: each running below costs token
def main():
    with get_openai_callback() as cb:
        prompt = "tell me about the future prospects of Macquarie Group"
        response = agent_executor.run(prompt)
        print("response:\n", response)
        search = store.similarity_search_with_score(prompt)
        # print("search:\n", search)
        print("page content:\n", search[0][0].page_content)

        prompt = "where is Germany located at?"
        response = agent_executor.run(prompt)
        print("response:\n", response)
        search = store.similarity_search_with_score(prompt)
        # print("search:\n", search)
        print("page content:\n", search[0][0].page_content)
        
        # trace token usage
        print(cb)

if __name__ == "__main__":
    main()