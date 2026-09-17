from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json, re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@dataclass
class Document:
    doc_id: str
    title: str
    text: str

class LocalKnowledgeBase:
    def __init__(self, docs: list[Document]):
        self.docs = docs
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.matrix = self.vectorizer.fit_transform([d.text for d in docs]) if docs else None
    @classmethod
    def from_path(cls, path: str | Path) -> "LocalKnowledgeBase":
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls([Document(**item) for item in raw["documents"]])
    def save(self, path: str | Path) -> None:
        path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"documents": [asdict(d) for d in self.docs]}, indent=2), encoding="utf-8")
    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if not self.docs: return []
        scores = cosine_similarity(self.vectorizer.transform([query]), self.matrix).ravel()
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
        return [{"doc_id": self.docs[i].doc_id, "title": self.docs[i].title, "score": float(score), "snippet": make_snippet(self.docs[i].text, query)} for i, score in ranked]

def make_snippet(text: str, query: str, width: int = 360) -> str:
    terms=[re.escape(t.lower()) for t in query.split() if len(t)>3]
    lower=text.lower(); pos=0
    for term in terms:
        m=re.search(term, lower)
        if m: pos=max(0, m.start()-80); break
    snippet=text[pos:pos+width].strip().replace("\n", " ")
    return snippet + ("..." if pos+width < len(text) else "")
