# logging
import logging

# OpenAI Agent
import os
from secret_key import openapi_key 
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings

# Prompt engineering
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.callbacks import get_openai_callback
from langchain_openai import OpenAI

# logging
logging.basicConfig(filename="logging/prompt_user_query.log",
                    level=logging.DEBUG,
                    filemode='w',
                    format='%(asctime)s %(message)s')
logger = logging.getLogger()
os.environ['OPENAI_API_KEY'] = openapi_key


# Prompt the agent with question and article
prompt_template_query_with_article = PromptTemplate(
    input_variables=['user_query', 'article'],
    template="""
        Considering the content of the following article and:\n
        {article}\n\n
        
        and the user query: {user_query},\n
        Answer the user's query general a detailed response that incorporates information form the content of the article and general financial knowledge.
    """
)


prompt_template_article_sentiment = PromptTemplate(
    input_variables=['article'],
    template="""
        Considering the content of the following article:\n
        {article}\n\n
        
        perform a sentiment analysis on the article provided, 
        do not explain, only return a numerical value where 1 for positive sentiment and 0 for negative sentiment.
    """
)

prompt_template_title_sentiment = PromptTemplate(
    input_variables=['title'],
    template="""
        Considering the content of the following article:\n
        {title}\n\n
        
        perform a sentiment analysis on the article provided, 
        do not explain, only return a numerical value where 1 for positive sentiment and 0 for negative sentiment.
    """
)
logging.info("3 Prompt templates created")

# example usage
def main():
    user_query_text = "How does this affect the economic prospects of the Singapore?"
    
    # article from Reuters, https://finance.yahoo.com/news/treasurys-yellen-says-funding-bill-060844566.html
    title = "Treasury's Yellen says funding bill allows lending of $21 bln to IMF trust"
    article = """
        By Andrea Shalal

        WASHINGTON, March 23 (Reuters) - A $1.2 trillion government funding bill passed by Congress will allow the U.S. to lend up to $21 billion to an International Monetary Fund (IMF) trust to help the world’s poorest countries, U.S. Treasury Secretary Janet Yellen said on Saturday.

        Yellen said the funding would make the United States the largest supporter of the IMF’s Poverty Reduction and Growth Trust (PRGT), which provides zero-interest rate loans to support low-income countries as they work to stabilize their economies, boost growth and improve debt sustainability.

        Congress approved the bill with a Senate vote after midnight, avoiding a government shutdown. The IMF spending will make good on a promise President Joe Biden made over two years ago with other leaders from the Group of 20 large economies to provide $100 billion to support low-income and vulnerable countries recovering from the COVID-19 pandemic and struggling with macroeconomic risks.

        The PRGT is the IMF's main vehicle for providing zero-interest loans to low-income countries to support their economic programs and help leverage additional financing from donors, development institutions, and the private sector.

        Since the beginning of the pandemic, the IMF says it has supported more than 50 low-income countries with some $30 billion in interest-free loans via the PRGT, reducing instability in poor countries from Haiti to the Democratic Republic of Congo and Nepal.

        The IMF expects demand for PRGT lending to reach nearly $40 billion this year, more than four times the historical average.

        "Today’s development marks a key milestone in the United States meeting its commitment to provide support to low-income countries that are still bearing economic scarring from the pandemic, while responding to high debt vulnerabilities, climate risks, and spillovers from Russia’s war against Ukraine," Yellen said in a statement first reported by Reuters.

        Kevin Gallagher, director of Boston University's Global Development Policy Center, said the long-delayed U.S. funding came "just in nick of time, given exorbitant interest rates in poorer countries, especially in Africa," that have hit low-income countries hard, compounding already high debt burdens.

        He noted that Congress had refused to approve Treasury's plans to loan some of the funds to the IMF's Resilience and Sustainability Trust, set up to provide funding for countries to work on climate change and other challenges.

        Yellen said the funding for the IMF reflected Washington's ongoing support for the institution and the unique role it plays in the international monetary system through its policy advice, capacity development and lending and focus on good governance, robust economic reforms and necessary adjustment.

        "I look forward to continuing our partnership with the IMF to support the needs of low-income countries,” Yellen said. (Reporting by Andrea Shalal; Editing by William Mallard)
    """

    llm = OpenAI(temperature=0.1, verbose=True, model="gpt-3.5-turbo-instruct")
    logging.info("LLM instance created")
    
    with get_openai_callback() as cb:
        # query + article => response
        chain_1 = LLMChain(llm=llm, prompt=prompt_template_query_with_article)
        response_1 = chain_1.run(user_query=user_query_text, article=article)
        logging.info("Chain 1 created and run")
        print("response_1:\n", response_1)
        print("token usage:", cb)
        print()
        
        # article => sentiment
        chain_article = LLMChain(llm=llm, prompt=prompt_template_article_sentiment)
        chain_title = LLMChain(llm=llm, prompt=prompt_template_title_sentiment)
        response_2 = chain_article.run(article=article)
        response_3 = chain_title.run(title=title)
        logging.info("Chain 2,3 created and run")
        print("response_2:\n", response_2)        
        print("token usage:", cb)
        print()
        
        print("response_3:\n", response_3)
        print("token usage:", cb)



if __name__ == "__main__":
    main()