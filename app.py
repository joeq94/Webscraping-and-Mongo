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

app = Flask(__name__)
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_scrape")

@app.route("/")
def home():
    
    return render_template("index.html")


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    title_paragraph = scrape_mars.scrape_news()
    featured_image_url = scrape_mars.scrape_featured_image()
    mars_hemi = scrape_mars.scrape_hemi_img()
   
    mars_news_data = {
        'news_title_p': title_paragraph,
        'featured_image_url': featured_image_url,
        'hemisphere_image_urls': mars_hemi
        }
        
    # update database
    mongo.db.collection.update({}, mars_news_data, upsert=True)
    mars_news_data = mongo.db.collection.find_one()

    return render_template("scrape.html", mars_news_data = mars_news_data)


if __name__ == "__main__":
    app.run(debug=True)
