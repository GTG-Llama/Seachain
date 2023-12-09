import requests
from bs4 import BeautifulSoup
from getpass import getpass
import os
import replicate
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
import torch



# MODIFIED SCRAPER TO GET THE TOP 10 HEADINGS
def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve search results. Status code: {response.status_code}")
        return None

def extract_headings(html):
    soup = BeautifulSoup(html, 'html.parser')
    headings = soup.find_all(['h1', 'h2', 'h3'])
    return [heading.text.strip() for heading in headings]

def extract_text_from_link(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        content_html = response.text

        soup = BeautifulSoup(content_html, 'html.parser')
        paragraphs = soup.find_all('p')
        text_content = ' '.join([p.text.strip() for p in paragraphs])

        return text_content

    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return None


def extract_headings_and_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    results = []
    for heading in headings:
        heading_text = heading.text.strip()
        link = heading.find_parent('a')
        if link:
            url = link.get('href')
            results.append({'heading': heading_text, 'url': url})

    return results

#LLAMA 2 FOR COMPARISON OF FETCHED ARTICLE DATA AND ARTICLE DATA FED IN
def get_replicate_api_token():
    # Access the value of the environment variable
    return "r8_PVATRiURP9qzFxN8anjEm4SYL8NuMjT4UCrjM"

def llama2_comparison(fed_data, fetched_data):
    api_token = get_replicate_api_token()

    if not api_token:
        print("Error: REPLICATE_API_TOKEN not set.")
        return

    replicate_client = replicate.Client(api_token)

    # Assuming you have the correct model version and input
    output = replicate_client.run(
        "meta/llama-2-70b-chat:2c1608e18606fad2812020dc541930f2d0495ce32eee50074220b87300bc16e1",
        input={
            "prompt": f"Given this article data from the user input {fed_data} and given this data I scraped from the internet {fetched_data}. Based on this information can you tell if the news fed from the user talks about the same thing to the news from the internet, and how likely is it that this news from the user is an actual real news. Keep your replies to 50 words max"
        }
    )
    output_str = ""
    for item in output:
        output_str += item
        print(item)
    
    return output_str



def similarity_checker(search_query, article_content):

    fetched_content = ""

    html_content = google_search(search_query)
    if html_content:
        data = extract_headings_and_links(html_content)
        
        print(f"Top 10 headings and URLs for '{search_query}':")
        urls = []
        titles = []
        for i, entry in enumerate(data[:5], 1):
            titles.append(entry['heading'])
            urls.append(entry['url'])
            print(f"{i}. {entry['heading']} - {entry['url']}")
        
        print("Fetching content from the URLs...")
        for url, title in zip(urls, titles):
            content = extract_text_from_link(url)
            if content:
                print(f"\nContent for '{title}':\n{content}")
                fetched_content += content
            
        max_char_len = 5000
        if (len(fetched_content) < max_char_len):
            max_char_len = len(fetched_content)

        print(fetched_content[:max_char_len])

        response = llama2_comparison(article_content, fetched_content[:1000])

        return response
    
    return "Unable to fetch data, please try again!"

#if __name__ == "__main__":
    #main()