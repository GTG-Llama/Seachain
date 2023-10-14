import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape news article
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


def scrape_article(url):
    # Fetch the page content
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the title and author
    title = soup.select_one('h1#main-heading').text if soup.select_one('h1#main-heading') else "N/A"
    author = soup.select_one('div.ssrcss-68pt20-Text-TextContributorName').text if soup.select_one('div.ssrcss-68pt20-Text-TextContributorName') else "N/A"
    
    # Extract the main body text by looping through each text block
    body_text_blocks = soup.select('div.ssrcss-11r1m41-RichTextComponentWrapper p')
    body = ' '.join([block.text for block in body_text_blocks])
    
    return {
        'Title': title,
        'Author': author,
        'URL': url,
        'Body': body
    }


# URL to scrape
url_to_scrape = "https://www.bbc.com/news/world-middle-east-67040221"

# Scrape the article
article_data = scrape_article(url_to_scrape)

# Output the scraped data to the console
print("Scraped Data:")
print(article_data)

# Save to CSV if scraping was successful
if article_data:
    keys = ['Title', 'Author', 'URL', 'Body']
    with open('article_data.csv', 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=keys)
        writer.writeheader()
        writer.writerow(article_data)
#     print("CSV file generated: article_data.csv")

# import requests
# from bs4 import BeautifulSoup
# import csv

# def scrape_article(url):
#     print(f"Scraping {url}...")
#     response = requests.get(url)
#     if response.status_code != 200:
#         print("Failed to fetch article.")
#         return None

#     soup = BeautifulSoup(response.text, 'html.parser')
#     title = soup.select_one('h1#main-heading').text if soup.select_one('h1#main-heading') else "N/A"
#     author = soup.select_one('div.ssrcss-68pt20-Text-TextContributorName').text if soup.select_one('div.ssrcss-68pt20-Text-TextContributorName') else "N/A"
#     body_text_blocks = soup.select('div.ssrcss-11r1m41-RichTextComponentWrapper p')
#     body = ' '.join([block.text for block in body_text_blocks])
    
#     print(f"Scraped title: {title}")
    
#     return {
#         'Title': title,
#         'Author': author,
#         'URL': url,
#         'Body': body
#     }

# def get_recent_articles(main_url, num_articles=10):
#     print(f"Fetching recent articles from {main_url}...")
#     response = requests.get(main_url)
#     if response.status_code != 200:
#         print("Failed to fetch main page.")
#         return None

#     soup = BeautifulSoup(response.text, 'html.parser')
#     article_links = soup.select('a.block-link__overlay-link')[:num_articles]  # Replace 'YOUR_ARTICLE_LINK_SELECTOR'
#     article_urls = ['https://www.bbc.com' + link['href'] for link in article_links]
    
#     print(f"Fetched {len(article_urls)} article URLs.")
    
#     return article_urls

# # Main URL of BBC
# main_url = 'https://www.bbc.com/'

# # Get first 10 recent article URLs
# recent_articles = get_recent_articles(main_url, 10)

# if recent_articles:
#     # Initialize a list to hold all articles data
#     all_articles_data = []

#     # Scrape each article
#     for url in recent_articles:
#         article_data = scrape_article(url)
#         if article_data:
#             all_articles_data.append(article_data)

#     # Save all scraped data to CSV
#     keys = ['Title', 'Author', 'URL', 'Body']
#     with open('all_articles_data.csv', 'w', newline='') as output_file:
#         writer = csv.DictWriter(output_file, fieldnames=keys)
#         writer.writeheader()
#         writer.writerows(all_articles_data)
#     print("CSV file generated: all_articles_data.csv")
# else:
#     print("No article URLs fetched.")
