import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

load_dotenv()

app = Flask(__name__)

api_key = os.getenv('NASA_API_KEY')

def get_nasa_image_info(search_date):
    url = "https://api.nasa.gov/planetary/apod"
    query = {'api_key': api_key, 'date': search_date}
    response = requests.get(url, params=query)

    if response.status_code == 200:
        data = response.json()
        return {
            'date': data['date'],
            'title': data['title'],
            'explanation': data['explanation'],
            'url': data.get('hdurl') or data['url']
        }
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_date = request.form['search_date']
        nasa_image_info = get_nasa_image_info(search_date)
        return jsonify(nasa_image_info)
    return render_template('index.html')

if __name__ == "__main__":
    app.run()
