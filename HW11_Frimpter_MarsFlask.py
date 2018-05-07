# HW11_Frimpter_MarsFlask
# Terminal >> Navigate to project folder
# >> export FLASK_APP=HW11_Frimpter_MarsFlask.py
# >> flask run

from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo

app = Flask(__name__)
mongo = PyMongo(app)

client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db # Define the db
mars_scrape = db.mars_scrape # Define the collection

import mars_test
mars_data = mars_test

@app.route("/")  # , methods=['GET']
def index():
        #mars = db.items.find_one()
        mars = mars_test
        return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    #import HW11_Frimpter_ScrapingMars
    #mars_data = HW11_Frimpter_ScrapingMars.scrape()
    import mars_test
    mars_data = mars_test

    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client.mars_db  # Define the db
    mars_scrape = db.mars_scrape  # Define the collection

    mars_scrape.update(mars_data, upsert=True, multi=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
