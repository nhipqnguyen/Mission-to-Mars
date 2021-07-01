# import tools
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the route for the HTML page
@app.route("/")
def index():
    # use PyMongo to find the "mars" collection in our database
   mars = mongo.db.mars.find_one()
    # return an HTML template using an index.html file
   return render_template("index.html", mars=mars)

# define the 'scrape' route
@app.route("/scrape")
def scrape():
   # assign a new variable that points to our Mongo database
   mars = mongo.db.mars
   # create a new variable to hold the newly scraped data
   mars_data = scraping.scrape_all()
   # update the database with the new data
   mars.update({}, mars_data, upsert=True)
   # add a redirect after successfully scraping the data
   return redirect('/', code=302)

# tell flask to run
if __name__ == "__main__":
    app.run()