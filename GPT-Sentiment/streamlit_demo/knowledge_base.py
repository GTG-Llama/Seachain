import os
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.agents.agent_toolkits import create_vectorstore_agent, VectorStoreToolkit, VectorStoreInfo
from langchain_community.callbacks import get_openai_callback
from langchain.agents import load_tools

class KnowledgeBase:
    def __init__(self):
        self.toolkit = None
        self.llm = None
        self.agent_executor = None
        self.embeddings = None
    
    def initialize_database(self, article_paths, vector_store_names, vector_store_descriptions, openapi_key, serpapi_key):
        # documents = []
        # for path in article_paths:
        #     loader = PyPDFLoader(path)
        #     pages = loader.load_and_split()
        #     documents.append(pages)
        
        loader = PyPDFLoader(article_paths)
        pages = loader.load_and_split()
        
        embeddings = OpenAIEmbeddings()
        store = Chroma.from_documents(pages, embeddings, collection_name=vector_store_names, persist_directory="./chroma_db")
        vectorstore_info = VectorStoreInfo(name=vector_store_names, 
                                           description=vector_store_descriptions, 
                                           vectorstore=store
                                           )
        self.toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)
        self._initialize_agent_executor(self.toolkit, openapi_key, serpapi_key)
        
    def _initialize_agent_executor(self, toolkit, openapi_key, serpapi_key):
        os.environ['SERPAPI_API_KEY'] = serpapi_key
        os.environ['OPENAI_API_KEY'] = openapi_key
        self.llm = OpenAI(temperature=0.1, verbose=True, model="gpt-3.5-turbo-instruct")
        tools = load_tools(['llm-math','serpapi'], llm=self.llm, verbose=True)
        self.agent_executor = create_vectorstore_agent(
            llm=self.llm,
            toolkit=toolkit,
            verbose=True,
            tools=tools
        )
    
    def save_agent(self):
        vector_store = self.toolkit.vectorstore_info.vectorstore
        vector_store.persist()
    
    # issue exists for loading
    def load_agent(self, path, name, description, openai_key):
        embeddings = OpenAIEmbeddings()

        self.toolkit = VectorStoreToolkit(
            vectorstore_info=VectorStoreInfo(name=name, 
                                             description=description, 
                                             vectorstore=Chroma(persist_directory=path, embedding_function=embeddings)))
        self._initialize_agent_executor(self.toolkit, openai_key)
    
    def embed_new_document(self, document_path):
        if document_path.endswith('.pdf'):
            loader = PyPDFLoader(document_path)
            pages = loader.load_and_split()
            self.toolkit.vectorstore_info.vectorstore.add_documents(pages)
        elif document_path.endswith('.txt'):
            with open(document_path, 'r') as file:
                text = file.read()
            self.toolkit.vectorstore_info.vectorstore.add_document(text)
    
    def query_database(self, query):
        with get_openai_callback() as cb:
            query = "Based on the knowledge base and google search, " + query
            response = self.agent_executor.run(query)
            vector_store = self.toolkit.vectorstore_info.vectorstore
            search = vector_store.similarity_search_with_score(query)
        return response, search[0][0].page_content
    
    def query_database_with_article(self, query, article, title):
        with get_openai_callback() as cb:
            query = "Based on the knowledge base and google search, " + query
            query = f"""
                        Considering the content of the following article with title: {title}:\n
                        {article}\n\n
                        
                        and the user query: {query},\n
                        Answer the user's query general a detailed response that incorporates information form the content of the article and general financial knowledge.
                    """
            response = self.agent_executor.run(query)
        return response
    
    def check_database_size(self):
        return len(self.toolkit.vectorstore_info.vectorstore)