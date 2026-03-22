# Metrics

## Retrieval
- Recall@5:
- MRR:
- Avg retrieval latency:

## Grounded QA
- Grounded answer rate:
- Correct refusal rate:
- Citation usefulness:
- p50 latency:
- p95 latency:

## Planner
- Valid plan rate:
- Prerequisite violation count:
- Requirement completion rate:

## Scheduler
- Conflict-free schedule rate:
- Constraint satisfaction rate:
- Generation latency:

## Admin / Platform
- School packs indexed:
- Ingestion success rate:
- Failed ingestion count:
- Eval pass rate:

## Foundation Validation Run 1 (2026-03-21)
- Config import: Pass
- DB initialization: Pass
- School pack listing: Pass
- School pack loading: Pass
- Logging write/read: Pass
- Pytest: 4/4 passing
- Pytest runtime: 0.05s

## PDF Ingestion Run 1 (2026-03-21)
- School pack: ucf_cs
- First run: 0 docs, 0 chunks
- Fixed runs: 3 docs, 60 chunks
- Chunks indexed: 60
- Ingestion status: Pass after bug fix
- Pytest: 6/6 passing
- Pytest runtime: 7.87s
- Notes: Initial bug came from scanning `docs/` instead of `docs/curated/`

## Retrieval Trial 1 (2026-03-21)
- Question: What are the prerequisites for Operating Systems?
- Hit count: 5
- Top hit useful: No
- Top document: Computer Science (B.S.).pdf page 6
- Notes: Retrieval returned a broadly relevant CS requirements chunk, but not a clear prerequisite answer for Operating Systems

## Retrieval Trial 2 (2026-03-21)
- Question: How many CS elective credits are required?
- Hit count: 5
- Top hit useful: Yes
- Top document: Computer Science (B.S.).pdf page 7
- Notes: Top hit clearly showed restricted electives as 9 total credits

## Retrieval Trial 3 (2026-03-21)
- Question: What is the first programming course?
- Hit count: 5
- Top hit useful: Mixed
- Top document: CSIT-Elective-List-AY2025-2026-Updated-on-6-27-25-Added-CNT4425.pdf page 7
- Notes: Top hit contained useful course descriptions, but the chunk was noisy and not a clean direct answer

## Retrieval Trial 4 (2026-03-21)
- Question: What courses are required for the computer science major?
- Hit count: 5
- Top hit useful: No
- Top document: CSIT-Elective-List-AY2025-2026-Updated-on-6-27-25-Added-CNT4425.pdf page 3
- Notes: Retrieval over-weighted elective course descriptions instead of core required courses