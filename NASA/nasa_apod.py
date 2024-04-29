import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

app = Flask(__name__)

api_key = os.getenv('NASA_API_KEY')

def api_nasa(search_date):
    url = "https://api.nasa.gov/planetary/apod"
    
    query = {
        'api_key': api_key,
        'date': search_date 
    }

    r = requests.get(url, params=query)

    if r.status_code == 200:
        response = r.json()
        return response['url']
    else:
        return None

def download_picture(url_picture):
    r = requests.get(url_picture)
    with open('static/picture_from_nasa.jpg', 'wb') as file:
        file.write(r.content)

@app.route('/', methods=['GET', 'POST'])
def index():
    nasa_image_url = None
    if request.method == 'POST':
        data_desejada = request.form['data_desejada']
        response_data = api_nasa(data_desejada)
        if response_data:
            nasa_image_url = response_data
            download_picture(nasa_image_url)
    return render_template('index.html', nasa_image_url=nasa_image_url)

if __name__ == "__main__":
    app.run(debug=True)
