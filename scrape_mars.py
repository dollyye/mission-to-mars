
# coding: utf-8

# In[1]:


# Dependencies
import time
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from selenium import webdriver
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# In[2]:
def scrape():

    # dictionary for scrape data
    mars_data = {}

#-------------------------------------
# NASA Mars News
#-------------------------------------

    # URL of NASA Mars News Site
    news_url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    news_response = requests.get(news_url)
    # Create BeautifulSoup object; parse with 'html.parser'
    news_soup = BeautifulSoup(news_response.text, 'html.parser')

    # Examine the results, then get content title text
    news_title = news_soup.find("div", class_="content_title").a.text.strip()

    # retrieve the paragraph text
    news_p = news_soup.find("div", class_="rollover_description_inner").text.strip()

    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p

# In[3]:


#-------------------------------------
# JPL Mars Space Images - Featured Image
#-------------------------------------

    nasa_url = "https://www.jpl.nasa.gov"
    img_search = "/spaceimages/?search=&category=Mars"
    mars_url = nasa_url+img_search
    mars_response = requests.get(mars_url)
    img_soup = BeautifulSoup(mars_response.text, "html.parser")
    img_src = img_soup.find("a", class_="button fancybox")["data-fancybox-href"]
    featured_image_url = nasa_url+img_src
    mars_data['featured_image_url'] = featured_image_url

# In[4]:


#-------------------------------------
# Mars Weather
#-------------------------------------

    twitter_url = "https://twitter.com/marswxreport?lang=en"
    weather_response = requests.get(twitter_url)
    weather_soup = BeautifulSoup(weather_response.text, "html.parser")
    mars_weather = weather_soup.find("div", class_="js-tweet-text-container").p.text

    mars_data['mars_weather'] = mars_weather

# In[5]:


#-------------------------------------
# Mars Facts
#-------------------------------------
    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    facts_df = tables[0]
    mars_facts = facts_df.to_html(justify='left', header=False, index=False, index_names=False)
    mars_data['mars_facts'] = mars_facts


# In[6]:


#-------------------------------------
# Mars Hemispheres
#-------------------------------------

    browser = init_browser()
    usgs_url = "https://astrogeology.usgs.gov"
    hemisphere_search = "/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url+hemisphere_search)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    descriptions = soup.find_all('div', class_='description')

    title = []
    url_list = []
    img_url = []

    for description in descriptions:
        hemisphere_name = description.h3.text.strip()
        title.append(hemisphere_name)
        hemisphere_url = description.find('a')['href']
        url_list.append(hemisphere_url)
        time.sleep(2)
        
    hemisphere_url_list = [usgs_url + url for url in url_list]

    img_url = []

    for h_url in hemisphere_url_list:
        browser = init_browser()
        browser.visit(h_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        download = soup.find("div", class_="downloads")
        hemisphere_img = download.find('a')['href']
        img_url.append(hemisphere_img)
        time.sleep(2)
    
    hemisphere_image_urls = []
    for i, j in zip(title, img_url):
        hemi = {"title": i, "img_url": j}
        hemisphere_image_urls.append(hemi)

    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_data