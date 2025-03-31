# ========================================
# ✅ FILE DI TEST AUTOMATICO PER CHROMADB
# ========================================

import chromadb
from sentence_transformers import SentenceTransformer

# Modello di embedding (lo stesso usato per l'indicizzazione)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ========================================
# 🔧 PARAMETRI DEL TEST
# ========================================

COLLECTION_NAME = "report_sostenibilita"
DB_PATH = "./"
TEST_QUERY = "Descrivi l'impatto ambientale dell’azienda"
N_RESULTS = 3


# ========================================
# 🔍 FUNZIONE DI TEST DEL DATABASE
# ========================================

def test_chromadb():
    try:
        # 1. Connessione al database
        print("🔗 Connessione a ChromaDB...")
        client = chromadb.PersistentClient(path=DB_PATH)
        collection = client.get_or_create_collection(name=COLLECTION_NAME)
        print("✅ Connessione riuscita")

        # 2. Verifica della presenza di documenti indicizzati
        print("\n📦 Verifica dei documenti nella collezione...")
        count = collection.count()
        print(f"🔢 Documenti indicizzati: {count}")
        if count == 0:
            print("⚠️ Nessun documento trovato. Verifica che store_in_chromadb sia stato chiamato.")
            return

        # 3. Query di test
        print("\n🧠 Esecuzione di una query di esempio...")
        query_embedding = embedder.encode([TEST_QUERY]).tolist()[0]
        results = collection.query(query_embeddings=[query_embedding], n_results=N_RESULTS)

        documents = results.get("documents", [[]])[0]

        if not documents:
            print("⚠️ Nessun risultato rilevante trovato.")
        else:
            print(f"✅ Trovati {len(documents)} chunk rilevanti:")
            for i, doc in enumerate(documents):
                print(f"\n--- Chunk {i+1} ---\n{doc[:300]}{'...' if len(doc) > 300 else ''}")

    except Exception as e:
        print("❌ Errore nel test:")
        print(e)


# ========================================
# ▶️ AVVIO TEST
# ========================================

if __name__ == "__main__":
    print("🚀 Avvio test automatico ChromaDB\n")
    test_chromadb()