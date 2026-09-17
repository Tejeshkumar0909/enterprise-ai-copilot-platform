from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI
from app.agent import answer_question
from app.ingest import build_index
from app.models import QueryRequest, QueryResponse, IngestResponse
from app.retriever import LocalKnowledgeBase
STORE = Path("data/index.json"); SAMPLE_DOCS = Path("sample_docs")
app = FastAPI(title="Enterprise AI Copilot Platform", version="1.0.0")
_kb: LocalKnowledgeBase | None = None

def get_kb() -> LocalKnowledgeBase:
    global _kb
    if _kb is None:
        if not STORE.exists(): build_index(SAMPLE_DOCS, STORE)
        _kb = LocalKnowledgeBase.from_path(STORE)
    return _kb
@app.get("/health")
def health(): return {"status": "ok", "documents": len(get_kb().docs)}
@app.post("/ingest", response_model=IngestResponse)
def ingest():
    global _kb; count = build_index(SAMPLE_DOCS, STORE); _kb = LocalKnowledgeBase.from_path(STORE)
    return IngestResponse(documents_indexed=count, store_path=str(STORE))
@app.post("/query", response_model=QueryResponse)
def query(payload: QueryRequest): return answer_question(get_kb(), payload.question, payload.top_k)
