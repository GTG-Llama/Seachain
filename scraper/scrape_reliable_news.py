import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By

import undetected_chromedriver as uc



start_time = time.time()

MONTHS_BEFORE = 3
current_datetime = datetime.now()
min_date = current_datetime - relativedelta(months=MONTHS_BEFORE)



###################################
#    Financial Times Headlines    #
###################################

# Specify sections
FT_SECTIONS = ["world", "companies", "technology", "markets", "climate-capital", "work-careers"]

# Scrape news
news_headlines = []

for section in FT_SECTIONS:
    print("Scraping", section)

    page = 1
    while True: # Increment pages
        url="https://www.ft.com/{}?page={}".format(section, page)
        result=requests.get(url)
        content=result.content
        soup=BeautifulSoup(content, "lxml")

        break_loop = False  # Tracker set to True if article is earlier than min_date

        # Iterate over each page
        for article in soup.findAll("li", {"class": "o-teaser-collection__item o-grid-row"}):
            try:
                title = article.find("div", {"class": "o-teaser__heading"}).text
                caption = article.find("p", {"class": "o-teaser__standfirst"}).text
                date_string = article.find("time", {"class": "o-date"})['datetime']

                # Check if date is within specified bounds
                date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
                if date < min_date:
                    break_loop = True
                    break

                news_headlines.append({
                    "Title": title,
                    "URL": url,
                    "Caption": caption,
                    "Date_Of_Publication": date, # datetime in string format 
                    "Section": section
                })

            except:
                continue

        if break_loop:
            break

        page += 1

ft_df = pd.DataFrame(news_headlines)
ft_df.to_csv('financial_times_sectioned.csv', index=False)

print("Financial Times (World News)")
print("Total number of headlines: {}".format(len(news_headlines)))
print("Value counts for", ft_df['Section'].value_counts())
del ft_df  # Remove from memory


############################
#       Reuters News       #
############################

# Specify sections

REUTERS_SECTIONS = ["business", "markets/asia", "markets/carbon", "markets/commodities", "markets/currencies", "markets/deals",
                    "markets/emerging", "markets/etf", "markets/europe", "markets/funds", "markets/rates-bonds",
                    "markets/stocks", "markets/us", "markets/wealth", "markets/macromatters"]

# Create an object of the Chrome webdriver
my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={my_user_agent}")

driver = uc.Chrome(options=options)
driver.implicitly_wait(5)

# Scrape news
reuters_news = []

for section in REUTERS_SECTIONS:
    # Initialize webdriver
    driver.get('/'.join(["https://www.reuters.com", section]))

    while True:
        # Retrieve page source info from driver
        page_source = driver.page_source

        # Get all news articles
        soup = BeautifulSoup(page_source, 'lxml')
        news_articles = soup.find_all('li', class_='story-collection__story__LeZ29')
        
        # Check if last news article meets date requirement
        last_news_article = news_articles[-1] 
        date_string = last_news_article.find("time")['datetime']
        try:
            news_date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%SZ")
        except: 
            news_date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))

        # Break if last news article was published before the min_date, else press "Load more articles" element
        if news_date < min_date:
            break
        else:
            try:
                driver.find_element(By.XPATH, '//button[(.//*|.)[contains(text(), "Load more articles")]]').click()
                time.sleep(3) # Wait for new articles to load
            except: # Break if button is no longer displayed
                break 

    print(len(news_articles))

    for news_item in news_articles:
        category = news_item.find("span", {"data-testid": "Label"})
        
        try:
            if category.find("a", {"data-testid": "Link"}):
                category = category.find("a", {"data-testid": "Link"}).text.replace("category", "")
            elif category.find("span", {"data-testid": "Text"}):
                category = category.find("span", {"data-testid": "Text"}).text.replace("category", "")
        except:
            category = None
            print("Category not found")

        try:
            if news_item.find("h3", {"data-testid": "Heading"}):
                title_object = news_item.find("h3", {"data-testid": "Heading"}).find("a", {"data-testid": "Link"})
            elif news_item.find("a", {"data-testid": "Heading"}):
                title_object = news_item.find("a", {"data-testid": "Heading"})
            title = title_object.text
            url = "https://www.reuters.com" + title_object.get("href")
        except:
            title = None
            url = None
            print("Title not found")

        try:
            date = datetime.strptime(news_item.find("time")['datetime'], "%Y-%m-%dT%H:%M:%SZ")
        except:
            date = None
            print("Date not found")
        
        if url:
            result = requests.get(url)
            content = result.content
            page_soup = BeautifulSoup(content, "lxml")

            body = page_soup.find("div", {"class": "article-body__content__17Yit"})
            all_paragraphs = [paragraph.text for paragraph in body.find_all('p')]
            text = ' '.join(all_paragraphs)

            reuters_news.append({
                "Title": title,
                "URL": url,
                "Category": category,
                "Date_Of_Publication": date, # datetime in string format 
                "Section": section,
                "Body": text
            })

driver.quit()
reuters_df = pd.DataFrame(reuters_news)
reuters_df.to_csv('reuters_sectioned.csv', index=False)

print("Financial Times (World News)")
print("Total number of articles: {}".format(len(reuters_news)))
print("Value counts for", reuters_df['Section'].value_counts())
del reuters_df  # Remove from memory



# Check how long does it take the script to run
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Time taken to complete the program: {elapsed_time} seconds")
