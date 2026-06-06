from app.ingestion.embedder import Embedder
from app.ingestion.vector_store import VectorStore
from app.ingestion.metadata_manager import MetadataManager

from app.rag.rag_pipeline import RAGPipeline


FAISS_PATH = "data/vector_store/faiss.index"
METADATA_PATH = "data/vector_store/metadata.json"


# Load Metadata
metadata_manager = MetadataManager()

metadata = metadata_manager.load(
    METADATA_PATH
)

# Load FAISS
vector_store = VectorStore(384)

vector_store.load(
    FAISS_PATH
)

# Initialize Components
embedder = Embedder()
rag = RAGPipeline()


while True:

    query = input(
        "\nAsk Question (type exit to quit): "
    )

    if query.lower() == "exit":
        break

    print(
        f"\nQuestion Received: {query}"
    )

    # Create Query Embedding
    query_embedding = embedder.embed(
        [query]
    )[0]

    # Retrieve Top K Results
    results = vector_store.search(
        query_embedding,
        k=5
    )

    retrieved_chunks = []
    sources = set()

    for idx in results:

        chunk_data = metadata[idx]

        text = chunk_data["text"]

        # Skip useless logo chunks
        if (
            chunk_data["type"] == "image_description"
            and len(text) < 100
        ):
            continue

        retrieved_chunks.append(text)

        sources.add(
            chunk_data["source"]
        )

        print(
            f"\nChunk ID : {chunk_data['chunk_id']}"
        )

        print(
            f"Type     : {chunk_data['type']}"
        )

        print(
            f"Source   : {chunk_data['source']}"
        )

        if chunk_data["type"] == "image_description":

            print(
                f"Image    : {chunk_data.get('image_path', 'N/A')}"
            )

        print("\nPreview:")

        print(
            chunk_data["text"][:300]
        )

        print("\n" + "-" * 60)

    # Build Context
    context = "\n\n".join(
        retrieved_chunks
    )

    print("\n" + "=" * 60)
    print("CONTEXT SENT TO LLM")
    print("=" * 60)

    print(
        context[:1500]
    )

    print("\n" + "=" * 60)

    # Generate Answer
    try:

        answer = rag.generate_answer(
            query,
            context
        )

        print("\nANSWER")
        print("=" * 60)

        print(answer)

    except Exception as e:

        print(
            f"\nLLM Error: {e}"
        )

    print("\nSOURCES")
    print("=" * 60)

    for source in sources:

        print(
            f"- {source}"
        )

    print("\n")