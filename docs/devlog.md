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