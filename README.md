📁 agente_esg/

│
├── 📄 app.py                  # App Streamlit (entry point)

├── 📄 parser.py               # PDF Parsing 

├── 📄 chroma_db.py            # Indicization, embedding e query

├── 📄 generator_ai.py         # Prompt + text generation

├── 📄 visual_utils.py         # Graphs and utilis

├── 📄 report_pdf.py           # Composition and PDF generation

├── 📁 documents/              # Directory for updated documents

├── 📁 Requirements/           # Envoironment requirements

└── 📁 output/                 # Generated report (PDF)

_______________________________________________________________________________________________________________

✅ What This Project Can Do So Far:

🧠 AI Agent for ESG Reporting
A local AI-powered assistant for automated ESG reporting

⸻

🎯 Main Objective

Allow users (e.g., sustainability officers or analysts) to:
	•	Upload one or more company documents (PDFs like sustainability reports, policies, etc.)
	•	Ask questions or give prompts in natural language
	•	Automatically generate high-quality report sections using a local LLM
	•	Ensure that generated text is grounded in the actual content of the uploaded documents
	•	Run fully offline and for free, without relying on external APIs (OpenAI, Hugging Face, etc.)

⸻

🧩 Current Features — Fully Implemented

📄 1. PDF Upload and Parsing
	•	Upload multiple PDF documents via a simple web interface (Streamlit)
	•	Extract full text and show a short preview of each file
	•	Organize uploaded files locally in a designated folder

⸻

🧠 2. Semantic Indexing of Document Content
	•	Documents are split into manageable chunks using LangChain
	•	Each chunk is converted to semantic vectors (embeddings) using sentence-transformers (MiniLM) locally
	•	The chunks and their vectors are saved in ChromaDB, a local vector store

⸻

🔍 3. Smart Retrieval from ChromaDB
	•	When the user enters a prompt, it’s converted into a query vector
	•	The app retrieves the most relevant document chunks from ChromaDB using vector similarity
	•	These chunks become the context for the LLM to generate a response

⸻

✍️ 4. Report Section Generation via Local LLM (Ollama)
	•	Supports local models like Mistral and Deepseek-Coder using Ollama
	•	Generates coherent, readable text based on the context retrieved
	•	Works with no internet connection and no token cost

⸻

🎨 5. Brand Color Customization
	•	Users can pick 3 colors (primary, secondary, accent) via a sidebar interface
	•	These colors are stored and will be used in ESG visualizations (charts, tables)

⸻

🧹 6. Agent Memory Reset
	•	A sidebar button lets the user delete the ChromaDB database (chroma.sqlite3)
	•	Useful for resetting the session or starting with a new document set

____________________________________________________________________________________________________________

Components:

Python  - Main development language
Streamlit - Web interface
PyMuPDF (fitz) - PDF parsing
LangChain - Text chunking
ChromaDB - Vector database
sentence-transformers - Local embeddings
Ollama - Local LLM runner
Matplotlib / Seaborn / Pandas - For ESG charts (ready to use)
