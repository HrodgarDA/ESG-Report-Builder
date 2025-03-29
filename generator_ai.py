# ========================================
# 📦 IMPORT
# ========================================

from vectorial_db import query_chromadb
import requests

# ========================================
# 🔗 FUNZIONE DI CHIAMATA A OLLAMA (LLM LOCALE)
# ========================================

def generate_text_section(prompt, model="mistral", temperature=0.7, max_tokens=512):
    """
    Interroga un modello Ollama locale per generare una sezione del report.

    Parametri:
    - prompt (str): istruzione da inviare al modello
    - model (str): nome del modello Ollama (es. 'mistral', 'deepseek-coder')
    - temperature (float): creatività del testo
    - max_tokens (int): limite massimo di token

    Ritorna:
    - testo generato (str)
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": False
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        raise Exception(f"Errore nella generazione: {response.text}")


# ========================================
# 🤖 AGENTE: GENERAZIONE BASATA SU DOCUMENTI
# ========================================

def generate_section_from_documents(prompt, model="mistral", n_results=5):
    """
    Combina retrieval + generazione: interroga ChromaDB e genera una sezione di report usando LLM.

    Parametri:
    - prompt (str): richiesta dell'utente
    - model (str): modello Ollama da utilizzare
    - n_results (int): numero di chunk da recuperare da ChromaDB

    Ritorna:
    - testo generato dal modello, basato sui chunk recuperati
    """

    # 1. Recupero dei chunk rilevanti dal database
    chunk_list = query_chromadb(prompt, n_results=n_results)

    if not chunk_list:
        raise ValueError("⚠️ Nessun documento rilevante trovato in ChromaDB.")

    # 2. Costruzione del contesto testuale (contesto + domanda)
    context = "\n\n".join(chunk_list)

    prompt_con_contesto = (
        f"Usa le seguenti informazioni per rispondere alla domanda:\n\n"
        f"{context}\n\n"
        f"Domanda: {prompt}\n\n"
        f"Risposta:"
    )

    # 3. Generazione del testo tramite modello LLM
    risposta = generate_text_section(prompt_con_contesto, model=model)

    return risposta