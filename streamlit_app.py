import streamlit as st

from app.storage.db import init_db
from app.storage.logging import get_recent_logs
from app.school_packs.loader import list_school_packs
from app.admin.ingestion import get_pack_summary, run_ingestion
from app.admin.diagnostics import get_latest_ingestion_runs
from app.rag.retriever import retrieve_chunks

init_db()

st.set_page_config(page_title="Campus Copilot", layout="wide")
st.title("Campus Copilot")
st.caption("Grounded academic copilot with retrieval debugging and admin diagnostics")

packs = list_school_packs()

if not packs:
    st.warning("No school packs found. Add one under school_packs/")
    st.stop()

school_id = st.sidebar.selectbox("Select school pack", packs)
workspace = st.sidebar.radio("Workspace", ["Retrieval Debug", "Admin Center"])

if workspace == "Retrieval Debug":
    st.subheader("Retrieval Debug")
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

else:
    st.subheader("Admin Center")

    summary = get_pack_summary(school_id)
    st.markdown("### School Pack Summary")
    st.write(summary)

    if st.button("Ingest selected school pack"):
        chunk_count = run_ingestion(school_id)
        st.success(f"Ingested {chunk_count} chunks for {school_id}")

    st.markdown("### Recent Ingestion Runs")
    runs = get_latest_ingestion_runs(limit=10)
    if runs:
        st.dataframe(runs, use_container_width=True)
    else:
        st.info("No ingestion runs yet.")

    st.markdown("### Recent Logs")
    logs = get_recent_logs(limit=10)
    if logs:
        st.dataframe(logs, use_container_width=True)
    else:
        st.info("No logs yet.")