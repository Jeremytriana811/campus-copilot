import streamlit as st

from app.storage.db import init_db
from app.school_packs.loader import list_school_packs
from app.rag.ingest import ingest_school_pack
from app.rag.retriever import retrieve_chunks

init_db()

st.set_page_config(page_title="Campus Copilot", layout="wide")
st.title("Campus Copilot")
st.caption("Grounded academic copilot with evidence, planning, and scheduling")

packs = list_school_packs()

if not packs:
    st.warning("No school packs found. Add one under school_packs/")
    st.stop()

school_id = st.sidebar.selectbox("Select school pack", packs)
tab1, tab2 = st.tabs(["Admin / Ingestion", "Retrieval Debug"])

with tab1:
    st.subheader("Ingest Documents")
    if st.button("Ingest selected school pack"):
        count = ingest_school_pack(school_id)
        st.success(f"Ingested {count} chunks for {school_id}")

with tab2:
    st.subheader("Retrieval Debug View")
    question = st.text_input(
        "Ask a question",
        placeholder="What are the prerequisites for Operating Systems?",
    )

    if st.button("Search") and question:
        hits = retrieve_chunks(school_id, question, k=5)

        if not hits:
            st.warning("No results found.")
        else:
            for i, hit in enumerate(hits, start=1):
                st.markdown(f"### Hit {i}")
                st.write(f"Document: {hit['metadata'].get('document_name')}")
                st.write(f"Page: {hit['metadata'].get('page')}")
                st.write(f"Distance: {hit['distance']}")
                st.write(hit["text"])
                st.divider()