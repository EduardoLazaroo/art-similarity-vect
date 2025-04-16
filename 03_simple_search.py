from flask import Flask, request, jsonify, render_template
import os
import numpy as np
from qdrant_client import QdrantClient
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.preprocessing import image as keras_image
from werkzeug.utils import secure_filename
from config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
base_model = EfficientNetB0(weights="imagenet", include_top=False, pooling="avg")

def image_to_vector(img_path):
    img = keras_image.load_img(img_path, target_size=(224, 224))
    x = keras_image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    vector = base_model.predict(x)[0].tolist()
    return vector

def search_similar_images(image_path, threshold=0.35):
    query_vector = image_to_vector(image_path)
    result = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=5,
        score_threshold=threshold
    )

    results = []
    for hit in result:
        results.append({
            "nome_arquivo": hit.payload.get("nome_arquivo", "desconhecido"),
            "score": hit.score
        })

    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    results = search_similar_images(filepath)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
