# ========================================
# 📦 IMPORTS
# ========================================

import requests
from vectorial_db import query_chromadb

# Import agent components (created in agent.py)
from agent import agent_executor, parser, modelResponse


# ========================================
# 🔗 FUNCTION TO CALL LOCAL OLLAMA LLM (RAW)
# ========================================

def generate_text_section(prompt: str, model: str = "mistral", temperature: float = 0.7, max_tokens: int = 512) -> str:
    """
    Query a local Ollama model to generate a report section (raw text only).

    Parameters:
    - prompt (str): The input prompt for the LLM
    - model (str): Ollama model name (e.g. 'mistral', 'deepseek-coder')
    - temperature (float): Controls creativity
    - max_tokens (int): Maximum number of tokens in the response

    Returns:
    - A generated text string
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
        raise Exception(f"Error during generation: {response.text}")


# ========================================
# 🤖 SIMPLE PIPELINE: RETRIEVAL + RAW LLM
# ========================================

def generate_section_from_documents(prompt: str, model: str = "mistral", n_results: int = 5) -> str:
    """
    Combines document retrieval and LLM generation (without agent, returns plain text).

    Parameters:
    - prompt (str): User question
    - model (str): LLM model name
    - n_results (int): Number of top chunks to retrieve from ChromaDB

    Returns:
    - Generated text from LLM, based on retrieved chunks
    """
    # Step 1: Retrieve relevant chunks from vector DB
    chunk_list = query_chromadb(prompt, n_results=n_results)

    if not chunk_list:
        raise ValueError("⚠️ No relevant documents found in ChromaDB.")

    # Step 2: Build context string from retrieved chunks
    context = "\n\n".join(chunk_list)

    contextual_prompt = (
        f"Use the following information to answer the question:\n\n"
        f"{context}\n\n"
        f"Question: {prompt}\n\n"
        f"Answer:"
    )

    # Step 3: Generate text using local LLM
    answer = generate_text_section(contextual_prompt, model=model)

    return answer


# ========================================
# 🧠 ADVANCED PIPELINE: RETRIEVAL + LANGCHAIN AGENT
# ========================================

def generate_structured_section(query: str, n_results: int = 5) -> modelResponse:
    """
    Retrieves context from ChromaDB and generates a structured ESG section
    using the LangChain agent with tools (charts, tables, etc.).

    Parameters:
    - query (str): User question or request (e.g. "What is the environmental impact?")
    - n_results (int): Number of top chunks to retrieve from ChromaDB

    Returns:
    - modelResponse: Structured output with title, paragraph, graphs, tables, sources
    """
    # Step 1: Retrieve relevant context
    chunk_list = query_chromadb(query, n_results=n_results)

    if not chunk_list:
        raise ValueError("⚠️ No relevant documents found in ChromaDB.")

    context = "\n\n".join(chunk_list)

    # Step 2: Compose full input for the agent
    full_input = {
        "query": query,
        "chat_history": context,
        "agent_scratchpad": ""
    }

    # Step 3: Call the agent
    raw_response = agent_executor.invoke(full_input)

    # Step 4: Parse the response using the output parser
    try:
        output_text = raw_response.get("output", "")
        if isinstance(output_text, list):
            # In some LangChain configs, output is a list of steps
            output_text = output_text[0].get("text", "")

        structured = parser.parse(output_text)
        return structured

    except Exception as e:
        raise ValueError(f"❌ Failed to parse structured output:\n{e}\nRaw output:\n{raw_response}")