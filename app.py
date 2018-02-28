from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)
mongo = PyMongo(app)


@app.route('/')
def index():
    mars = mongo.db.marsmission.find_one()
    return render_template('index.html', mars=mars)

@app.route('/scrape')
def scraping():
    marsmission = mongo.db.marsmission
    data = scrape_mars.scraping()
    marsmission.update({}, data, upsert=True)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
