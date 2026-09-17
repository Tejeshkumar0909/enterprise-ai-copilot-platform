from pydantic import BaseModel, Field
from typing import Literal

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int = Field(3, ge=1, le=10)

class Citation(BaseModel):
    doc_id: str
    title: str
    score: float
    snippet: str

class QueryResponse(BaseModel):
    intent: Literal["qa", "summarize", "search"]
    answer: str
    citations: list[Citation]
    grounded: bool

class IngestResponse(BaseModel):
    documents_indexed: int
    store_path: str
