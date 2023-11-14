import requests
from bs4 import BeautifulSoup
import re
from urllib.request import urlopen, Request

def get_links_forbes(ticker): #forbes stops tracking
    url = f"https://www.forbes.com/search/?q={ticker}&sh=3d5ce05c279f"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = soup.find_all(class_ = "stream-item__title", href=True)
    dicter = {}
    for items in data:
        string = items.prettify() #makes data into a string
        string = re.sub("<.*?>", " ", string)
        dicter[string] = (items['href'])
    return dicter #returns dict of links

def get_content_forbes(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'lxml')
    a_tags = soup.find_all("a")
    span_tags = soup.find_all("span")
    img_tags = soup.find_all("img")
    for rows in img_tags:
        rows.extract()
    for rows in a_tags:
        rows.extract()
    for rows in span_tags:
        rows.extract()
    try:    
        data = soup.find_all("div", class_ = "article-body fs-article fs-responsive-text current-article" )[0].findAll("p")
    except:
        return ""
    lister = []
    string = ""
    for rows in data:
        lister.append(str(rows))
    for rows in lister:
        rows = re.sub("<.*?>", " ", rows)
        rows = re.sub("</p>", " ", rows)
        string += rows
    return string #returns content in url

def main(ticker):
    #get dict of links
    dict_link = get_links_forbes(ticker)
    lister = list(dict_link.items())
    fin_data = {}
    
    for rows in lister:
        title = rows[0]
        #print (rows[1])
        content = get_content_forbes(rows[1])
        fin_data[title] = content
    return fin_data

def get_links_and_title(ticker):
    dict_link = get_links_forbes(ticker)
    lister = list(dict_link.items())
    fin_data = {}

    for rows in lister:
        title = rows[0]
        links = rows[1]
        fin_data[title] = links
    return fin_data

