import os
import time
import requests
import random
from bs4 import BeautifulSoup
import csv
# Check how long does it take the script to run
start_time = time.time()

########
# General function to scrape news article (not quite working for any site cuz this html is not specific to the websites)
########

# def scrape_article(url):
#     # Fetch the page content
#     response = requests.get(url)
#     if response.status_code != 200:
#         return None
    
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # Extract the title, author, and main body text
#     # Note: These selectors are hypothetical. You'll need to inspect the actual HTML to find the correct ones.
#     # title = soup.select_one('h1.title').text if soup.select_one('h1.title') else "N/A"
#     # author = soup.select_one('span.author').text if soup.select_one('span.author') else "N/A"
#     title = soup.select_one('h1#main-heading').text if soup.select_one('h1#main-heading') else "N/A"
#     author = soup.select_one('div.ssrcss-68pt20-Text-TextContributorName').text if soup.select_one('div.ssrcss-68pt20-Text-TextContributorName') else "N/A"
#     body = soup.select_one('div.article-body').text if soup.select_one('div.article-body') else "N/A"
    
#     return {
#         'Title': title,
#         'Author': author,
#         'URL': url,
#         'Body': body
#     }


###################################################

########
# Scrape single BBC News
#########

# def scrape_article(url):
#     # Fetch the page content
#     response = requests.get(url)
#     if response.status_code != 200:
#         return None
    
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # Extract the title and author
#     title = soup.select_one('h1#main-heading').text if soup.select_one('h1#main-heading') else "N/A"
#     author = soup.select_one('div.ssrcss-68pt20-Text-TextContributorName').text if soup.select_one('div.ssrcss-68pt20-Text-TextContributorName') else "N/A"
    
#     # Extract the main body text by looping through each text block
#     body_text_blocks = soup.select('div.ssrcss-11r1m41-RichTextComponentWrapper p')
#     body = ' '.join([block.text for block in body_text_blocks])
    
#     return {
#         'Title': title,
#         'Author': author,
#         'URL': url,
#         'Body': body
#     }

###################################################

######
# function to scrape single Waterford Whispers News
######

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537',
]

def scrape_article(url):
    # Fetch the page content
    headers = {
        "User-Agent": random.choice(user_agents),
        "Referer": "https://waterfordwhispersnews.com/category/business/"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        print(f"Failed to fetch article {url}. Error: {e}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the title, author, and main body text
    # Note: These selectors are hypothetical. You'll need to inspect the actual HTML to find the correct ones.
    # title = soup.select_one('h1.title').text if soup.select_one('h1.title') else "N/A"
    # author = soup.select_one('span.author').text if soup.select_one('span.author') else "N/A"
    title = soup.select_one('div.s_header_wraper div.s-post-header h1[itemprop="headline"]').text if soup.select_one('div.s_header_wraper div.s-post-header h1[itemprop="headline"]') else "N/A"
    author = soup.select_one('div.post-author[itemprop="author"] a').text if soup.select_one('div.post-author[itemprop="author"] a') else "N/A"
    body_text_blocks = soup.select('div.article-content[itemprop="articleBody"] p')
    body = ' '.join([block.text for block in body_text_blocks]) if body_text_blocks else "N/A"
    
    return {
        'Title': title,
        'Author': author,
        'URL': url,
        'Body': body
    }
###################################################

#######
# Run the function to get content from one news article (this function works for any website, cuz it's using abstraction)
#######

# # URL to scrape
# url_to_scrape = "https://waterfordwhispersnews.com/2012/05/10/jobbridge-scheme-extended-by-30000-places-as-government-opens-cotton-picking-plantation-in-leitrim/"

# # Scrape the article
# article_data = scrape_article(url_to_scrape)

# # Output the scraped data to the console
# print("Scraped Data:")
# print(article_data)


# # Get the directory of the current script
# script_dir = os.path.dirname(os.path.abspath(__file__))

# # Create the path for the new CSV file to be in the same directory as the script
# csv_path = os.path.join(script_dir, 'single_article_data_for_testing.csv')

# # Save to CSV if scraping was successful
# if article_data:
#     keys = ['Title', 'Author', 'URL', 'Body']
#     with open(csv_path, 'w', newline='') as output_file:
#         writer = csv.DictWriter(output_file, fieldnames=keys)
#         writer.writeheader()
#         writer.writerow(article_data)
#     print("CSV file generated: single_article_data_for_testing.csv")




###################################################
#######
# FUNCTION to get urls of multiple news articles given main news website (one page)
#######

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.3",
}

def get_recent_articles(main_url, num_articles=10):
    print(f"Fetching recent articles from {main_url}...")
    
    try:
        response = requests.get(main_url, headers=headers)
        response.raise_for_status()  # will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        print(f"Failed to fetch main page. Error: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    article_links = soup.select('h4.title a')[:num_articles]  # Replace 'the part inside .select(...)'
    article_urls = [link['href'] for link in article_links]
    
    print(f"Fetched {len(article_urls)} article URLs.")
    
    return article_urls

### Testing printing all urls for a single home page
# page_url = 'https://waterfordwhispersnews.com/category/business/page/19/'
# print(get_recent_articles(page_url, 10))


###################################################
#######
# GET and PRINT urls of multiple news articles given main news website (multiple pages)
#######

# Main URL of Waterford Whispers News
main_url = 'https://waterfordwhispersnews.com/category/business/'
num_articles_to_scrape = 500  #must be mutiples of 10, cuz there's 10 news on each page, we are scraping all news in one page
max_page_index = (num_articles_to_scrape//10 + 1)
recent_articles = []
# Get first "num_articles_to_scrape" recent article URLs
for page_index in range(1, max_page_index, 1): #the first page's index is 1, every other page index increase by 1
    if page_index == 1:
        page_url = "https://waterfordwhispersnews.com/category/business/"
    else:
        page_url = main_url + "page/" + str(page_index) + "/"
    print("Got URLs for page", page_index)
    recent_articles += get_recent_articles(page_url, 10) #10 is the max article in a single page

# print all the article links that will be scraped
print()
print("Total", len(recent_articles), "articles fetched.", "Below are the urls:")
print(recent_articles)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the path for the new CSV file to be in the same directory as the script
csv_path = os.path.join(script_dir, 'waterford_whispers_fake_news.csv')


##################################################
#####
# scraping all the articles and output to csv
####
if recent_articles:
    # Initialize a list to hold all articles data
    all_articles_data = []

    # Scrape each article
    for index, url in enumerate(recent_articles):
        # time.sleep(1)  # sleep for 1 second
        article_data = scrape_article(url)
        if article_data:
            all_articles_data.append(article_data)
            print(f"Article {index+1} finished scraping")
        else:
            print(f"Article {index+1} failed to scrape")

    # Save all scraped data to CSV
    keys = ['Title', 'Author', 'URL', 'Body']
    with open(csv_path, 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_articles_data)
    print("CSV file generated: waterford_whispers_fake_news.csv")
else:
    print("No article URLs fetched.")
##################################################



# Check how long does it take the script to run
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken to complete the program: {elapsed_time} seconds")
