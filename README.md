# Industrial Equipment Maintenance Agent
### Multi-Agent LangGraph System for Industrial Fault Diagnosis

A production-grade multi-agent AI system built with LangGraph that diagnoses industrial equipment faults, retrieves relevant maintenance knowledge, and generates structured work orders — with a human-in-the-loop approval checkpoint.

---

## What It Does

An engineer enters an equipment ID and describes a fault. Six specialized AI agents collaborate to investigate, diagnose, and produce a maintenance work order:

1. **Planner Agent** — breaks down the investigation into structured tasks
2. **Data Retrieval Agent** — fetches equipment maintenance history from database
3. **Diagnostic Agent** — reasons through the fault using LLM + historical data
4. **Knowledge Agent** — retrieves relevant sections from maintenance manuals using RAG
5. **HITL Checkpoint** — pauses for human engineer review and approval
6. **Report Writer Agent** — generates structured Excel and JSON work order

---

## Key Features

- Multi-agent orchestration using LangGraph StateGraph
- Human-in-the-loop with interrupt() and resume — engineer can reject and the system rediagnoses
- RAG pipeline using FAISS vector store and Cohere embeddings
- Structured output — Excel and JSON work orders with confidence scores
- Local LLM using Ollama (Llama 3) — works completely offline
- Streamlit web interface

---

## Tech Stack

- **LangGraph** — multi-agent graph orchestration
- **LangChain** — LLM framework
- **Ollama + Llama 3** — local LLM inference
- **Cohere** — embeddings for RAG
- **FAISS** — vector store for document search
- **SQLite** — equipment maintenance database
- **Streamlit** — web interface
- **Python 3.13**

---

## Project Structure

├── agents/          # Six specialized AI agents
├── graph/           # LangGraph state and graph builder
├── tools/           # Equipment database, RAG, report generator
├── data/            # SQLite database and maintenance manuals
├── ui/              # Streamlit web interface
├── output/          # Generated work orders
└── config.py        # Central configuration

---

## Setup

1. Clone the repository
2. Create virtual environment and activate it
3. Install dependencies
4. Add your Cohere API key to .env
5. Make sure Ollama is running with Llama 3

```bash
git clone https://github.com/SatvikSPandey/siemens-maintenance-agent.git
cd siemens-maintenance-agent
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run ui/app.py
```

---

## How It Works

The system uses LangGraph's StateGraph where all agents share a single typed state object. Each agent reads what it needs, does its job, and writes results back. The supervisor routes between agents using conditional edges. The HITL checkpoint uses LangGraph's interrupt() to pause execution and wait for human input before generating the final report.

---

Built by Satvik Pandey — AI Engineer | Python Developer | LangGraph
Targeted at industrial automation and manufacturing AI roles.

