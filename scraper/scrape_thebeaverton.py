import os
import time
import requests
import random
from bs4 import BeautifulSoup
import csv
# Check how long does it take the script to run
start_time = time.time()

# Configuration section
CONFIG = {
    "user_agents": [
        'Mozilla/5.0 ...',
        'Mozilla/5.0 ...',
        'Mozilla/5.0 ...',
    ],
    "referer": "https://www.thebeaverton.com/news/", # for bypass bot detection, same or more general than "main_url"
    "main_url": "https://www.thebeaverton.com/news/business/", # main page where we want to scrape all articles
    "first_page_url": "https://www.thebeaverton.com/news/business/", # the first page that we want to scrape
    "test_single_page_url": "https://www.thebeaverton.com/news/business/page/3", # a random page that contains many articles
    "test_single_article_url": "https://www.thebeaverton.com/2023/10/in-event-of-cabin-pressure-change-air-canada-instructs-passengers-to-secure-own-mask-before-360-roundhouse-kicking-the-person-next-to-them/", # a random article
    "title_selector": "header.post-title.entry-header .entry-title", # article title
    "author_selector": "aside.post-author span[itemprop=\"author\"] a", # article author
    "body_selector": "div.post-content.entry-content p", # article content
    "article_selector": 'header.post-title.entry-header h3[itemprop="headline"] a', # the html tags for an article on a category page
    "num_articles_to_scrape": 10, # number of aricles, must be multiple of the number of articles in a page
    "articles_per_page": 10, # how many articles in a page
    "csv_filename": "satirewire_biz_briefs_fake_news.csv" # export file name
}
###################################################

######
# function to scrape single News
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
        "Referer": CONFIG['referer']
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
    title = soup.select_one(CONFIG['title_selector']).text if soup.select_one(CONFIG['title_selector']) else "N/A"
    author = soup.select_one(CONFIG['author_selector']).text if soup.select_one(CONFIG['author_selector']) else "N/A"
    body_text_blocks = soup.select(CONFIG['body_selector']) # for all websites
    body = ' '.join([block.text for block in body_text_blocks]) if body_text_blocks else "N/A" # for all websites
    # entry_content = soup.select_one(CONFIG['body_selector']) # for satire wire, might not work for others
    # body_text_blocks = entry_content.find_all(['p', 'span'], text=True) if entry_content else [] # for satire wire, might not work for others
    # body = ' '.join(block.get_text(strip=True) for block in body_text_blocks) if body_text_blocks else "N/A" # for satire wire, might not work for others
    
    return {
        'Title': title,
        'Author': author,
        'URL': url,
        'Body': body
    }
###################################################

#######
# (For testing) Run the function to get content from one news article (this function works for any website, cuz it's using abstraction)
#######

# # URL to scrape
# url_to_scrape = CONFIG['test_single_article_url']

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
#     with open(csv_path, 'w', newline='', encoding='utf-8') as output_file:
#         writer = csv.DictWriter(output_file, fieldnames=keys)
#         writer.writeheader()
#         writer.writerow(article_data)
#     print("CSV file generated: single_article_data_for_testing.csv")




# ###################################################
# #######
# # FUNCTION to get urls of multiple news articles given main news website (single page)
# #######

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
    article_links = soup.select(CONFIG['article_selector'])[:num_articles]  # Replace 'the part inside .select(...)'
    article_urls = [link['href'] for link in article_links]
    
    print(f"Fetched {len(article_urls)} article URLs.")
    
    return article_urls

# ## Testing printing all urls for a single home page
# page_url = CONFIG['test_single_page_url']
# print(get_recent_articles(page_url, 10))


# ###################################################
# #######
# # GET and PRINT urls of multiple news articles given main news website (multiple pages)
# #######

# Main URL of Waterford Whispers News
main_url = CONFIG['main_url']
num_articles_to_scrape = CONFIG['num_articles_to_scrape']  #must be mutiples of 10, cuz there's 10 news on each page, we are scraping all news in one page
max_page_index = (num_articles_to_scrape//CONFIG['articles_per_page'])
recent_articles = []
# Get first "num_articles_to_scrape" recent article URLs
for page_index in range(1, max_page_index+1, 1): #the first page's index is 1, every other page index increase by 1
    if page_index == 1:
        page_url = CONFIG['first_page_url']
    else:
        page_url = main_url + "page/" + str(page_index) + "/"
    print("Got URLs for page", page_index)
    recent_articles += get_recent_articles(page_url, CONFIG['articles_per_page']) #10 is the max article in a single page

# print all the article links that will be scraped
print()
print("Total", len(recent_articles), "articles fetched.", "Below are the urls:")
print(recent_articles)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the path for the new CSV file to be in the same directory as the script
csv_path = os.path.join(script_dir, CONFIG['csv_filename'])


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
    with open(csv_path, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_articles_data)
    print("CSV file generated:", CONFIG['csv_filename'])
else:
    print("No article URLs fetched.")
#################################################



# Check how long does it take the script to run
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken to complete the program: {elapsed_time} seconds")
