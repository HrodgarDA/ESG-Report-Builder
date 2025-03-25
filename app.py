import streamlit as st
import os
import shutil
from parser import parse_pdf
from generator_ai import generate_text_section

# Configurazione pagina
st.set_page_config(page_title="Agente ESG", layout="wide")
st.title("🧠 Agente AI per Report di Sostenibilità")

# -- SEZIONE UPLOAD PDF --
st.header("📄 Carica documenti PDF")
UPLOAD_FOLDER = "documenti"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

uploaded_files = st.file_uploader("Carica uno o più file PDF", type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(uploaded_file, f)
        
        nome, estensione, testo, pagine = parse_pdf(file_path)
        
        with st.expander(f"📘 {nome}{estensione} ({len(pagine)} pagine)", expanded=False):
            st.markdown(f"**Nome file:** `{nome}`")
            st.markdown("**Anteprima del testo estratto:**")
            st.write(testo[:1000] + "..." if len(testo) > 1000 else testo)

else:
    st.info("Carica almeno un file PDF per iniziare.")

# -- SEZIONE GENERAZIONE TESTO CON OLLAMA --
st.header("✏️ Genera sezione del report")

with st.form("form_generazione"):
    prompt = st.text_area("Scrivi qui il prompt per generare una sezione del report", height=200)
    modello = st.selectbox("Scegli il modello da usare", options=["mistral", "deepseek-coder"])
    temperatura = st.slider("Creatività del testo (temperature)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    max_tokens = st.slider("Numero massimo di token generati", 100, 1024, 512)

    genera = st.form_submit_button("🧠 Genera testo")

if genera and prompt.strip() != "":
    st.info("Generazione in corso... ⏳")
    try:
        output = generate_text_section(prompt, model=modello, temperature=temperatura, max_tokens=max_tokens)
        st.success("Testo generato ✅")
        st.markdown("### 📝 Risultato")
        st.write(output)
    except Exception as e:
        st.error(f"Errore nella generazione: {str(e)}")