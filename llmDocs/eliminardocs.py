import chromadb

client = chromadb.PersistentClient(path="embeddings")
collection = client.get_or_create_collection("mis_docs")

# Obtén todos los IDs
docs = collection.get()
ids = docs["ids"]

if ids:
    collection.delete(ids=ids)
    print("¡Colección vaciada!")
else:
    print("La colección ya está vacía.")