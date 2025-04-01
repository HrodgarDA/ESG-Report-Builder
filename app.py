# ========================================
# 📦 IMPORT LIBRARIES AND MODULES
# ========================================

import streamlit as st
import os
import shutil

from parser import parse_pdf
from vectorial_db import store_in_chromadb  # ✅ indexing of parsed chunks
from generator_ai import generate_section_from_documents  # ✅ RAG pipeline (retrieval + generation)


# ========================================
# ⚙️ STREAMLIT PAGE CONFIGURATION
# ========================================

st.set_page_config(page_title="ESG Report AI Agent", layout="wide")
st.title("🧠 AI Agent for Sustainability Reporting")


# ========================================
# 🎨 BRAND COLOR SELECTION SECTION (STREAMLIT SIDEBAR)
# ========================================

st.sidebar.header("🎨 Customize Chart Colors")

# Sidebar color pickers — user selects up to 3 custom brand colors
color_1 = st.sidebar.color_picker("Primary color", "#3B82F6")  # blue
color_2 = st.sidebar.color_picker("Secondary color", "#10B981")  # green
color_3 = st.sidebar.color_picker("Accent color", "#F59E0B")  # yellow

# Colors will be used in ESG chart functions
brand_colors = [color_1, color_2, color_3]


# ========================================
# 📁 FILE UPLOAD SECTION (MAIN PAGE BLOCK)
# ========================================

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


# ========================================
# ✍️ REPORT PARAGRAPH GENERATION FORM
# ========================================

st.header("✏️ Generate a report paragraph")

# Prompt + model configuration
with st.form("form_generation"):
    prompt = st.text_area(
        label="Enter your prompt",
        height=200,
        placeholder="e.g., Describe the environmental impact of the company"
    )
    modello = st.selectbox("Choose the LLM", options=["mistral", "deepseek-coder"])
    temperatura = st.slider("Creativity (temperature)", 0.0, 1.0, 0.7, step=0.1)
    max_chunks = st.slider("How many document chunks to retrieve?", 1, 10, 5)

    genera = st.form_submit_button("🧠 Generate section")

# If user submits the form
if genera and prompt.strip() != "":
    st.info("Generating your section... ⏳")
    try:
        # Use RAG pipeline to generate text from indexed documents
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