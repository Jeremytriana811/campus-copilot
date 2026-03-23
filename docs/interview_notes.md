# Interview Notes

## Why this project?
I wanted to build a grounded copilot for a domain where wrong answers matter.

## Key architecture idea
- Documents answer questions
- Structured rules drive planning
- Constraint solvers handle scheduling
- The model explains, but does not own, hard decisions

## Reliability
- Citations
- Refusal mode
- Evaluation
- Logging


## Why school packs?
They let me keep the application logic fixed while changing the data source by institution.

## Why SQLite?
I chose SQLite because it was enough for a local-first prototype and kept setup and deployment simple.

## Why add logs early?
Logs make it much easier to debug ingestion failures, retrieval mistakes, and future answer quality problems.

## Why validate foundation before ingestion?
If config, storage, and school-pack loading are unstable, later debugging becomes much harder. I wanted to isolate foundation issues first.

## Why use curated documents first?
The full catalog is authoritative, but it is too large and noisy for a strong v1 retriever. I kept the full catalog as a raw source and used a smaller curated set first to improve retrieval precision, simplify debugging, and produce cleaner citations.

## Why not let the model handle everything?
I do not want the model making hard academic decisions by itself. For planning and scheduling, deterministic logic and constraint-based methods are more reliable than prompting alone.

## What made this feel like a real software project?
I separated config from logic, added persistence with SQLite, added logs for observability, organized school data into modular packs, wrote tests early, and used Git branches with validation before merging.

## Why test ingestion before retrieval?
If extraction and chunking are wrong, retrieval quality will be wrong too. I validated document text extraction and indexing first so retrieval failures would be easier to diagnose.

## Why use curated docs first?
The full catalog is authoritative, but it is too noisy for a strong v1 retriever. I used a smaller curated set first to improve retrieval precision and make debugging easier.

## Why test retrieval before grounded answering?
If retrieval is weak, grounded answering will still be weak. I tested retrieval first so I could separate retrieval quality problems from answer-generation problems.

## What did retrieval testing show?
The pipeline worked technically, but retrieval quality was mixed. Questions about elective credits did well, while prerequisite and required-course questions often returned overly broad or elective-focused chunks.

## What would I improve next?
I would improve the curated document set, especially by adding cleaner prerequisite/course-description sources and reducing retrieval noise from broad elective/course-list documents.

## Why use a retrieval debug UI?
I wanted a fast way to inspect top-k results, document names, page numbers, and chunk quality before moving to grounded answering.

## What did the retrieval UI show?
The retrieval pipeline worked technically, but result quality was mixed. Elective-credit questions performed well, while prerequisite and required-course questions often returned overly broad or noisy chunks.

## Why was retrieval quality mixed?
The current curated set is better for program requirements than for precise prerequisite lookups. The elective/course-list PDF also appeared to dominate several search results.

## Why not use the full raw catalog immediately?
The raw catalog is much larger and noisier. I kept retrieval focused on a curated set first so I could debug precision before expanding the source set.

## What is one limitation of the current approach?
Some PDFs, especially flowcharts or highly visual documents, may not extract clean text with `pypdf`, which limits their usefulness in retrieval.

## Why didn’t you move straight to grounded answering?
Because the retrieval layer was not reliable enough yet. I chose to avoid building answer generation on top of weak retrieval and instead improved the product with admin workflows and logging.

## Why add an Admin Center?
I wanted the project to feel like a managed product, not just a local script. The Admin Center lets an operator inspect school pack contents, trigger ingestion, and review ingestion/log history without touching Python code.

## Why do logs matter here?
Logs help diagnose whether a bad answer came from ingestion problems, retrieval problems, or missing source coverage.

## Why did you add rule-based refusal on top of retrieval?
Nearest-neighbor retrieval can return semantically related but still irrelevant chunks. I added conservative refusal logic for unsupported question types to reduce false confidence and make the copilot safer.

## Why is refusal important?
A grounded copilot should not answer confidently when the source documents do not support the question. Refusal behavior is part of trust and reliability.

## Why add an Evaluation Center before more advanced answering?
I wanted measurable pass/fail feedback before making the copilot feel smarter. That let me inspect retrieval and refusal behavior separately instead of hiding weak retrieval behind polished responses.