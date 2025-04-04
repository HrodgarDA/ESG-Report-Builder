# ===============================
# agent.py — ESG Section Generator Agent (Local Ollama Version)
# ===============================

# 📦 Imports
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.llms import ollama

# Import available tools for chart and table generation
from tools import plot_bar_chart, plot_line_chart, plot_pie_chart, plot_table

# ============================================
# 🧠 STEP 1: Define the Output Schema using Pydantic
# ============================================

class modelResponse(BaseModel):
    """
    Output model for generating ESG report sections.
    """
    paragraph_title: str
    paragraph: str
    graphs: str
    tables: str
    sources: list[str]

# ============================================
# 🔍 STEP 2: Create Output Parser
# ============================================

parser = PydanticOutputParser(pydantic_object=modelResponse)

# ============================================
# 📝 STEP 3: Define Prompt Template
# ============================================

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful assistant that generates sections of environmental, social, and governance (ESG) reports based on user input and document context.
            Proceed with the generation using relevant information retrieved from the database.
            Make sure to include all necessary insights and calculations.
            Use available tools to create graphs and tables using the user's selected color palette.
            Wrap the output using the following format:\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# ============================================
# ⚙️ STEP 4: Initialize the Local Ollama Model
# ============================================

try:
    llm = ollama(model="mistral", temperature=0.3, max_tokens=2048)
except Exception as e:
    raise RuntimeError("❌ Could not initialize the Ollama model. Make sure Ollama is running and the model is available.") from e

# ============================================
# 🛠️ STEP 5: Define Available Tools for the Agent
# ============================================

tools = [plot_bar_chart, plot_line_chart, plot_pie_chart, plot_table]

# ============================================
# 🤖 STEP 6: Create the Tool-Calling Agent
# ============================================

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

# ============================================
# 🚀 STEP 7: Create the Agent Executor
# ============================================

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    return_intermediate_steps=True
)

# ============================================
# 🧩 STEP 8: Expose Agent Components for Import
# ============================================

__all__ = ["agent_executor", "parser", "modelResponse"]