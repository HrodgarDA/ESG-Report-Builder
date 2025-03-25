# generator_ai.py

import requests

def generate_text_section(prompt, model="mistral", temperature=0.7, max_tokens=512):
    """
    Interroga un modello Ollama locale per generare una sezione del report.

    Parametri:
    - prompt (str): istruzione da inviare al modello
    - model (str): nome del modello Ollama (es. 'mistral', 'deepseek-coder')
    - temperature (float): livello di creatività del testo
    - max_tokens (int): massimo numero di token da generare

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
        raise Exception(f"Errore durante la richiesta a Ollama: {response.text}")