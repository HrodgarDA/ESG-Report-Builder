# ========================================
# 📦 LIBRARY IMPORTS
# ========================================

import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


# ========================================
# ⚙️ INITIALIZE EMBEDDING MODEL
# ========================================

# Loads a local, CPU-compatible embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")


# ========================================
# 📥 STORE DOCUMENT CHUNKS INTO CHROMADB
# ========================================

def store_in_chromadb(nome, estensione, testo, chunk_size=500, overlap=50):
    """
    Splits the text into chunks, generates local embeddings, and stores them in ChromaDB.

    Parameters:
    - nome (str): source file name (no extension)
    - estensione (str): file extension (.pdf, .txt, etc.)
    - testo (str): full text extracted from document
    - chunk_size (int): max characters per chunk
    - overlap (int): character overlap between chunks

    Output:
    - Indexed chunks saved into ChromaDB collection
    """

    print(f"📥 Indexing started for: {nome}{estensione}")

    # 1. Text splitting configuration
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", " "]  # priority of split: paragraph > line > sentence > word
    )

    # 2. Split text into chunks
    chunks = splitter.split_text(testo)

    # ❗ Skip empty documents or failed parsing
    if not chunks:
        print(f"⚠️ Skipped {nome}{estensione}: no content extracted.")
        return

    # 3. Generate embeddings for each chunk
    embeddings = embedder.encode(chunks).tolist()

    # ❗ Safety check to avoid crash with empty embeddings
    if not embeddings:
        print(f"⚠️ Skipped {nome}{estensione}: empty embeddings list.")
        return

    # 4. Initialize ChromaDB client and collection
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="report_sostenibilita")

    # 5. Generate unique IDs and metadata
    ids = [f"{nome}_{i}" for i in range(len(chunks))]
    metadatas = [{"origine": nome, "estensione": estensione, "chunk": i} for i in range(len(chunks))]

    # 6. Add records to the collection
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"✅ Indexed {len(chunks)} chunks from '{nome}{estensione}' using local embeddings.")


# ========================================
# 🔍 QUERY CHROMADB FOR RELEVANT CHUNKS
# ========================================

def query_chromadb(prompt, n_results=20):
    """
    Searches for the most relevant document chunks in ChromaDB based on a user prompt.

    Parameters:
    - prompt (str): user input prompt/question
    - n_results (int): number of top matching chunks to retrieve

    Returns:
    - List[str]: list of retrieved text chunks
    """

    # 1. Generate embedding for the user prompt
    query_embedding = embedder.encode([prompt]).tolist()[0]

    # 2. Connect to ChromaDB and access the collection
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection(name="report_sostenibilita")

    # 3. Perform vector search
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    # 4. Return retrieved text chunks
    return results.get("documents", [[]])[0]