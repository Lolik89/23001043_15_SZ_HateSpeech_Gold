from flask import Flask, jsonify
import pandas as pd
import re

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from

app = Flask(__name__)

app.json_encoder = LazyJSONEncoder

swagger_template = {
      "swagger": "2.0",
      "info": {
        "title":  "API Documentation for Data Processing and Modeling",
        "version": "1.0.0",
        "description": "Dokumentasi API untuk Data Processing dan Modeling"
    },
    #"host": "127.0.0.1:5000"
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json',
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template, config=swagger_config)

#TEXT PROCESSING

@swag_from('docs/text-clean-by-user.yml', methods=['POST'])
@app.route('/text-clean-by-user', methods=['POST'])
def text_clean_by_user():

    inputText = request.form.get('text')

    json_response = {
        'status_code': 200,
        'description': 'Original Text',
        'data': re.sub(r'[^a-zA-Z0-9]', ' ', inputText)
    }

    response_data = jsonify(json_response)

    return response_data

@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing():
    text = request.form.get('text')
    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': re.sub(r'[^a-zA-Z0-9]', ' ', text),
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/text_processing_file.yml", methods=['POST'])
@app.route('/text-processing-file', methods=['POST'])
def text_processing_file():

    # Upladed file
    file = request.files.getlist('file')[0]

    # Import file csv ke Pandas
    df = pd.read_csv(file)

    # Ambil teks yang akan diproses dalam format list
    texts = df.text.to_list()

    # Lakukan cleansing pada teks
    cleaned_text = []
    for text in texts:
        cleaned_text.append(re.sub(r'[^a-zA-Z0-9]', ' ', text))

    json_response = {
        'status_code': 200,
        'description': "Teks yang sudah diproses",
        'data': cleaned_text,
    }

    response_data = jsonify(json_response)
    return response_data

if __name__ == '__main__':
        app.run()