import streamlit as st
import sys

BASE_PATH = "/content/drive/MyDrive/legal-ai-system"

sys.path.append(BASE_PATH)

from app.ingestion.pdf_parser import (
    extract_text_from_pdf
)

from app.ingestion.chunker import (
    chunk_text
)

from app.retrieval.embedder import (
    get_embedding
)

from app.retrieval.vectordb import (
    add_chunk
)

from app.retrieval.retriever import (
    retrieve
)

from app.retrieval.reranker import (
    rerank_results
)

from app.drafting.grounded_generator import (
    generate_memo
)

from app.learning.memory_store import (
    save_edit,
    get_all_edits
)

from app.learning.pattern_extractor import (
    extract_patterns
)

# =====================================================
# CONFIG
# =====================================================

st.set_page_config(
    page_title="Legal AI System",
    layout="wide"
)

st.title(
    "AI-Powered Legal Drafting System"
)

# =====================================================
# SESSION STATE
# =====================================================

if "result" not in st.session_state:

    st.session_state["result"] = None

if "show_editor" not in st.session_state:

    st.session_state["show_editor"] = False

if "reranked" not in st.session_state:

    st.session_state["reranked"] = None


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def render_memo(memo):

    sections = {

        "Key Findings":
            memo.get("key_findings", []),

        "Notice Requirements":
            memo.get("notice_requirements", []),

        "Potential Risks":
            memo.get("potential_risks", []),

        "Missing Information":
            memo.get("missing_information", []),

        "Evidence References":
            memo.get("evidence_references", [])
    }

    for title, items in sections.items():

        st.subheader(title)

        if items:

            for item in items:

                st.write(f"• {item}")

        else:

            st.write(
                "No information available."
            )


# =====================================================
# FILE UPLOAD
# =====================================================

uploaded_file = st.file_uploader(
    "Upload Legal PDF",
    type=["pdf"]
)

if uploaded_file:

    pdf_path = (
        f"{BASE_PATH}/data/raw/temp_upload.pdf"
    )

    with open(pdf_path, "wb") as f:

        f.write(uploaded_file.read())

    st.success("PDF uploaded.")

    # =================================================
    # OCR + CHUNKING
    # =================================================

    pages = extract_text_from_pdf(
        pdf_path
    )

    all_chunks = []

    for page in pages:

        chunks = chunk_text(
            page["text"]
        )

        for i, chunk in enumerate(chunks):

            all_chunks.append({

                "chunk_id":
                    f"page_{page['page']}_chunk_{i}",

                "text":
                    chunk,

                "page":
                    page["page"]
            })

    st.info(
        f"Created {len(all_chunks)} chunks."
    )

    # =================================================
    # EMBEDDINGS
    # =================================================

    with st.spinner(
        "Generating embeddings..."
    ):

        for chunk in all_chunks:

            embedding = get_embedding(
                chunk["text"]
            )

            add_chunk(

                chunk_id=chunk["chunk_id"],

                text=chunk["text"],

                embedding=embedding,

                metadata={
                    "page": chunk["page"]
                }
            )

    st.success("Embeddings stored.")

    # =================================================
    # QUERY
    # =================================================

    query = st.text_input(
        "Ask Legal Question"
    )

    if query:

        with st.spinner(
            "Retrieving evidence..."
        ):

            results = retrieve(query)

            reranked = rerank_results(
                query,
                results
            )

            st.session_state[
                "reranked"
            ] = reranked

        with st.spinner(
            "Generating grounded memo..."
        ):

            result = generate_memo(
                reranked
            )

            st.session_state[
                "result"
            ] = result


# =====================================================
# SHOW RESULT
# =====================================================

if st.session_state["result"]:

    result = st.session_state["result"]

    if result["success"]:

        memo = result["memo"]

        st.header("Generated Memo")

        render_memo(memo)

        # =============================================
        # VERIFICATION
        # =============================================

        with st.expander(
            "Verification Result"
        ):

            st.write(
                result["verification"]
            )

        # =============================================
        # EVIDENCE
        # =============================================

        with st.expander(
            "Retrieved Evidence"
        ):

            reranked = st.session_state[
                "reranked"
            ]

            documents = reranked[
                "documents"
            ][0]

            ids = reranked["ids"][0]

            scores = reranked[
                "scores"
            ][0]

            for doc, chunk_id, score in zip(
                documents,
                ids,
                scores
            ):

                with st.expander(
                    f"{chunk_id} | score={score:.2f}"
                ):

                    st.write(doc)

        # =============================================
        # EDIT BUTTON
        # =============================================

        if st.button("✏️ Edit Memo"):

            st.session_state[
                "show_editor"
            ] = True

        # =============================================
        # EDITOR
        # =============================================

        if st.session_state[
            "show_editor"
        ]:

            st.subheader(
                "Edit Memo"
            )

            edited_text = st.text_area(

                "Improve memo:",

                value=str(memo),

                height=300
            )

            col1, col2 = st.columns(2)

            # =========================================
            # SAVE EDIT
            # =========================================

            with col1:

                if st.button(
                    "💾 Save Edit"
                ):

                    save_edit(

                        original_text=str(memo),

                        edited_text=edited_text,

                        edit_summary=(
                            "user correction"
                        )
                    )

                    st.success(
                        "Edit saved."
                    )

                    patterns = extract_patterns(
                        get_all_edits()
                    )

                    st.subheader(
                        "Learned Patterns"
                    )

                    st.json(patterns)

            # =========================================
            # CANCEL
            # =========================================

            with col2:

                if st.button(
                    "❌ Cancel"
                ):

                    st.session_state[
                        "show_editor"
                    ] = False

                    st.rerun()

    else:

        st.error(
            result["error"]
        )