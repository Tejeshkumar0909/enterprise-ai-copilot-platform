# Build This Project From Scratch With AI

This guide is for learning, not copying. Use AI as a pair-programmer: ask it to explain, generate small files, review your code, and quiz you.

## Goal
Build a portfolio-safe Enterprise AI Copilot Platform from zero: FastAPI + local RAG + simple agent routing + tests + Docker + CI.

## Free tools only
- Python 3.11+
- VS Code or any editor
- Git + GitHub
- FastAPI, scikit-learn, pytest, httpx
- Optional AI helpers: ChatGPT free tier, Gemini free tier, Claude free tier, Cursor free tier, or Hermes here

## Recommended AI prompt style
Use prompts like this, one small step at a time:

```text
Act as my senior AI engineer mentor. I am building a FastAPI RAG copilot from scratch for my portfolio. Do not dump the whole solution. Teach me step-by-step. First explain the file structure, then give me only the next file to create, tests to run, and what I should understand before moving on.
```

## Phase 0 — Create the repo locally

```bash
mkdir enterprise-ai-copilot-platform
cd enterprise-ai-copilot-platform
git init -b main
python3 -m venv .venv
. .venv/bin/activate
```

Create `requirements.txt`:

```txt
fastapi==0.115.6
uvicorn[standard]==0.34.0
pydantic==2.10.4
scikit-learn==1.5.2
numpy==2.1.3
pytest==8.3.4
httpx==0.28.1
```

Install:

```bash
pip install -r requirements.txt
```

## Phase 1 — Understand the architecture

Ask AI:

```text
Explain RAG in simple terms using this architecture: sample docs -> ingestion -> local index -> retriever -> agent router -> grounded answer with citations. Give me a mental model and interview explanation.
```

You should be able to explain:
- What retrieval means
- Why citations reduce hallucinations
- Why local/sample data is safer for GitHub
- What FastAPI does

## Phase 2 — Build the retriever first

Create:
- `app/retriever.py`
- `sample_docs/copilot_architecture.md`
- `sample_docs/evaluation.md`
- `sample_docs/deployment.md`

Ask AI:

```text
Help me implement a simple Python LocalKnowledgeBase using TfidfVectorizer and cosine_similarity. I want a Document dataclass, save/load JSON, and search(query, top_k). Explain every method.
```

Verify manually in Python:

```bash
python
```

```python
from app.ingest import build_index
from app.retriever import LocalKnowledgeBase
build_index('sample_docs', 'data/index.json')
kb = LocalKnowledgeBase.from_path('data/index.json')
kb.search('hallucinations citations grounding', top_k=1)
```

## Phase 3 — Add ingestion CLI

Create `app/ingest.py`.

Ask AI:

```text
Write a small ingestion CLI that reads markdown files from sample_docs, creates Document objects, and saves a JSON index. Keep it beginner-friendly and explain argparse.
```

Run:

```bash
python -m app.ingest --input sample_docs --store data/index.json
```

Expected:

```text
indexed 3 documents -> data/index.json
```

## Phase 4 — Add agent routing

Create `app/agent.py`.

Ask AI:

```text
Help me build a tiny agent router. It should classify questions into qa, summarize, or search using keywords, then call the retriever and compose a grounded answer with citations.
```

Understand:
- This is not a heavy LangGraph agent yet.
- It is an explainable portfolio-safe approximation.
- Later you can replace it with LangGraph nodes.

## Phase 5 — Add FastAPI

Create:
- `app/models.py`
- `app/main.py`

Ask AI:

```text
Help me expose my local RAG copilot with FastAPI. I need /health, /ingest, and /query endpoints. Use Pydantic request/response models and explain why response_model matters.
```

Run:

```bash
uvicorn app.main:app --reload
```

Test:

```bash
curl -X POST http://127.0.0.1:8000/query \
  -H 'Content-Type: application/json' \
  -d '{"question":"How does the copilot reduce hallucinations?","top_k":2}'
```

## Phase 6 — Tests

Create `tests/test_copilot.py`.

Ask AI:

```text
Help me write pytest tests for intent routing, retrieval relevance, and the FastAPI /query endpoint. Explain what each assert proves.
```

Run:

```bash
pytest -q
```

Expected:

```text
3 passed
```

## Phase 7 — Docker + CI

Create:
- `Dockerfile`
- `.github/workflows/ci.yml`

Ask AI:

```text
Help me containerize this FastAPI project and add GitHub Actions CI that installs requirements and runs pytest. Explain each line.
```

## Phase 8 — Upgrade ideas after you understand the base

Only after the simple version works:
- Replace TF-IDF with FAISS + sentence-transformers
- Add LangGraph node flow
- Add Streamlit UI
- Add evaluation dataset with golden answers
- Add Docker Compose

## Interview explanation

Use this:

```text
I built a portfolio-safe enterprise AI copilot demo with FastAPI and local RAG. It indexes synthetic markdown documents, retrieves relevant passages with vector-style TF-IDF similarity, routes user intent into QA/search/summarization flows, and returns grounded answers with citations. I added pytest coverage, Docker packaging, and GitHub Actions CI. The repo avoids paid APIs and confidential data, but the architecture is designed so FAISS, Hugging Face embeddings, LangGraph, or cloud LLMs can be added later.
```
