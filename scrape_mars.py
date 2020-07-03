# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

def scrape():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="article_teaser_body").text
    
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    img = soup.find('article', class_="carousel_item")
    href = img.a.get("data-fancybox-href")
    featured_image_url = "https://www.jpl.nasa.gov" + href
    
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    twt = soup.find('div', class_='js-tweet-text-container')
    mars_weather = twt.p.text
    
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    df = tables[0]
    df.columns=["Category", "Value"]
    df.set_index("Category")
    html_table = df.to_html

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    titles = soup.find_all('div', class_='description')
    title_list = []
    for title in titles:
        title_list.append(title.h3.text)
        
    base = "https://astrogeology.usgs.gov"
    url_list = []
    for title in titles:
        url1 = base + title.a["href"]
        browser.visit(url1)
        html1 = browser.html
        soup1 = bs(html1, 'html.parser')
        img = soup1.find('div', class_='downloads') 
        url_list.append(img.li.a["href"])
        
    hemisphere_image_urls = []
    for i in range(4):
        hemisphere_image_urls.append ({'title': title_list[i],'img_url': url_list[i]})
    
    

    scrape_data = {'news title': news_title,
                   'news paragraph':news_p,
                   'featured image url':featured_image_url,
                   'mars weather':mars_weather,
                   'html table':html_table,
                   'hemisphere image urls':hemisphere_image_urls}
    return scrape_data