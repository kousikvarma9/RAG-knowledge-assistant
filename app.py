import os
import re
import sys
import subprocess
import streamlit as st

from app.ingestion.embedder import Embedder
from app.ingestion.vector_store import VectorStore
from app.ingestion.metadata_manager import MetadataManager
from app.rag.rag_pipeline import RAGPipeline
from app.chat.chat_history import ChatHistory

FAISS_PATH = "data/vector_store/faiss.index"
METADATA_PATH = "data/vector_store/metadata.json"
UPLOAD_FOLDER = "data/uploads"

st.set_page_config(
    page_title="Knowledge Assistant",
    page_icon="🇦🇮",
    layout="wide"
)

if "history" not in st.session_state:

    st.session_state.history = (
        ChatHistory.load()
    )
    
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

st.markdown("""
<style>

.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

footer {
    visibility: hidden;
}

section[data-testid="stSidebar"] {
    padding-top: 0rem !important;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}

section[data-testid="stSidebar"] * {
    font-size: 13px !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    font-size: 18px !important;
}

/* Sidebar width */
[data-testid="stSidebar"]{
    width:280px !important;
    min-width:260px !important;
}

.fixed-header{
    position:sticky;
    top:0;
    z-index:999;
    background:inherit;
    padding-top:15px;
    padding-bottom:5px;
    text-align:center;
}

.main-title{
    padding-top:2px;
    padding-bottom:2px;
}

</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_components():
    metadata_manager = MetadataManager()
    metadata = metadata_manager.load(METADATA_PATH)
    if len(metadata) == 0:

        vector_store = None

    vector_store = VectorStore(384)
    if os.path.exists(
    FAISS_PATH
):
        vector_store.load(
        FAISS_PATH
    )

    embedder = Embedder()
    rag = RAGPipeline()

    return metadata, vector_store, embedder, rag



metadata, vector_store, embedder, rag = load_components()

document_count = len(
    set(
        item["source"]
        for item in metadata
    )
)

text_chunks = sum(
    1
    for item in metadata
    if item["type"] == "text"
)

image_chunks = sum(
    1
    for item in metadata
    if item["type"] == "image_description"
)


with st.sidebar:
    
    st.header("📂 Document Management")

    uploaded_files = st.file_uploader(
    "Upload Documents",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.uploader_key}"
)

    if st.button("🚀 Process Documents"):

        if uploaded_files:

            for uploaded_file in uploaded_files:

                save_path = os.path.join(
                    UPLOAD_FOLDER,
                    uploaded_file.name
                )

                with open(save_path, "wb") as f:
                    f.write(
                        uploaded_file.getbuffer()
                    )

            with st.spinner(
                "Processing documents..."
            ):

                subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "app.ingestion.ingest"
                    ]
                )

                st.cache_resource.clear()

                metadata_manager = MetadataManager()

                new_metadata = metadata_manager.load(
                    METADATA_PATH
                )

                document_count = len(
                    set(
                        item["source"]
                        for item in new_metadata
                    )
                )

                text_chunks = sum(
                    1
                    for item in new_metadata
                    if item["type"] == "text"
                )

                image_chunks = sum(
                    1
                    for item in new_metadata
                    if item["type"] == "image_description"
                )

            st.session_state.uploader_key += 1

            st.success(
                f"""
    ✅ Knowledge Base Updated Successfully

    📄 Documents: {document_count}
    🧩 Total Chunks: {len(new_metadata)}
    📝 Text Chunks: {text_chunks}
    🖼 Image Chunks: {image_chunks}
    """
            )

            # TEMPORARILY COMMENT THIS
            st.rerun()

        else:
            st.warning(
                "Please upload at least one file."
            )
            
            st.divider()
    
        # =========================
    # KNOWLEDGE BASE ANALYTICS
    # =========================

    text_chunks = sum(
        1
        for item in metadata
        if item["type"] == "text"
    )

    image_chunks = sum(
        1
        for item in metadata
        if item["type"] == "image_description"
    )

    document_count = len(
    set(item["source"] for item in metadata)
)

    st.subheader("📊 KNOWLEDGE BASE")

    st.write(f"📄 Documents: {document_count}")
    st.write(f"🧩 Chunks: {len(metadata)}")
    st.write(f"📝 Text: {text_chunks}")
    st.write(f"🖼 Images: {image_chunks}")

    st.divider()
    
    show_debug = st.toggle(
    "🔍 Show Retrieval Details",
    value=False
)

    st.divider()
    
    with st.expander(
    "📚 Indexed Documents",
    expanded=False):
        status = st.empty()
        documents = sorted(
        set(
            item["source"]
            for item in metadata
        )
    )
        
        for doc in documents:
            
            col1, col2 = st.columns(
        [4,1]
    )

            with col1:
                st.caption(
            f"📄 {doc}"
        )

            with col2:

                if st.button(
        "🗑",
        key=f"delete_{doc}"
    ):

                    file_path = os.path.join(
            UPLOAD_FOLDER,
            doc
        )

                    if os.path.exists(
            file_path
        ):

                        os.remove(
    file_path
)

                        status.info("Updating knowledge base...")

                        subprocess.run(
    [sys.executable, "-m", "app.ingestion.ingest"]
)
                        st.cache_resource.clear()

                        status.success(
    f"{doc} deleted successfully"
)
                        

                        st.rerun()

    st.divider()

    if st.button(
        "🗑 Clear History",
        use_container_width=True
    ):
        st.session_state.history = []

        ChatHistory.save([])
        st.rerun()
        
    
    if st.session_state.history:

        chat_text = ""

        for item in st.session_state.history:

            chat_text += (
        f"Question:\n"
        f"{item['question']}\n\n"
    )

            chat_text += (
        f"Answer:\n"
        f"{item['answer']}\n\n"
    )

            chat_text += (
        "Sources:\n"
    )

            for source in item["sources"]:

                    chat_text += (
                        f"- {source}\n"
                    )

            chat_text += (
                    "\n"
                    + "=" * 60
                    + "\n\n"
                )

        st.download_button(
                label="⬇ Download Chat History",
                data=chat_text,
                file_name="chat_history.txt",
                mime="text/plain",
                use_container_width=True
                
            )
st.markdown("""
<div class="fixed-header">
    <h1>
        Multimodal Knowledge Assistant
    </h1>

</div>
""",
unsafe_allow_html=True)

if not st.session_state.history:

    st.info(
        """
👋 Welcome to your Multimodal Knowledge Assistant

"""
    )


st.markdown(
    """
    <p style='text-align:center;
              color:gray;
              font-size:18px;'>
        Ask questions across PDFs, DOCX, TXT files and extracted image content
    </p>
    """,
    unsafe_allow_html=True
)


st.divider()

if st.session_state.history:

    for item in st.session_state.history:

        # USER BUBBLE

        st.markdown(
            f"""
            <div style="
                display:flex;
                justify-content:flex-end;
                margin-top:20px;
                margin-bottom:10px;
            ">
                <div style="
                    background:#ADD8E6;
                    color:black;
                    padding:12px 16px;
                    border-radius:18px;
                    max-width:40%;
                    margin-right:20px;
                ">
                     {item['question']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # SOURCE BADGES

        badges = ""

        for source in item["sources"]:
            badges += f"""
            <span style="
                background:#2d3748;
                color:white;
                padding:5px 10px;
                border-radius:15px;
                margin-right:5px;
                font-size:12px;
                display:inline-block;
                margin-top:10px;
            ">
                📄 {source}
            </span>
            """

        

        # ASSISTANT CARD

        with st.container(border=False):

            st.markdown("##### 🗣️ Knowledge Assistant")
            st.write(item["answer"])
            st.markdown(badges, unsafe_allow_html=True)  
    
    if show_debug:

                        with st.expander(
                            "🔍 Retrieved Chunks"
                        ):

                            for chunk in item["chunks"]:

                                st.markdown(
                                    f"**Source:** {chunk['source']}"
                                )

                                st.markdown(
                                    f"**Type:** {chunk['type']}"
                                )

                                st.write(
                                    chunk["text"]
                                )

                                st.divider()

question = st.chat_input(
    "Ask about your documents..."
)



if question:

    with st.spinner("Searching knowledge base..."):
        query_embedding = embedder.embed([question])[0]
        if len(metadata) == 0:

            st.warning(
                "No documents available. Please upload and process documents."
            )

            st.stop()

        results = vector_store.search(
            query_embedding,
            k=5
        )

        retrieved_chunks = []
        sources = set()
        debug_chunks = []

        for idx in results:
            chunk_data = metadata[idx]
            text = chunk_data["text"]

            if (
                chunk_data["type"] == "image_description"
                and len(text) < 100
            ):
                continue

            retrieved_chunks.append(text)
            sources.add(chunk_data["source"])
            debug_chunks.append(
    {
        "source": chunk_data["source"],
        "type": chunk_data["type"],
        "text": chunk_data["text"]
    }
)

        context = "\n\n".join(retrieved_chunks)

        try:
            answer = rag.generate_answer(
                question,
                context
            )
            print(answer)
        except Exception as e:
            answer = f"LLM Error: {e}"


    clean_answer = re.sub(
        r"<[^>]*>",
        "",
        str(answer)
)

    st.session_state.history.append(
{
    "question": question,
    "answer": clean_answer,
    "sources": list(sources),
    "chunks": debug_chunks
}
)

    ChatHistory.save(
    st.session_state.history
)

    st.rerun()
