# ============================================
# 📦 IMPORT LIBRARIES AND MODULES
# ============================================

import streamlit as st
import os
import shutil

from parser import parse_pdf
from vectorial_db import store_in_chromadb  # ✅ indexing of parsed chunks
from generator_ai import generate_section_from_documents  # ✅ RAG pipeline (retrieval + generation)


# ============================================
# ⚙️ STREAMLIT PAGE CONFIGURATION
# ============================================
st.set_page_config(page_title="ESG Report AI Agent", layout="wide")
st.title("🧠 AI Agent for Sustainability Reporting")


# ============================================
# 📑 SIDEBAR MENU: BRAND COLORS + RESET BUTTON
# ============================================

with st.sidebar:
    st.header("⚙️ Settings")

    st.subheader("🎨 Brand Colors")
    color_1 = st.color_picker("Primary color", "#3B82F6")  # blue
    color_2 = st.color_picker("Secondary color", "#10B981")  # green
    color_3 = st.color_picker("Accent color", "#F59E0B")  # yellow
    brand_colors = [color_1, color_2, color_3]

    st.subheader("🧹 Memory Management")
    if st.button("🗑️ Reset LLM Memory / Clear ChromaDB"):
        if os.path.exists("chroma.sqlite3"):
            os.remove("chroma.sqlite3")
            st.success("Agent's memory has been reset.")
        else:
            st.warning("No memory found to clear.")


# ============================================
# 📁 FILE UPLOAD SECTION (MAIN PAGE BLOCK)
# ============================================

st.header("📄 Upload your ESG document(s)")

# Folder where uploaded documents are saved
UPLOAD_FOLDER = "Documents"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

uploaded_files = st.file_uploader(
    label="Upload one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

# Parses each uploaded file
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

        # Save uploaded file locally
        with open(file_path, "wb") as f:
            shutil.copyfileobj(uploaded_file, f)

        # Extract text and metadata from the PDF
        nome, estensione, testo, pagine = parse_pdf(file_path)

        # ✅ Save extracted content in ChromaDB vector store
        store_in_chromadb(nome, estensione, testo)

        # Expandable preview of document content
        with st.expander(f"📘 {nome}{estensione} ({len(pagine)} pages)", expanded=False):
            st.markdown(f"**File name:** `{nome}`")
            st.markdown("**Text preview:**")
            st.write(testo[:1000] + "..." if len(testo) > 1000 else testo)

else:
    st.info("Please upload at least one file to proceed.")


# ============================================
# ✍️ REPORT PARAGRAPH GENERATION FORM
# ============================================

st.header("✏️ Generate a report paragraph")

# Prompt + model configuration
with st.form("form_generation"):
    prompt = st.text_area(
        label="Enter your prompt",
        height=200,
        placeholder="e.g., Describe the environmental impact of the company"
    )
    modello = st.selectbox("Choose the LLM", options=["mistral", "deepseek-coder"])
    genera = st.form_submit_button("🧠 Generate section")

# If user submits the form
if genera and prompt.strip() != "":
    st.info("Generating your section... ⏳")
    try:
        # Use RAG pipeline to generate text from indexed documents
        output = generate_section_from_documents(
            prompt=prompt,
            model=modello,
            n_results=6  # fixed max_chunks
        )

        st.success("✅ Section generated successfully!")
        st.markdown("### 📝 Result")
        st.write(output)

    except Exception as e:
        st.error(f"Text generation failed: {str(e)}")