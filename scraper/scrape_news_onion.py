import os
import time
import requests
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
# function to scrape single onion news
######

def scrape_article(url):
    # Fetch the page content
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the title, author, and main body text
    # Note: These selectors are hypothetical. You'll need to inspect the actual HTML to find the correct ones.
    # title = soup.select_one('h1.title').text if soup.select_one('h1.title') else "N/A"
    # author = soup.select_one('span.author').text if soup.select_one('span.author') else "N/A"
    title = soup.select_one('h1.sc-1efpnfq-0.dAlcTj').text if soup.select_one('h1.sc-1efpnfq-0.dAlcTj') else "N/A"
    author = soup.select_one('div.ssrcss-68pt20-Text-TextContributorName').text if soup.select_one('div.ssrcss-68pt20-Text-TextContributorName') else "N/A"
    body_text_blocks = soup.select('p.sc-77igqf-0.fnnahv')
    body = ' '.join([block.text for block in body_text_blocks]) if body_text_blocks else "N/A"
    
    return {
        'Title': title,
        'Author': author,
        'URL': url,
        'Body': body
    }
###################################################

#####
# Run the function to get content from one url
#####

# # URL to scrape
# url_to_scrape = "https://www.theonion.com/pros-and-cons-of-keeping-senile-politicians-in-office-1850900125"

# # Scrape the article
# article_data = scrape_article(url_to_scrape)

# # Output the scraped data to the console
# print("Scraped Data:")
# print(article_data)


# # Get the directory of the current script
# script_dir = os.path.dirname(os.path.abspath(__file__))

# # Create the path for the new CSV file to be in the same directory as the script
# csv_path = os.path.join(script_dir, 'article_data.csv')

# # Save to CSV if scraping was successful
# if article_data:
#     keys = ['Title', 'Author', 'URL', 'Body']
#     with open(csv_path, 'w', newline='') as output_file:
#         writer = csv.DictWriter(output_file, fieldnames=keys)
#         writer.writeheader()
#         writer.writerow(article_data)
#     print("CSV file generated: article_data.csv")


###################################################
#######
# function to get urls of multiple news articles given main news website
#######

def get_recent_articles(main_url, num_articles=10):
    print(f"Fetching recent articles from {main_url}...")
    response = requests.get(main_url)
    if response.status_code != 200:
        print("Failed to fetch main page.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    article_links = soup.select('div.sc-cw4lnv-5.dYIPCV a.sc-1out364-0.dPMosf.js_link')[:num_articles]  # Replace 'YOUR_ARTICLE_LINK_SELECTOR'
    article_urls = [link['href'] for link in article_links]
    
    print(f"Fetched {len(article_urls)} article URLs.")
    
    return article_urls

# Main URL of BBC
main_url = 'https://www.theonion.com/politics'
num_articles_to_scrape = 500  #must be mutiples of 20, cuz there's 20 news on each page, we are scraping all news in one page
max_page_index = (num_articles_to_scrape//20 + 1) * 20
recent_articles = []
# Get first 100 recent article URLs
for page_index in range(20, max_page_index, 20): #the first page's index is 20, every other page index increase by 20
    page_url = main_url + "?startIndex=" + str(page_index)
    recent_articles += get_recent_articles(page_url, 20) #20 is the max article in a single page

# print all the article links that will be scraped
print()
print("Total", len(recent_articles), "articles fetched.", "Below are the urls:")
print(recent_articles)

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Create the path for the new CSV file to be in the same directory as the script
csv_path = os.path.join(script_dir, 'onion_fake_news.csv')

#####
# scraping all the articles and output to csv
####
if recent_articles:
    # Initialize a list to hold all articles data
    all_articles_data = []

    # Scrape each article
    for index, url in enumerate(recent_articles):
        article_data = scrape_article(url)
        if article_data:
            all_articles_data.append(article_data)
            print("Article", index+1, "finished scraping")

    # Save all scraped data to CSV
    keys = ['Title', 'Author', 'URL', 'Body']
    with open(csv_path, 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(all_articles_data)
    print("CSV file generated: onion_fake_news.csv")
else:
    print("No article URLs fetched.")
##################################################

# Check how long does it take the script to run
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken to complete the program: {elapsed_time} seconds")

