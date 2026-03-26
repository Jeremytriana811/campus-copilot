# Dev Log

## 2026-03-21 — Document selection for `ucf_cs`

Goal:
- Collect high-signal official documents for the first UCF CS school pack

What I changed:
- Selected curated official documents for the initial retrieval set
- Added a raw/full catalog source for backup reference
- Organized UCF docs into `raw/` and `curated/`

Selected docs:
- `cs_program_requirements.pdf`
- `cs_courses_prereqs.pdf`
- `cs_flowchart.pdf`
- `cs_advising_guide.pdf`

Rejected:
- catalog homepage
- mission statement
- general university contact pages

Why I changed it:
- These selected documents directly support advising Q&A, requirement checking, degree planning, and schedule planning
- Lower-signal pages would add retrieval noise without helping core questions

What broke:
- I could not find a single official CS advising guide PDF that cleanly covered everything I wanted

What passed:
- I found enough official sources to support a strong v1 curated document set

Metrics before:
- none

Metrics after:
- raw sources added: 1
- curated sources added: 4

Decision:
- Kept the full UCF undergraduate catalog as an official raw source
- Used smaller curated PDFs for the active retrieval set
- Created a derived advising guide from official sources and labeled it non-authoritative

Why this decision:
- The full catalog contains useful official information, including Computer Science (B.S.), course listings, and university degree requirements
- But it is too large and noisy for a strong v1 retriever
- A curated set should improve retrieval precision, speed up ingestion, simplify debugging, and produce cleaner citations

Next step:
- Validate the project foundation before starting ingestion

---

## 2026-03-21 — Foundation validation before ingestion

Goal:
- Validate config, DB, logging, and school pack loader before moving to ingestion

What I changed:
- Added central config paths in `app/core/config.py`
- Added SQLite bootstrap in `app/storage/db.py`
- Added event logging helpers in `app/storage/logging.py`
- Added school pack loader in `app/school_packs/loader.py`
- Added first UCF school pack structure with `metadata.json`
- Added raw and curated document folders
- Added initial test coverage for config, DB, and school pack loading

Why I changed it:
- I wanted a clean system foundation before building ingestion and retrieval

What broke:
- The school pack folders were nested incorrectly at first
- I accidentally mixed PowerShell commands with the Python REPL
- PowerShell virtual environment activation caused confusion

What passed:
- config path imports
- DB initialization
- school pack listing
- school pack loading
- logging write/read
- pytest checks

Metrics before:
- none

Metrics after:
- school packs loaded: 1
- DB initialized: yes
- log write/read: yes
- tests passing: 4/4
- pytest runtime: 0.05s

Decision:
- The foundation is stable enough to begin ingestion next

Next step:
- Build PDF ingestion for the curated UCF document set first, then test chunking and indexing

---

## 2026-03-21 — PDF ingestion and vector indexing

Goal:
- Validate PDF ingestion, chunking, and vector indexing for curated UCF documents

What I changed:
- Added `app/rag/backend.py`
- Added `app/rag/ingest.py`
- Added PDF chunking with chunk size 1200 and overlap 150
- Added Chroma vector indexing for school-specific retrieval
- Switched ingestion to read from `docs/curated/`
- Added ingestion test coverage in `tests/test_ingest.py`

Why I changed it:
- I wanted retrieval to be grounded in smaller, cleaner official documents before building answer generation

What broke:
- Initial ingestion returned 0 chunks because the code searched `docs/` directly instead of `docs/curated/`

What passed:
- PDF text extraction worked
- embeddings loaded correctly
- ingestion completed successfully
- chunks were indexed
- pytest checks passed
- After fixing the curated path, ingestion processed 3 PDFs and indexed 60 chunks

Metrics before:
- chunks indexed: 0
- tests passing: 4/4

Metrics after:
- curated PDFs processed: 3
- ingestion run history:
  - first run: 0 docs / 0 chunks
  - fixed runs: 3 docs / 60 chunks
- chunks indexed: 60
- tests passing: 6/6
- pytest runtime: 7.87s

