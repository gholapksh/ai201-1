# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
<!-- 
Proffessor and course reviews for UTD's CS department. This knowledge is valuable because official sources - course catalogs, department websites, professor bios tell students what a course covers, not what it's actually like to take it. Students need to know whether a professor's exams match the lectures, whether a course is manageable alongside other commitments, and which sections to avoid. This information exists but is scatterd across Rate My Professors, Reddit threads, and word-of-mouth - there's no single place to search it up.

-->
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source             | Description                                   | URL or location                                   |
|---|--------------------|-----------------------------------------------|---------------------------------------------------|
| 1 | Rate My Proffessor | Reviews for Proffessor Srinivasan             |https://www.ratemyprofessors.com/professor/2424646
| 2 | Rate My Proffessor | Reviews for Proffessor Bereg                  |https://www.ratemyprofessors.com/professor/462041   
| 3 | r/utdallas         |Best Prof for CS 4347- Database Systems?       |https://www.reddit.com/r/utdallas/comments/fq4kd6/best_prof_for_cs_4347_database_systems/
| 4 | r/utdallas         |Best CS 2336 professor                         |https://www.reddit.com/r/utdallas/comments/77gzmm/best_cs_2336_professor/
| 5 | Rate My Proffessor |Reviews for Prof. Omar Hamdy                   |https://www.ratemyprofessors.com/professor/2727867
| 6 | Rate My Proffessor |Reviews for Prof. Vincent Ng (CS 4365 AI)      | https://www.ratemyprofessors.com/professor/505677
| 7 | Rate My Proffessor |Reviews for Prof. Haim Schweitzer (CS 6364 AI) | https://www.ratemyprofessors.com/professor/182842
| 8 | Rate My Proffessor |Reviews for Prof. Yapeng Tian (CS 4391)        | https://www.ratemyprofessors.com/professor/2822081
| 9 | Rate My Proffessor |Reviews for Prof. Brian Ricks (CS 2336)        |https://www.ratemyprofessors.com/professor/2822326 
| 10 |r/utdallas         |Professor recommendations for CS 3305          |https://www.reddit.com/r/utdallas/comments/nrzf7a/professor_recommendations_for_cs_3305/


---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 300 characters

**Overlap:** 50 characters

**Reasoning:** Most RMP reviews are 2–5 sentences — short, self-contained opinions.
A 300-character chunk captures roughly one full review or one distinct claim (e.g.
"exams are curved" or "attendance is mandatory"). Larger chunks risk merging opinions
about different aspects of a professor into a single embedding, which makes retrieval
less precise. The 50-character overlap ensures that a sentence split across a boundary
is still retrievable from either side — important when a key fact (like a grading
policy) ends up near a chunk edge. Reddit threads are longer but still opinion-dense,
so the same chunk size applies.


---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** `all-MiniLM-L6-v2` via `sentence-transformers` (runs locally,
no API key required)

**Top-k:** 5

**Production tradeoff reflection:** For a real deployment I'd weigh several factors.
`all-MiniLM-L6-v2` is fast and free but has a 256-token context window, which is
fine for short reviews but would truncate longer documents. A model like
`text-embedding-3-small` (OpenAI) offers better accuracy and a longer context window
but adds API cost and latency. If the university had international students writing
reviews in other languages, multilingual support (e.g. `paraphrase-multilingual-MiniLM-L12-v2`)
would matter. For this project's scale and document types, `all-MiniLM-L6-v2` is
the right tradeoff.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question                                                    | Expected answer |
|---|-------------------------------------------------------------|---------------------------------------------------------|
| 1 | What do students say about [PROF 1]'s exam difficulty?      | Curved                                                  
| 2 | Which intro CS professor is most recommended for beginners? | Srinivasan                                              
| 3 | Do any professors curve final grades in the CS department?  | Srinivasan metioned curving her tests and Hamdy does not
| 4 | What feedback do students give about CS advising at UTD?    | Students often describe UTD CS advising as helpful when accessible, but frequently criticize slow response times, high advisor workloads, and occasional inconsistencies in advising guidance.
| 5 | Which CS professor is known for giving detailed feedback on assignments? | Jessica Ouyang

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Chunk boundary splits on key facts. RMP reviews are short, but a grading
   policy or exam style comment might still land across two chunks. If only half the
   context is retrieved, the LLM either misses it or hedges. The 50-character overlap
   is designed to mitigate this, but I'll verify during the chunk inspection step in
   Milestone 3.

2. Professor name variation.** Students refer to professors by last name, first
   name, nickname, or title ("Prof. Smith," "Smith," "Dr. Smith," "John"). The
   embedding model may not link these as the same entity, causing retrieval to miss
   relevant chunks when a query uses a different form than the document. I'll
   normalize names during cleaning and test retrieval with multiple name forms.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
I'll give Claude my Documents section (file types: plain .txt, one file per source)
and my Chunking Strategy section (300 chars, 50 overlap, source metadata required).
I'll ask it to implement two functions: `load_documents(folder_path) -> list[dict]`
that returns `{text, source}` for each file, and `chunk_documents(docs) -> list[dict]`
using LangChain's `CharacterTextSplitter` with my specified parameters. I'll verify
the output by printing 5 random chunks and confirming they're readable, non-empty,
and have correct source metadata attached.

**Milestone 4 — Embedding and retrieval:**
I'll give Claude my Architecture diagram (the embedding and vector store stage) and
ask it to implement `embed_and_store(chunks)` that loads `all-MiniLM-L6-v2`, embeds
each chunk, and stores it in a local ChromaDB collection with source metadata. Then
I'll ask it to implement `retrieve(query, k=5) -> list[dict]` that returns the top-k
chunks with their source names and distance scores. I'll verify by running 3 of my
evaluation questions and checking that returned chunks visibly relate to each question
and have distance scores below 0.5.

**Milestone 5 — Generation and interface:**
I'll give Claude my grounding requirement ("answer from retrieved context only; if
context is insufficient, say so explicitly") and my Gradio interface spec (one text
input, two text outputs: answer and sources). I'll ask it to implement `ask(question)`
that calls `retrieve()`, formats the chunks into a prompt, calls the Groq API, and
returns `{answer, sources}`. I'll verify grounding by asking a question my documents
don't cover and confirming the system declines rather than hallucinating.