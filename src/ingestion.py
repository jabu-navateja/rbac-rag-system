from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent
DOCUMENTS_DIR = BASE_DIR / "documents"
CHROMA_DIR = BASE_DIR.parent / "data" / "chroma"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = client.get_or_create_collection(
    name="enterprise_documents"
)


def split_text(text, chunk_size=500, overlap=80):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def get_department(file_path):
    return file_path.parent.name


def get_access_level(text):
    for line in text.splitlines():
        if line.startswith("Access Level:"):
            return line.split(":", 1)[1].strip()

    return "Full"


def ingest_documents():
    documents = []
    metadatas = []
    ids = []

    document_number = 0

    for file_path in DOCUMENTS_DIR.rglob("*.md"):

        text = file_path.read_text(encoding="utf-8")

        department = get_department(file_path)
        access_level = get_access_level(text)

        chunks = split_text(text)

        for chunk_number, chunk in enumerate(chunks):

            document_id = f"doc_{document_number}"

            documents.append(chunk)

            metadatas.append({
                "department": department,
                "access_level": access_level,
                "source": file_path.name,
                "chunk_number": chunk_number
            })

            ids.append(document_id)

            document_number += 1

    embeddings = embedding_model.encode(documents).tolist()

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Documents processed: {len(list(DOCUMENTS_DIR.rglob('*.md')))}")
    print(f"Chunks stored: {len(documents)}")
    print("ChromaDB ingestion completed successfully.")


if __name__ == "__main__":
    ingest_documents()