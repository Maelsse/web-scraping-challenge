
#################################################
# Dependencies
##################################################

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

#################################################
# Database Setup
#################################################

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#################################################
# Flask Routes
#################################################

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_dict = mongo.db.mars_db.find_one()
    
    # Return template and data
    return render_template("index.html", mars_dict=mars_dict)

@app.route("/scrape")
def scraper():

    mars_dict = mongo.db.mars_db
    mars_data = scrape_mars.scrape()
        
    # Update the Mongo database using update and upsert=True
    mars_dict.update_many({}, {"$set": mars_data}, upsert=True)
        
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)