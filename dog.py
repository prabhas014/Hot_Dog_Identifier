from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("HUGGING_FACE_API_URL")
API_KEY = os.getenv("HUGGING_FACE_API_KEY")

app = Flask(__name__)

def query(file):
    file_bytes = file.read()
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": file.mimetype   # automatically sets image/jpeg, image/png etc.
        },
        data=file_bytes
    )
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file1']
    modeldata = query(file)
    top_prediction = max(modeldata, key=lambda x: x["score"])["label"]

    return render_template("index.html", prediction=top_prediction)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81, debug=True)
