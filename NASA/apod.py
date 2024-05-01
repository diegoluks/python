import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, url_for

load_dotenv()

app = Flask(__name__)

# Carregar a chave da API da NASA do arquivo .env
api_key = os.getenv('NASA_API_KEY')

# Verificar se a chave da API está presente
if not api_key:
    raise ValueError("Chave da API da NASA não encontrada. Por favor, defina a variável de ambiente 'NASA_API_KEY'.")

def get_nasa_image_info(search_date):
    """Obter informações sobre a imagem da NASA para a data especificada."""
    url = "https://api.nasa.gov/planetary/apod"
    params = {'api_key': api_key, 'date': search_date}
    response = requests.get(url, params=params)

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
    """Rota principal para renderizar a página inicial e fornecer informações sobre a imagem da NASA."""
    if request.method == 'POST':
        # Obter a data de busca do formulário
        search_date = request.form['search_date']
        
        # Obter informações sobre a imagem da NASA para a data especificada
        nasa_image_info = get_nasa_image_info(search_date)

        # Salvar a imagem localmente
        image_url = nasa_image_info['url']
        image_filename = image_url.split('/')[-1]
        image_path = os.path.join(app.root_path, 'static', image_filename)
        with open(image_path, 'wb') as f:
            f.write(requests.get(image_url).content)
        
        # Atualizar o URL da imagem para ser servido localmente
        nasa_image_info['url'] = url_for('static', filename=image_filename)

        # Retornar as informações em formato JSON
        return jsonify(nasa_image_info)
    
    # Renderizar a página inicial
    return render_template('index.html')

if __name__ == "__main__":
    # Executar o aplicativo Flask
    app.run()
