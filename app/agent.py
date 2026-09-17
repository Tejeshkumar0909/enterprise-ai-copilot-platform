from __future__ import annotations
from app.retriever import LocalKnowledgeBase
SUMMARY_WORDS = {"summarize", "summary", "overview", "brief"}
SEARCH_WORDS = {"find", "search", "locate", "show"}

def classify_intent(question: str) -> str:
    tokens = set(question.lower().replace("?", "").split())
    if tokens & SUMMARY_WORDS: return "summarize"
    if tokens & SEARCH_WORDS: return "search"
    return "qa"

def answer_question(kb: LocalKnowledgeBase, question: str, top_k: int = 3) -> dict:
    intent = classify_intent(question); hits = kb.search(question, top_k=top_k)
    if not hits:
        return {"intent": intent, "answer": "I do not have indexed documents to answer from.", "citations": [], "grounded": False}
    if intent == "search":
        answer = "I found these relevant knowledge-base passages: " + "; ".join(f"{h['title']} ({h['score']:.2f})" for h in hits)
    elif intent == "summarize":
        answer = "Summary from the indexed sources: " + " ".join(h["snippet"] for h in hits[:2])
    else:
        answer = f"Based on {hits[0]['title']}, {hits[0]['snippet']} The response is limited to indexed source material and includes citations so reviewers can verify the answer."
    return {"intent": intent, "answer": answer, "citations": hits, "grounded": bool(hits)}
