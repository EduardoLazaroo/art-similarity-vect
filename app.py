# Importações necessárias
import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from qdrant_client import QdrantClient
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.preprocessing import image as keras_image
from db_utils import get_info_by_filename
from minio import Minio
from minio.error import S3Error
from config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME
from config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET

# Configurações iniciais do Flask
app = Flask(__name__)
CORS(app)

# Config pasta de upload
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inicializa Qdrant e modelo
client_qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
base_model = EfficientNetB0(weights="imagenet", include_top=False, pooling="avg")

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)
bucket_name = MINIO_BUCKET

# Função pra gerar vetor da imagem
def image_to_vector(img_path):
    img = keras_image.load_img(img_path, target_size=(224, 224))
    x = keras_image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    vector = base_model.predict(x)[0].tolist()
    return vector

# Busca imagens similares
def search_similar_images(image_path, threshold=0.35):
    query_vector = image_to_vector(image_path)
    result = client_qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=20,
        score_threshold=threshold
    )

    results = []
    for hit in result:
        nome_arquivo = hit.payload.get("nome_arquivo", "desconhecido")
        dados = get_info_by_filename(nome_arquivo)

        results.append({
            "nome_arquivo": nome_arquivo,
            "score": hit.score,
            "url": dados['url'] if dados else None,
            "info": dados['info'] if dados else []
        })

    return results

# Rota pra buscar similares
@app.route('/api/search', methods=['POST'])
def search():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    print(f"Processando imagem: {filename}")

    try:
        results = search_similar_images(filepath)
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota pra buscar info por nome do arquivo
@app.route('/info/<nome_arquivo>', methods=['GET'])
def info(nome_arquivo):
    try:
        data = get_info_by_filename(nome_arquivo)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rota pra verificar se imagem existe no bucket MinIO
@app.route('/api/search/buscar-imagem/<nome_arquivo>', methods=['GET'])
def buscar_imagem(nome_arquivo):
    try:
        stat = minio_client.stat_object(bucket_name, nome_arquivo)
        return jsonify({
            "mensagem": f"Imagem '{nome_arquivo}' encontrada no bucket '{bucket_name}'.",
            "tamanho_bytes": stat.size,
            "ultima_modificacao": stat.last_modified.isoformat()
        }), 200
    except S3Error as e:
        if e.code == "NoSuchKey":
            return jsonify({"erro": f"Imagem '{nome_arquivo}' não encontrada no bucket '{bucket_name}'."}), 404
        else:
            return jsonify({"erro": "Erro ao acessar o MinIO", "detalhes": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
