# Import Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from datetime import datetime
import os
import time
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape_news():
    browser = init_browser()
    
    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)
    time.sleep(2)

    html = browser.html
    soup = bs(html,"html.parser")

    slides = soup.find_all("li", class_="slide")
    # create lists to append title and paragraph
    news_title = []
    paragraph_text = []

    content_title = slides[0].find('div', class_='content_title').text
    article_teaser = slides[0].find('div', class_='article_teaser_body').text
        
    news_t_p = {"Title": content_title, 
                "Paragraph": article_teaser
                }
    browser.quit()            
    return news_t_p

def scrape_featured_image():
    jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser = init_browser()
    # Retrieve page with the requests module and visit url
    browser.visit(jpl_url)
    html = browser.html
    soup = bs(html, 'html.parser')

    # find featured image img link
    img_link = soup.find('img', class_='headerimage')['src']
    img_link
    browser.quit()
    featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_link}'
    return featured_image_url

def scrape_hemi_img():
    browser = init_browser()

    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    hemispheres = ["Cerberus Hemisphere Enhanced","Schiaparelli Hemisphere Enhanced","Syrtis Major Hemisphere Enhanced","Valles Marineris Hemisphere Enhanced"]
    browser.visit(hemi_url)
    img_urls= []
    hemisphere_image_urls = []
    for hemisphere in hemispheres:
        browser.click_link_by_partial_text(f"{hemisphere}")
        html = browser.html
        soup = bs(html, "html.parser")
        
        img_url = (soup.find('div', class_="downloads").find('a')['href'])
        img_urls.append(img_url)
        
        hemisphere_image_urls.append({"title": hemisphere, "img_url":img_url})
        # slow the website scrape as page is very slow
        time.sleep(1)
        
        # go back to products page
        browser.back()
        
    browser.quit()
    return hemisphere_image_urls
