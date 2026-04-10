import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from config import (
    MANUALS_DIR, VECTOR_STORE_PATH,
    COHERE_API_KEY, COHERE_EMBEDDING_MODEL,
    CHUNK_SIZE, CHUNK_OVERLAP, RAG_TOP_K
)


def build_vector_store():
    documents = []
    for filename in os.listdir(MANUALS_DIR):
        if filename.endswith(".txt") or filename.endswith(".pdf"):
            filepath = os.path.join(MANUALS_DIR, filename)
            loader = TextLoader(filepath)
            documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)

    embeddings = CohereEmbeddings(
        cohere_api_key=COHERE_API_KEY,
        model=COHERE_EMBEDDING_MODEL
    )

    vector_store = FAISS.from_documents(chunks, embeddings)
    save_path = str(VECTOR_STORE_PATH.resolve())
    os.makedirs(save_path, exist_ok=True)
    vector_store.save_local(save_path)
    print("Vector store built and saved.")
    return vector_store


def load_vector_store():
    embeddings = CohereEmbeddings(
        cohere_api_key=COHERE_API_KEY,
        model=COHERE_EMBEDDING_MODEL
    )
    vector_store = FAISS.load_local(
        str(VECTOR_STORE_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vector_store


def search_maintenance_knowledge(query: str) -> list:
    index_file = VECTOR_STORE_PATH / "index.faiss"

    if index_file.exists():
        vector_store = load_vector_store()
    else:
        vector_store = build_vector_store()

    results = vector_store.similarity_search(query, k=RAG_TOP_K)

    return [
        {
            "content": doc.page_content,
            "source": doc.metadata.get("source", "unknown")
        }
        for doc in results
    ]