from __future__ import annotations
from pathlib import Path
import argparse
from app.retriever import Document, LocalKnowledgeBase

def load_markdown_docs(input_dir: str | Path) -> list[Document]:
    docs=[]
    for path in sorted(Path(input_dir).glob("*.md")):
        text=path.read_text(encoding="utf-8")
        title=text.splitlines()[0].lstrip("# ") if text.splitlines() else path.stem
        docs.append(Document(doc_id=path.stem, title=title, text=text))
    return docs

def build_index(input_dir: str | Path, store: str | Path) -> int:
    kb=LocalKnowledgeBase(load_markdown_docs(input_dir)); kb.save(store); return len(kb.docs)

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--input", default="sample_docs"); parser.add_argument("--store", default="data/index.json")
    args=parser.parse_args(); print(f"indexed {build_index(args.input, args.store)} documents -> {args.store}")
if __name__ == "__main__": main()
