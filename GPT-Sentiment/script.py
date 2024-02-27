import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Set up environment
load_dotenv()
GPT_KEY = os.getenv('GPT_KEY')
llm = ChatOpenAI(openai_api_key=GPT_KEY)

# Initialize variables

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional financial analyst."),
    ("user", "{input}")
])
output_parser = StrOutputParser()

# Chain call

chain = prompt | llm | output_parser
output = chain.invoke({"input": "Will Nvidia's stock going to increase next month?"})

print(output)
