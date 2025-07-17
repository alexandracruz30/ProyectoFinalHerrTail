import chromadb

client = chromadb.PersistentClient(path="embeddings")
collection = client.get_or_create_collection("mis_docs")

# Recupera todos los documentos (puedes limitar el número con limit=...)
docs = collection.get()
print("IDs en la colección:", docs["ids"])