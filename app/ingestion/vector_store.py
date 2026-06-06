import faiss
import numpy as np


class VectorStore:

    def __init__(self, dimension):
        self.index = faiss.IndexFlatL2(dimension)

    def add_embeddings(self, embeddings):
        embeddings = np.array(
            embeddings,
            dtype="float32"
        )

        self.index.add(embeddings)

    def save(self, path):
        faiss.write_index(
            self.index,
            path
        )

    def load(self, path):
        self.index = faiss.read_index(
            path
        )

    def search(self, query_embedding, k=3):

        query_embedding = np.array(
            [query_embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            query_embedding,
            k
        )

        return indices[0]