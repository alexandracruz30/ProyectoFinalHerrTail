import os
import requests
import whisper
import chromadb
from sentence_transformers import SentenceTransformer
import noisereduce as nr
import soundfile as sf
import numpy as np
import torch
import pyttsx3
import PyPDF2

AUDIO_DIR = "audios"
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

client = chromadb.PersistentClient(path="embeddings")
collection = client.get_or_create_collection("mis_docs")

device = "cuda" if torch.cuda.is_available() else "cpu"
embedder = SentenceTransformer("all-MiniLM-L6-v2", device=device)
whisper_model = whisper.load_model("medium", device=device)

def leer_documento(ruta_archivo):
    """Lee documentos PDF y TXT"""
    try:
        if ruta_archivo.endswith('.pdf'):
            with open(ruta_archivo, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                texto = ""
                for page in pdf_reader.pages:
                    texto += page.extract_text() + "\n"
                return texto
        elif ruta_archivo.endswith('.txt'):
            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            return ""
    except Exception as e:
        print(f"Error leyendo {ruta_archivo}: {e}")
        return ""

def chunk_text(texto, max_length=350, overlap=50):
    """Divide texto en chunks más pequeños con overlap"""
    if not texto:
        return []
    
    chunks = []
    start = 0
    texto_len = len(texto)
    
    while start < texto_len:
        end = min(start + max_length, texto_len)
        
        # Buscar el final de una oración cerca del límite
        if end < texto_len:
            # Buscar punto, signo de exclamación o interrogación
            for i in range(end, max(start, end - 50), -1):
                if texto[i] in '.!?':
                    end = i + 1
                    break
        
        chunk = texto[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
        
        # Evitar chunks muy pequeños al final
        if start >= texto_len - overlap:
            break
    
    return chunks

def normalizar_audio(input_wav, output_wav):
    data, rate = sf.read(input_wav)
    norm_data = data / np.max(np.abs(data))
    sf.write(output_wav, norm_data, rate)

def limpiar_audio(input_wav, output_wav, noise_clip_seconds=1):
    data, rate = sf.read(input_wav)
    noise_clip = data[:int(rate*noise_clip_seconds)]
    reduced_noise = nr.reduce_noise(y=data, sr=rate, y_noise=noise_clip, stationary=True)
    sf.write(output_wav, reduced_noise, rate)

def transcribir_whisper(wav_path):
    result = whisper_model.transcribe(wav_path, language="es", task="transcribe")
    texto = result["text"].strip()
    return texto

def buscar_contexto(pregunta, top_k=2): #PARA QUE FUNCIONE LLAMA 3.1 TOP_K:3, PARA EL PHI DEBE SER 2
    client = chromadb.PersistentClient(path="embeddings")
    collection = client.get_or_create_collection("mis_docs")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    embedder = SentenceTransformer("all-MiniLM-L6-v2", device=device)
    query_embedding = embedder.encode([pregunta])[0].tolist()
    resultados = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return "\n".join(resultados["documents"][0])


def armar_prompt(contexto, pregunta):
    if contexto.strip():
        return f"""Usa la siguiente información para responder:
{contexto}

Pregunta: {pregunta}
Respuesta:"""
    else:
        # Si no hay contexto, responde solo con la pregunta.
        return f"{pregunta}\nRespuesta:"

def texto_a_audio(texto, output_path):
    engine = pyttsx3.init()
    engine.save_to_file(texto, output_path)
    engine.runAndWait()
    print(f"🔊 Audio guardado en {output_path}")

def consultar_llm(pregunta):
    contexto = buscar_contexto(pregunta)
    prompt = armar_prompt(contexto, pregunta)
    #url = "http://host.docker.internal:1234/v1/chat/completions" #ESTA ES PARA LA DE DOCKER
    url = "http://localhost:1234/v1/chat/completions"  # ESTA SERIA PARA LA PC LOCAL
    headers = {"Content-Type": "application/json"}

    data = {
        "model": "meta-llama-3.1-8b-instruct",
        #"model": "phi-3-mini-4k-instruct",
        "role": "system",
        "content": "Eres un asistente AI experto, amable y directo, responde de forma clara y profesional a todas las preguntas del usuario.",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    respuesta = requests.post(url, headers=headers, json=data)
    try:
        resultado = respuesta.json()
        if "choices" in resultado and resultado["choices"]:
            return resultado["choices"][0]["message"]["content"]
        else:
            return f"Error: respuesta inesperada del servidor LLM: {resultado}"
    except Exception as e:
        return f"Error procesando respuesta del LLM: {e}. Respuesta cruda: {respuesta.text}"