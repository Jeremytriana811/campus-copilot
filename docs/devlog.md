# Dev Log

## Entry Template
- Date:3/21/2026
- Goal:
- What I changed: 
## Decision: Kept the full UCF undergraduate catalog as an official raw source, but created smaller curated PDFs for active retrieval.
- Why I changed it:
## Why:The full catalog contains useful official content, including Computer Science (B.S.), course listings, and university degree requirements, but it is too large and noisy for a strong v1 retriever.

Chosen approach:
- use full catalog as backup/raw source
- use smaller extracted PDFs for CS requirements, CS courses/prereqs, and general degree policies

Expected benefit:
better retrieval precision, faster ingestion, easier debugging, cleaner citations

- What broke:
- Metrics before:
- Metrics after:
- Decision:
- Next step: