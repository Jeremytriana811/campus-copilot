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

## Retrieval Trial 1 (2026-03-21)
- Question: What are the prerequisites for Operating Systems?
- Hit count: 5
- Top hit useful: No
- Top document: Computer Science (B.S.).pdf page 6
- Found in top 5: Yes
- Found in top 1: No
- Notes: Retrieval returned a broadly relevant CS requirements chunk, but not a clear prerequisite answer for Operating Systems

## Retrieval Trial 2 (2026-03-21)
- Question: How many CS elective credits are required?
- Hit count: 5
- Top hit useful: Yes
- Top document: Computer Science (B.S.).pdf page 7
- Found in top 5: Yes
- Found in top 1: Yes
- Notes: Top hit clearly showed restricted electives as 9 total credits

## Retrieval Trial 3 (2026-03-21)
- Question: What is the first programming course?
- Hit count: 5
- Top hit useful: Mixed
- Top document: CSIT-Elective-List-AY2025-2026-Updated-on-6-27-25-Added-CNT4425.pdf page 7
- Found in top 5: Yes
- Found in top 1: Mixed
- Notes: Top hit contained useful course descriptions, but the chunk was noisy and not a clean direct answer

## Retrieval Trial 4 (2026-03-21)
- Question: What courses are required for the computer science major?
- Hit count: 5
- Top hit useful: No
- Top document: CSIT-Elective-List-AY2025-2026-Updated-on-6-27-25-Added-CNT4425.pdf page 3
- Found in top 5: Yes
- Found in top 1: No
- Notes: Retrieval over-weighted elective course descriptions instead of core required courses

## PDF Ingestion Run 2 (2026-03-21)
- Pytest: 7/7 passing
- Pytest runtime: 7.82s

## Retrieval Debug UI Check (2026-03-21)
- School pack: ucf_cs
- Admin ingestion button: Pass
- UI-ingested chunks: 60
- Notes: Streamlit UI successfully triggered ingestion without terminal-only commands

## Retrieval Trial 1 (2026-03-21)
- Question: What are the prerequisites for Operating Systems?
- Hit count: 5
- Top hit useful: No
- Top document: Computer Science (B.S.).pdf page 6
- Found in top 5: Yes
- Found in top 1: No
- Notes: Retrieval returned a general CS requirements chunk instead of a clear prerequisite answer for Operating Systems

## Retrieval Trial 2 (2026-03-21)
- Question: How many CS elective credits are required?
- Hit count: 5
- Top hit useful: Yes
- Top document: Computer Science (B.S.).pdf page 7
- Found in top 5: Yes
- Found in top 1: Yes
- Notes: Top hit clearly showed restricted electives as 9 total credits

## Retrieval Trial 3 (2026-03-21)
- Question: What is the first programming course?
- Hit count: 5
- Top hit useful: Mixed
- Top document: CSIT-Elective-List-AY2025-2026-Updated-on-6-27-25-Added-CNT4425.pdf page 7
- Found in top 5: Yes
- Found in top 1: Mixed
- Notes: Top hit contained useful course descriptions, but the chunk was noisy and the elective list appeared to dominate the result

## Retrieval Quality Summary (2026-03-21)
- Clearly useful top hits: 1
- Mixed top hits: 1
- Weak top hits: 1
- Main issue: elective/course-list PDF is dominating retrieval for some question types
- Main decision: improve curated documents before moving to grounded answering

## Admin Center Validation Run 1 (2026-03-22)
- School pack summary: Pass
- Curated PDF count: 3
- Raw PDF count: 1
- Recent ingestion runs visible: Yes
- Recent logs visible: Yes
- UI ingestion control: Pass
- Notes: Admin Center successfully exposed ingestion history and log history through the Streamlit UI
## Student Copilot Validation Run 1 (2026-03-22)
- Supported question tested: Yes
- Unsupported question tested: Yes
- Grounded response shown for supported query: Yes
- Refusal shown for unsupported query: Yes
- Evidence panel shown: Yes
- Notes: Student Copilot flow works. After tightening refusal logic, the system became more conservative and now refuses weak prerequisite queries instead of showing misleading grounded answers.

## Refusal Logic Fix Check (2026-03-22)
- Unsupported pattern refusal added: Yes
- Distance threshold tightened: Yes
- Question retested: Which professor is easiest for CS1?
- Expected result after fix: Refused
- Actual result after fix: Refused
- Notes: The refusal fix prevented unsupported professor-ranking questions from being incorrectly marked as grounded.

## Evaluation Center Run 1 (2026-03-22)
- Total questions: 3
- Passed questions: 3
- Grounded answers: 1
- Correct refusals: 2
- Notes: The evaluation workflow is working. The current system performs best on supported requirement-style questions and now correctly refuses unsupported or weakly supported questions.
- Pytest: 7/7 passing
- Pytest runtime: 35.75s
- Notes: Runtime increased after adding retrieval/evaluation-related tests, which is expected because those tests touch heavier components than the earlier foundation-only checks.

## Degree Checker Run 1 (2026-03-22)
- Structured requirements file added: Yes
- Degree checker implemented: Yes
- Choice-group logic working: Yes
- Milestone detection working: Yes
- Pytest: 10/10 passing
- Pytest runtime: 35.73s
- Manual smoke test: Pass
- Notes: The checker correctly identified missing core courses, satisfied the AI/ML choice group with `CAP4630`, showed the technical writing group still incomplete, and marked `COT3960` as a missing milestone.

## Planner Run 1 (2026-03-22)
- Planner implemented: Yes
- Max-courses-per-term respected: Yes
- Prerequisite ordering working: Yes
- Duplicate completed-course planning avoided: Yes
- Pytest: 13/13 passing
- Pytest runtime: 8.31s
- Manual smoke test: Pass
- Notes: The planner generated a valid term-by-term sequence, avoided already completed courses, selected `ENC3241` to satisfy the technical writing choice group, and produced no unresolved courses.

## Scheduler Run 1 (2026-03-22)
- Conflict detection implemented: Yes
- Conflict-free schedule success case: Yes
- Overlap failure case: Yes
- Pytest: 17/17 passing
- Pytest runtime: 7.59s
- Manual smoke test (success): Pass
- Manual smoke test (failure): Pass
- Notes: The scheduler foundation correctly distinguishes valid schedules from overlapping section combinations and reports conflicts clearly.