Decision:
- ingestion is working and the project is ready for retrieval code next

Next step:
- add `retriever.py` and test real retrieval queries before moving to grounded answering

---

## 2026-03-21 — Retrieval validation before grounded answering

Goal:
- Validate top-k retrieval quality before building grounded answers

What I changed:
- Added `app/rag/retriever.py`
- Added retrieval logging
- Added retrieval test coverage in `tests/test_retriever.py`
- Added a minimal retrieval debug UI
- Added `streamlit_app.py` as the project-root Streamlit entrypoint
- Ran retrieval through the UI instead of terminal-only tests
- Verified ingestion from the UI

Why I changed it:
- I wanted to test retrieval independently before adding answer generation
- I wanted to inspect retrieval behavior in a more realistic product flow

What broke:
- Running Streamlit from `app/main.py` caused `ModuleNotFoundError: No module named 'app'`
- Some queries returned semantically related but wrong chunks
- Prerequisite and required-course questions were weak
- The elective/course-list PDF appeared to dominate several results
- Operating Systems prerequisite retrieval was weak

What passed:
- Retrieval returned top-k results
- Chroma queries worked
- Retrieval logs were written
- Streamlit retrieval debug UI ran successfully from `streamlit_app.py`
- UI ingestion completed with 60 chunks
- Some question types, like elective-credit questions, returned useful hits
- Pytest checks passed

Metrics before:
- retrieval tests: none
- retrieval debug UI: not tested
- tests passing: 6/6

Metrics after:
- retrieval smoke tests run: 4
- UI-ingested chunks: 60
- clearly useful top hit: 1
- mixed top hit: 1
- weak top hit: 2
- tests passing: 7/7
- pytest runtime: 7.82s

Decision:
- Use `streamlit_app.py` as the UI entrypoint
- Retrieval infrastructure works, but retrieval quality is mixed
- Do not move to grounded answering yet
- Postpone grounded answering until the source set and retrieval quality improve

Next step:
- Improve the curated document set and retrieval behavior before moving to grounded answering
- Continue strengthening the product with admin tooling in parallel

---

## 2026-03-22 — Admin Center and diagnostics

Goal:
- Add admin workflow and diagnostics without pretending retrieval is already solved

What I changed:
- Added `app/admin/ingestion.py`
- Added `app/admin/diagnostics.py`
- Updated `streamlit_app.py` with an Admin Center workspace
- Added school pack summary, ingestion control, recent runs, and recent logs

Why I changed it:
- I wanted the project to feel more like a managed product and not just a script-based prototype

What passed:
- Admin Center rendered successfully
- School pack summary displayed correctly
- UI ingestion button worked
- Recent ingestion runs displayed
- Recent logs displayed
- Retrieval queries and ingestion events were visible in logs

What broke:
- Nothing major in this phase

Metrics before:
- admin UI: not implemented

Metrics after:
- admin workspace: pass
- school pack summary: pass
- recent ingestion runs visible: yes
- recent logs visible: yes

Decision:
- Continue improving product/admin tooling while retrieval quality is still being refined

Next step:
- Commit and push the Admin Center phase
- Move to Evaluation Center, or return later to retrieval tuning

## 2026-03-22 — Refusal logic fix for Student Copilot

Goal:
- Prevent unsupported question types from being incorrectly labeled as grounded

What I changed:
- Updated `app/rag/answering.py`
- Added simple unsupported-question pattern refusal
- Tightened the grounded-answer distance threshold

Why I changed it:
- The Student Copilot incorrectly marked unsupported professor-ranking questions as grounded when retrieval returned semantically nearby but irrelevant chunks

What passed:
- Student Copilot UI, evidence panel, and supported-question flow were already working
- Unsupported questions now refuse instead of showing misleading evidence

What broke:
- Some borderline retrieval cases now refuse more often, including weak prerequisite queries, but that is safer than false confidence

Decision:
- Prefer conservative refusal over false confidence while retrieval quality is still mixed

