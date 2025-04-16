import os
import numpy as np
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.models import Model
from config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME, IMAGES_FOLDER, BATCH_SIZE

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
base_model = EfficientNetB0(weights="imagenet", include_top=False, pooling="avg")

# ======= INICIALIZA COLLECTION =======
VECTOR_SIZE = base_model.output_shape[1]
try:
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )
    print(f"✅ Collection '{COLLECTION_NAME}' criada.")
except Exception as e:
    print(f"❌ Erro criando collection: {repr(e)}")
    exit()

# ======= CARREGA IMAGENS =======
image_files = sorted([
    f for f in os.listdir(IMAGES_FOLDER)
    if f.lower().endswith((".png", ".jpg", ".jpeg"))
])

# ======= PROCESSA E ENVIA EM LOTES =======
batch = []

for idx, filename in enumerate(image_files):
    try:
        path = os.path.join(IMAGES_FOLDER, filename)
        img = keras_image.load_img(path, target_size=(224, 224))
        x = keras_image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        vector = base_model.predict(x, verbose=0)[0].tolist()
        payload = {"nome_arquivo": filename}

        point = PointStruct(id=idx, vector=vector, payload=payload)
        batch.append(point)

        print(f"📸 Vetorizado: {filename}")

        if len(batch) >= BATCH_SIZE:
            client.upsert(collection_name=COLLECTION_NAME, points=batch)
            print(f"🚀 Enviado batch com {len(batch)} imagens.")
            batch = []

    except Exception as e:
        print(f"❌ Erro com '{filename}': {repr(e)}")

# Envia o que sobrou
if batch:
    try:
        client.upsert(collection_name=COLLECTION_NAME, points=batch)
        print(f"🚀 Enviado último batch com {len(batch)} imagens.")
    except Exception as e:
        print(f"❌ Erro no último upsert: {repr(e)}")
