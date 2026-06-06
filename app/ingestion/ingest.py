from app.ingestion.document_parser import DocumentParser
from app.ingestion.chunker import TextChunker
from app.ingestion.embedder import Embedder
from app.ingestion.vector_store import VectorStore
from app.ingestion.metadata_manager import MetadataManager

from app.vision.image_extractor import ImageExtractor
from app.vision.image_filter import ImageFilter
from app.vision.image_analyzer import ImageAnalyzer
import sys

import os


UPLOAD_FOLDER = "data/uploads"

FAISS_PATH = "data/vector_store/faiss.index"

METADATA_PATH = "data/vector_store/metadata.json"

IMAGE_FOLDER = "data/extracted_images"

import os
all_chunks = []
all_metadata = []

current_chunk_id = 0

document_files = []

SUPPORTED_EXTENSIONS = (
    ".pdf",
    ".docx",
    ".txt"
)

for file in os.listdir(UPLOAD_FOLDER):

    if file.lower().endswith(
        SUPPORTED_EXTENSIONS
    ):

        document_files.append(
            os.path.join(
                UPLOAD_FOLDER,
                file
            )
        )

print("Found Documents:")
print(document_files)

# Initialize Components
parser = DocumentParser()
chunker = TextChunker()
embedder = Embedder()

image_extractor = ImageExtractor()
image_filter = ImageFilter()
image_analyzer = ImageAnalyzer()

all_chunks = []
metadata = []


# Process All PDFs
for file_path in document_files:

    print(f"Processing: {file_path}")

    content = parser.parse(file_path)
    print("TEXT PARSING COMPLETED")

    chunks = chunker.chunk_text(content)
    
    print(
    f"{os.path.basename(file_path)} "
    f"generated {len(chunks)} text chunks"
)

    for chunk in chunks:

        all_chunks.append(chunk)

        metadata.append(
    {
        "chunk_id": current_chunk_id,
        "type": "text",
        "text": chunk,
        "source": os.path.basename(file_path)
    }
)

        current_chunk_id += 1

    print("STARTING IMAGE EXTRACTION")

        # Process Images Only For PDFs

    if file_path.lower().endswith(".pdf"):

        image_paths = image_extractor.extract_images(
            file_path,
            IMAGE_FOLDER
        )

        for image_path in image_paths[:5]:

            if not image_filter.is_useful_image(
                image_path
            ):
                continue

            print(
                f"Analyzing Image: {image_path}"
            )
            

            try:

                description = image_analyzer.describe_image(
                    image_path
                )
                
                print(
    f"Image description length: "
    f"{len(description)}")

                all_chunks.append(
                    description
                )

                metadata.append(
                    {
                        "chunk_id": current_chunk_id,
                        "type": "image_description",
                        "text": description,
                        "source": os.path.basename(
                            file_path
                        ),
                        "image_path": image_path
                    }
                )

                current_chunk_id += 1

            except Exception as e:

                print(
                    f"Image Analysis Failed: {e}"
                )

# No documents left

if len(all_chunks) == 0:

    metadata_manager = MetadataManager()

    metadata_manager.save(
        [],
        METADATA_PATH
    )

    if os.path.exists(
        FAISS_PATH
    ):
        os.remove(
            FAISS_PATH
        )

    print("Knowledge base cleared")

    exit()

# Create Embeddings

embeddings = embedder.embed(
    all_chunks
)

vector_store = VectorStore(
    embeddings.shape[1]
)

vector_store.add_embeddings(
    embeddings
)

vector_store.save(
    FAISS_PATH
)

# Save Metadata
metadata_manager = MetadataManager()

metadata_manager.save(
    metadata,
    METADATA_PATH
)

print("Ingestion Completed")
print(f"Total Chunks Saved: {len(all_chunks)}")
print(f"Total Documents: {len(document_files)}")