import os
import chromadb
from sentence_transformers import SentenceTransformer
from utils import leer_documento, chunk_text
import torch  # Agrega esto para detectar GPU

def cargar_documentos_y_chunks(ruta, max_length=350, overlap=50):
    docs = []
    for archivo in os.listdir(ruta):
        path = os.path.join(ruta, archivo)
        if archivo.endswith((".txt", ".pdf")):
            contenido = leer_documento(path)
            print(f"==== {archivo} ====")
            for idx, chunk in enumerate(chunk_text(contenido, max_length, overlap)):
                docs.append((f"{archivo}_chunk{idx}", chunk))
    return docs

def indexar_documentos():
    client = chromadb.PersistentClient(path="embeddings")
    collection = client.get_or_create_collection("mis_docs")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    documentos = cargar_documentos_y_chunks("data")
    for nombre, chunk in documentos:
        embedding = embedder.encode([chunk])[0].tolist()
        collection.add(documents=[chunk], embeddings=[embedding], ids=[nombre])

    print("✔ Documentos indexados en ChromaDB por chunks.")

if __name__ == "__main__":
    indexar_documentos()