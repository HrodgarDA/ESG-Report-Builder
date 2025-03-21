''' 🔹 Passo 1: Importare le librerie '''

import chromadb  # Importa la libreria ChromaDB
from chromadb.utils import embedding_functions  # Per la generazione di embedding testuali

''' 🔹 Passo 2: Inizializzare il Database '''

# Creiamo un'istanza del client ChromaDB con persistenza su disco
client = chromadb.PersistentClient(path="./chroma_db")

# Creiamo o recuperiamo una collezione di documenti
collection = client.get_or_create_collection(name="report_sostenibilità")

'''  Passo 3: Aggiungere documenti alla collezione '''

# Aggiungiamo un documento alla collezione
collection.add(
    ids=["doc1"],  # ID univoco per il documento
    documents=["Questo è un report ESG che tratta la sostenibilità e l'impatto ambientale di un'azienda."],
    metadatas=[{"source": "Report Aziendale 2024"}]  # Metadati opzionali
)

print("Documento aggiunto con successo!")

'''  Passo 4: Recupero di Informazioni dai Documenti '''
# Eseguiamo una query per trovare documenti rilevanti rispetto a una domanda
query = "sostenibilità aziendale"
results = collection.query(query_texts=[query], n_results=2)

print("Risultati della ricerca:", results)