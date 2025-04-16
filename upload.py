import os
from minio import Minio
from minio.error import S3Error
from config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET

client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # Muda pra True se estiver usando HTTPS
)

folder_path = "imgs"  # Pasta local com as imagens

# Upload dos arquivos
try:
    if client.bucket_exists(MINIO_BUCKET):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                client.fput_object(MINIO_BUCKET, filename, file_path)
                print(f"Arquivo '{filename}' enviado com sucesso para o bucket '{MINIO_BUCKET}'!")
    else:
        print(f"Bucket '{MINIO_BUCKET}' não encontrado.")
except S3Error as e:
    print("Erro ao acessar o MinIO:", e)

# Listar os arquivos do bucket
try:
    if client.bucket_exists(MINIO_BUCKET):
        print(f"\nObjetos no bucket '{MINIO_BUCKET}':")
        for obj in client.list_objects(MINIO_BUCKET):
            print(obj.object_name)
    else:
        print(f"Bucket '{MINIO_BUCKET}' não encontrado.")
except S3Error as e:
    print("Erro ao acessar o MinIO:", e)
