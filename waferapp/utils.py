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

AUDIO_DIR = "audios"
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

client = chromadb.PersistentClient(path="embeddings")
collection = client.get_or_create_collection("mis_docs")

device = "cuda" if torch.cuda.is_available() else "cpu"
embedder = SentenceTransformer("all-MiniLM-L6-v2", device=device)
whisper_model = whisper.load_model("medium", device=device)

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
    
    try:
        query_embedding = embedder.encode([pregunta])[0].tolist()
        resultados = collection.query(query_embeddings=[query_embedding], n_results=top_k)
        
        # Verificar si hay resultados
        if not resultados["documents"] or not resultados["documents"][0]:
            return ""
        
        # Filtrar solo contexto relevante basado en similitud
        contexto_relevante = []
        for doc, distance in zip(resultados["documents"][0], resultados["distances"][0]):
            # Solo incluir si la similitud es suficientemente alta (distancia baja)
            if distance < 0.7:  # Ajusta este umbral según sea necesario
                contexto_relevante.append(doc)
        
        # Si no hay contexto relevante, devolver vacío
        if not contexto_relevante:
            return ""
            
        return "\n".join(contexto_relevante)
    
    except Exception as e:
        print(f"Error en buscar_contexto: {e}")
        return ""


def armar_prompt(contexto, pregunta):
    if contexto.strip():
        return f"""Basándote en la siguiente información relevante, responde la pregunta de manera natural y conversacional:

{contexto}

Pregunta: {pregunta}

Responde de forma clara y directa. Si la información proporcionada no es relevante para la pregunta, simplemente responde la pregunta normalmente sin forzar el uso del contexto."""
    else:
        # Si no hay contexto, responde solo con la pregunta.
        return f"{pregunta}"

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
        "messages": [
            {"role": "system", "content": "Eres un asistente AI experto, amable y directo, responde de forma clara y profesional a todas las preguntas del usuario."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    print(f"🔍 DEBUG - Enviando petición a: {url}")
    print(f"🔍 DEBUG - Prompt: {prompt}")
    print(f"🔍 DEBUG - Data: {data}")

    try:
        respuesta = requests.post(url, headers=headers, json=data, timeout=200)
        print(f"🔍 DEBUG - Status code: {respuesta.status_code}")
        print(f"🔍 DEBUG - Respuesta raw: {respuesta.text}")
        
        if respuesta.status_code == 200:
            resultado = respuesta.json()
            print(f"🔍 DEBUG - JSON resultado: {resultado}")
            
            if "choices" in resultado and resultado["choices"]:
                return resultado["choices"][0]["message"]["content"]
            else:
                return f"Error: respuesta inesperada del servidor LLM: {resultado}"
        else:
            return f"Error HTTP {respuesta.status_code}: {respuesta.text}"
            
    except requests.exceptions.ConnectionError:
        return "Error: No se pudo conectar con el servidor LLM. Verifica que LM Studio esté corriendo en localhost:1234"
    except requests.exceptions.Timeout:
        return "Error: Timeout al conectar con el servidor LLM"
    except Exception as e:
        return f"Error procesando respuesta del LLM: {e}. Respuesta cruda: {respuesta.text if 'respuesta' in locals() else 'No response'}"