Next step:
- Commit and push the Student Copilot phase, then move to the Evaluation Center

## 2026-03-22 — Evaluation Center

Goal:
- Add a simple offline evaluation workflow for retrieval and refusal behavior

What I changed:
- Added `app/eval/eval_questions.json`
- Added `app/eval/eval_runner.py`
- Updated `streamlit_app.py` with an Evaluation Center workspace

Why I changed it:
- I wanted a measurable way to inspect pass/fail behavior before moving to more advanced answer generation

What passed:
- Evaluation Center rendered successfully
- Evaluation suite ran from the UI
- Results table displayed pass/fail details
- Eval runs were recorded in SQLite
- Run 1 finished with 3/3 passing
- The system produced 1 grounded answer and 2 correct refusals

What broke:
- Nothing major in this phase
- Streamlit showed a non-blocking deprecation warning about `use_container_width`

Decision:
- Keep improving measurable quality before more advanced answering behavior
- Treat the Streamlit warning as a cleanup task, not a functional issue

Next step:
- Commit and push the Evaluation Center phase

What passed:
- Pytest checks passed
- Test suite is now 7/7 passing

Metrics after:
- tests passing: 7/7
- pytest runtime: 35.75s

## 2026-03-22 — Structured degree checker

Goal:
- Add deterministic requirement-checking logic using structured UCF program rules

What I changed:
- Added `school_packs/ucf_cs/structured/requirements.json`
- Added `app/planner/checker.py`
- Added `tests/test_degree_checker.py`

Why I changed it:
- I wanted requirement checking to use structured and auditable rules instead of relying on retrieval or language generation

What passed:
- The checker loaded structured requirements successfully
- Missing core courses were identified correctly
- Choice-group logic worked
- Milestone checks worked
- Pytest checks passed
- Manual smoke test returned the expected missing-core, choice-group, and milestone results

What broke:
- Nothing major in this phase

Metrics after:
- tests passing: 10/10
- pytest runtime: 35.73s
- manual smoke test: pass

Decision:
- Keep degree progress logic deterministic and separate from grounded QA

Next step:
- Commit and push the degree checker phase

## 2026-03-22 — Better planner foundation

Goal:
- Add a term-by-term planner that is stronger than simple course grouping but still easy to explain and test

What I changed:
- Added `app/planner/generator.py`
- Added `tests/test_planner.py`
- Added a small prerequisite map for key required-course sequencing
- Added simple choice-group planning support

Why I changed it:
- I wanted the planner to respect basic academic sequencing instead of just splitting missing courses into equal-size terms

What passed:
- The planner respected max-courses-per-term limits
- The planner did not re-plan already completed courses
- Dependent courses were placed after prerequisite courses
- Pytest checks passed
- Manual smoke test produced a valid multi-term plan with no unresolved courses

What broke:
- Nothing major in this phase

Metrics after:
- tests passing: 13/13
- pytest runtime: 8.31s
- manual smoke test: pass

Decision:
- Keep the planner deterministic and modest in scope
- Treat this as a stronger v1 planner, not the final full academic planner

Next step:
- Commit and push the planner phase

## 2026-03-22 — Scheduler foundation

Goal:
- Add a simple deterministic schedule-conflict checker

What I changed:
- Added `app/scheduler/solver.py`
- Added `tests/test_scheduler.py`

Why I changed it:
- I wanted the scheduling layer to use deterministic conflict logic instead of relying on language generation

What passed:
- Overlapping sections on the same day were detected correctly
- Different-day sections were allowed
- Conflict-free schedules returned success
- Conflicting schedules returned failure
- Pytest checks passed
- Manual smoke tests returned the expected success and failure outputs

What broke:
- Nothing major in this phase

Metrics after:
- tests passing: 17/17
- pytest runtime: 7.59s
- manual smoke test (success): pass
- manual smoke test (failure): pass

Decision:
- Keep scheduling logic deterministic and easy to explain before adding more advanced optimization

Next step:
- Commit and push the scheduler phase