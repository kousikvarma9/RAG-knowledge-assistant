from app.ingestion.document_parser import DocumentParser
from app.ingestion.chunker import TextChunker
from app.ingestion.embedder import Embedder
from app.ingestion.vector_store import VectorStore

from app.rag.rag_pipeline import RAGPipeline


# Parse Document
parser = DocumentParser()

content = parser.parse(
    "E:/sample_document.pdf"
)

# Chunking
chunker = TextChunker()

chunks = chunker.chunk_text(content)

# Embeddings
embedder = Embedder()

embeddings = embedder.embed(chunks)

# FAISS
vector_store = VectorStore(
    embeddings.shape[1]
)

vector_store.add_embeddings(
    embeddings
)

# User Question
query = input("Ask Question: ")

# Query Embedding
query_embedding = embedder.embed(
    [query]
)[0]

# Retrieval
results = vector_store.search(
    query_embedding,
    k=3
)

retrieved_context = "\n\n".join(
    [chunks[i] for i in results]
)

# Gemini
rag = RAGPipeline()

answer = rag.generate_answer(
    query,
    retrieved_context
)

print("\nAnswer:\n")
print(answer)