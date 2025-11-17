# scripts/ingest_rag_data.py
"""
RAG 인덱싱 스크립트 예시.
"""
from app.rag.embeddings import embed_texts
from app.rag.vector_store import global_vector_store
from app.rag.loaders.file_loader import load_from_file


def main():
    # TODO: rag_sources.yml 읽어서 반복 처리하는 방식으로 확장
    texts = load_from_file("README.md") if False else ["dummy doc"]
    vectors = embed_texts(texts)
    global_vector_store.add(texts, vectors)
    print(f"Ingested {len(texts)} docs into vector store")


if __name__ == "__main__":
    main()
