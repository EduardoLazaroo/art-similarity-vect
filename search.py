from flask import Flask, jsonify
from flask_cors import CORS
from minio import Minio
from minio.error import S3Error
from config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET

app = Flask(__name__)
CORS(app)  # Libera geral o CORS

# Cliente MinIO usando config
client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # Altere pra True se for HTTPS
)

# Rota que busca a imagem no MinIO
@app.route('/api/search/buscar-imagem/<nome_arquivo>', methods=['GET'])
def buscar_imagem(nome_arquivo):
    try:
        stat = client.stat_object(MINIO_BUCKET, nome_arquivo)
        return jsonify({
            "mensagem": f"Imagem '{nome_arquivo}' encontrada no bucket '{MINIO_BUCKET}'.",
            "tamanho_bytes": stat.size,
            "ultima_modificacao": stat.last_modified.isoformat()
        }), 200
    except S3Error as e:
        if e.code == "NoSuchKey":
            return jsonify({"erro": f"Imagem '{nome_arquivo}' não encontrada no bucket '{MINIO_BUCKET}'."}), 404
        else:
            return jsonify({"erro": "Erro ao acessar o MinIO", "detalhes": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
