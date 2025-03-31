# ========================================
# 📦 IMPORT DELLE LIBRERIE
# ========================================

import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


# ========================================
# ⚙️ INIZIALIZZAZIONE DEL MODELLO DI EMBEDDING
# ========================================

# Carichiamo il modello di embedding locale (gratuito, compatibile con CPU)
embedder = SentenceTransformer("all-MiniLM-L6-v2")


# ========================================
# 📥 FUNZIONE DI INDICIZZAZIONE IN CHROMADB
# ========================================

def store_in_chromadb(nome, estensione, testo, chunk_size=500, overlap=50):
    """
    Divide il testo in chunk, genera embedding locali e li salva in ChromaDB.

    Parametri:
    - nome (str): nome del file sorgente
    - estensione (str): formato file (.pdf, .txt, ecc.)
    - testo (str): testo completo del documento
    - chunk_size (int): numero massimo di caratteri per chunk
    - overlap (int): sovrapposizione tra chunk consecutivi

    Output:
    - Salva i chunk indicizzati in una collezione ChromaDB
    """
    print(f"📥 Indicizzazione in corso per: {nome}{estensione}")
    # 1. Creazione dello splitter per suddividere il testo
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", " "]  # priorità di separazione
    )

    # 2. Suddivisione in chunk
    chunks = splitter.split_text(testo)

    # 3. Calcolo degli embedding locali
    embeddings = embedder.encode(chunks).tolist()

    # 4. Inizializzazione del database vettoriale ChromaDB
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="report_sostenibilita")

    # 5. Creazione degli ID e metadati per ogni chunk
    ids = [f"{nome}_{i}" for i in range(len(chunks))]
    metadatas = [{"origine": nome, "estensione": estensione, "chunk": i} for i in range(len(chunks))]

    # 6. Aggiunta alla collezione
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"✅ Indicizzati {len(chunks)} chunk del documento '{nome}{estensione}' usando embedding locali.")
    

# ========================================
# 🔍 FUNZIONE DI QUERY IN CHROMADB
# ========================================

def query_chromadb(prompt, n_results=5):
    """
    Cerca i chunk più rilevanti in ChromaDB rispetto a un prompt.

    Parametri:
    - prompt (str): domanda o tema da cercare
    - n_results (int): numero di risultati da restituire

    Ritorna:
    - List[str]: lista dei chunk di testo più rilevanti
    """

    # 1. Calcolo dell'embedding del prompt
    query_embedding = embedder.encode([prompt]).tolist()[0]

    # 2. Inizializzazione del client e recupero collezione
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="report_sostenibilita")

    # 3. Ricerca dei documenti più simili semanticamente
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    # 4. Estrazione dei documenti rilevanti
    documenti = results["documents"][0]  # lista di stringhe
    return documenti