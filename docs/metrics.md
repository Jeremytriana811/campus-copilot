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