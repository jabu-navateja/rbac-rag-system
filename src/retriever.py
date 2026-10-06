from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR.parent / "data" / "chroma"

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = client.get_collection(
    name="enterprise_documents"
)


def retrieve(query, top_k=5):
    query_embedding = embedding_model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    chunks = []

    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return chunks


if __name__ == "__main__":
    query = "What is the company leave policy?"

    results = retrieve(query)

    print("\nRetrieved Chunks:\n")

    for i, chunk in enumerate(results, 1):
        print(f"--- Chunk {i} ---")
        print("Source:", chunk["metadata"]["source"])
        print("Department:", chunk["metadata"]["department"])
        print("Distance:", chunk["distance"])
        print("Text:", chunk["text"])
        print()