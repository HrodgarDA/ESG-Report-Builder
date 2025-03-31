# ========================================
# 📦 IMPORT LIBRARIES AND MODULES
# ========================================

import streamlit as st
import os
import shutil

from parser import parse_pdf
from vectorial_db import store_in_chromadb  # ✅ indicizzazione
from generator_ai import generate_section_from_documents  # ✅ retrieval + generazione


# ========================================
# ⚙️ STREAMLIT PAGE CONFIGURATION
# ========================================

st.set_page_config(page_title="ESG Report AI Agent", layout="wide")
st.title("🧠 AI Agent for Sustainability Reporting")


# ========================================
# 📁 FILE UPLOAD SECTION
# ========================================

st.header("📄 Upload your ESG document(s)")
UPLOAD_FOLDER = "Documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

uploaded_files = st.file_uploader(
    label="Upload one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

# Process each uploaded file
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

        # Save the file locally
        with open(file_path, "wb") as f:
            shutil.copyfileobj(uploaded_file, f)

        # Parse the PDF content
        nome, estensione, testo, pagine = parse_pdf(file_path)

        # Index the text chunks into ChromaDB ✅
        store_in_chromadb(nome, estensione, testo)

        # Show preview
        with st.expander(f"📘 {nome}{estensione} ({len(pagine)} pages)", expanded=False):
            st.markdown(f"**File name:** `{nome}`")
            st.markdown("**Text preview:**")
            st.write(testo[:1000] + "..." if len(testo) > 1000 else testo)
else:
    st.info("Please upload at least one file to proceed.")


# ========================================
# ✍️ SECTION GENERATION FORM
# ========================================

st.header("✏️ Generate a report paragraph")

with st.form("form_generation"):
    prompt = st.text_area("Enter your prompt", height=200, placeholder="e.g., Describe the environmental impact of the company")
    modello = st.selectbox("Choose the LLM", options=["mistral", "deepseek-coder"])
    temperatura = st.slider("Creativity (temperature)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
    max_chunks = st.slider("How many document chunks to retrieve?", 1, 10, 5)

    genera = st.form_submit_button("🧠 Generate section")

# When user submits the form
if genera and prompt.strip() != "":
    st.info("Generating your section... ⏳")
    try:
        # Retrieval + generation (RAG pipeline)
        output = generate_section_from_documents(
            prompt=prompt,
            model=modello,
            n_results=max_chunks
        )

        st.success("✅ Section generated successfully!")
        st.markdown("### 📝 Result")
        st.write(output)

    except Exception as e:
        st.error(f"Text generation failed: {str(e)}")