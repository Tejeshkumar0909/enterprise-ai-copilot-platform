# Copilot Architecture

The enterprise copilot is organized as a FastAPI service with a retrieval layer, an agent routing layer, and a response composer. Documents are indexed into a vector-search friendly representation. User questions are routed to search, summarization, or question-answering flows.

The design reduces hallucinations by grounding answers in retrieved passages, returning citations, and refusing to answer when the knowledge base does not contain enough evidence.
