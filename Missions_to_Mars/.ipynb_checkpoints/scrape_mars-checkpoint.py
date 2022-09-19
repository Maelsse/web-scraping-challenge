# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template
import pandas as pd
import requests
import pymongo


# For scraping with Chrome
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict = {}
    
    #######################
    # NASA MARS NEWS      #
    #######################
    
    # Url to scrape
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'lxml')
    
    # Retrieve Latest News Title
    news_title = soup.find_all('div', class_='content_title')[0].text
    # Retrieve Latest News Paragraph
    news_paragraph = soup.find_all('div', class_='article_teaser_body')[0].text
    
    ##############################################
    # JPL Mars Space Images—Featured Image       #
    ##############################################
    
    # Url to Scrape
    jpl_url = 'https://spaceimages-mars.com/'
    browser.visit(jpl_url)
    image_html = browser.html
    soup = bs(image_html, 'lxml')
    
    # Find the Ft. Image
    ft_img = soup.find('img', class_='headerimage')['src']
    featured_image_url = jpl_url + ft_img
    
    #######################
    # MARS FACTS          #
    #######################
    
    mars_facts_url = 'https://galaxyfacts-mars.com'
    browser.visit(mars_facts_url)
    mars_facts_html = browser.html
    soup = bs(mars_facts_html, 'lxml')
    
    tables = pd.read_html(mars_facts_url)
    mars_facts = tables[0]
    
    # Formatting Columns
    mars_facts = mars_facts.rename(columns={0:"Description", 1:"Mars", 2:"Earth"}, errors="raise")
    mars_facts = mars_facts.set_index('Description') 
    mars_facts = mars_facts.iloc[1: , :]
    
    # To_html()
    mars_facts_table = mars_facts.to_html()
    mars_facts_table.replace('\n','')
    
    #############################
    # MARS HEMISPHERES          #
    #############################
    
    astro_url = 'https://marshemispheres.com/'
    browser.visit(astro_url)
    astro_html = browser.html
    soup = bs(astro_html, 'lxml')
    
    # Extract hemisphere item elements
    mars_hemis = soup.find('div', class_='collapsible results')
    mars_item = mars_hemis.find_all('div', class_='item')
    hemisphere_img_urls = []
    
    # Loop through each hemisphere item
    hemisphere_img_urls = []
    for item in mars_item:
        
        # Extract Title
        h3 = item.find_all('h3')
        img_title = h3[0].text
        
        # Extract IMG Url
        link = item.find('div',class_='description')
        a_url = link.a['href']
        
        # Go to page
        browser.visit(astro_url+a_url)
        img_html = browser.html
        soup = bs(img_html, 'lxml')
        img_src = soup.find('li').a['href']
        
        # Save the link
        
        img_url = astro_url + img_src
        
        # Save To Dictionary
        dict = {'title': img_title, 
                'img_url': img_url}
    
        hemisphere_img_urls.append(dict)

    # CREATE A DICTIONARY OF ALL SOURCES ABOVE
    
    mars_dict={"news_title": news_title,
              "news_p": news_paragraph,
              "featured_image_url": featured_image_url,
              "mars_facts_table":mars_facts_table,
              "hemisphere_imgs":hemisphere_img_urls,
              }
    
    # Close browser after scraping
    browser.quit()
    
    return mars_dict