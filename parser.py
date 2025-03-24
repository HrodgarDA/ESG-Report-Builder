import fitz # PyMuPDF
import os

def parse_pdf(file_path):
    """
    Estrae il testo da un file PDF pagina per pagina, restituendo anche nome e estensione del file.
    
    Parametri:
    - file_path (str): percorso al file PDF
    
    Ritorna:
    - nome_origine (str): nome del file (senza estensione)
    - estensione (str): estensione del file originale
    - testo_intero (str): tutto il testo estratto, unito
    - testo_per_pagina (list): lista di testi divisi per pagina
    """
    # Recupera nome file ed estensione
    base_name = os.path.basename(file_path)
    nome_origine, estensione = os.path.splitext(base_name)

    # Apriamo il file PDF
    doc = fitz.open(file_path)

    testo_per_pagina = []

    # Estraiamo il testo da ogni pagina
    for page_num, page in enumerate(doc):
        testo = page.get_text()
        testo_pulito = testo.strip()
        testo_per_pagina.append(testo_pulito)

        print(f"[{nome_origine} - Pagina {page_num + 1}] Estratti {len(testo_pulito)} caratteri")

    # Unione di tutte le pagine in una stringa unica
    testo_intero = "\n\n".join(testo_per_pagina)

    return nome_origine, estensione, testo_intero, testo_per_pagina


def parse_folder(folder_path):
    """
    Estrae il testo da tutti i file PDF in una cartella.
    
    Parametri:
    - folder_path (str): percorso della cartella
    
    Ritorna:
    - lista_risultati (list): lista di tuple (nome_origine, estensione, testo_intero, testo_per_pagina)
    """
    lista_risultati = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(folder_path, file_name)

            # Chiamiamo la funzione di parsing per ogni PDF
            risultato = parse_pdf(file_path)

            # Aggiungiamo il risultato alla lista
            lista_risultati.append(risultato)

    return lista_risultati