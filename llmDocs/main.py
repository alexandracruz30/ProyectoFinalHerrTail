import chromadb
from sentence_transformers import SentenceTransformer
import requests
import torch

def buscar_contexto(pregunta, top_k=3):
    client = chromadb.PersistentClient(path="embeddings")
    collection = client.get_or_create_collection("mis_docs")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    embedder = SentenceTransformer("all-MiniLM-L6-v2", device=device)
    query_embedding = embedder.encode([pregunta])[0].tolist()
    resultados = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return "\n".join(resultados["documents"][0])

def consultar_llm(pregunta):
    contexto = buscar_contexto(pregunta)
    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    if contexto.strip():
        prompt = f"""Usa la siguiente información para responder:
{contexto}

Pregunta: {pregunta}
Respuesta:"""
    else:
        prompt = f"{pregunta}\nRespuesta:"

    data = {
        #"model": "llama-3.1",
        "model": "phi-3-mini-4k-instruct",
        "role": "system",
        "content": "Eres un asistente AI experto, amable y directo, responde de forma clara y profesional a todas las preguntas del usuario.",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    respuesta = requests.post(url, headers=headers, json=data)
    return respuesta.json()["choices"][0]["message"]["content"]