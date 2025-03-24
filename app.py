import streamlit as st
import os
import shutil
from parser import parse_pdf

# Titolo dell'app
st.set_page_config(page_title="ESG Agent", layout="wide")
st.title("📄 AI Agent for ESG reporting")

st.markdown("""
This app will allow you to upload one or more PDF files and extract the text from them.
""")

# Crea la cartella per i documenti caricati se non esiste
UPLOAD_FOLDER = "Uploaded documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Upload multiplo dei file
uploaded_files = st.file_uploader("📎  Load one or more file(s)", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    st.success(f"You loaded {len(uploaded_files)} file(s) ✅")

    for uploaded_file in uploaded_files:
        # Salva il file in locale nella cartella /documenti
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(uploaded_file, f)

        # Parsing del file PDF
        nome, estensione, testo_intero, testo_per_pagina = parse_pdf(file_path)

        # Visualizzazione
        with st.expander(f"📘 {nome}{estensione} - {len(testo_per_pagina)} pagine", expanded=False):
            st.markdown(f"**File Name:** `{nome}`")
            st.markdown(f"**Extension:** `{estensione}`")
            st.markdown(f"**Number of pages:** `{len(testo_per_pagina)}`")
            st.markdown("**Extraxted text preview:**")
            st.write(testo_intero[:1000] + "..." if len(testo_intero) > 1000 else testo_intero)
else:
    st.info("Load the file for parsing.")