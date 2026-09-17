from fastapi.testclient import TestClient
from app.agent import classify_intent
from app.ingest import build_index
from app.main import app
from app.retriever import LocalKnowledgeBase

def test_intent_router():
    assert classify_intent("summarize this document") == "summarize"
    assert classify_intent("find deployment info") == "search"
    assert classify_intent("How are hallucinations reduced?") == "qa"

def test_retriever_finds_relevant_doc(tmp_path):
    store = tmp_path / "index.json"; count = build_index("sample_docs", store); kb = LocalKnowledgeBase.from_path(store)
    hits = kb.search("hallucinations citations grounding", top_k=1)
    assert count >= 3; assert hits[0]["doc_id"] == "copilot_architecture"

def test_query_endpoint_returns_citations():
    client = TestClient(app); res = client.post("/query", json={"question": "How does the copilot reduce hallucinations?", "top_k": 2})
    assert res.status_code == 200; body = res.json(); assert body["grounded"] is True; assert body["citations"]
