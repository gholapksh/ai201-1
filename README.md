# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

     Student reviews of CS professors at the University of Texas at Dallas (UTD). This knowledge is valuable because official sources - course catalogs, department website and professor bios - only describe what a course covers, not what it's actually like to take it. Students need to know whether a professor's exam match the lectures, whethr grades are curved, and which sections to avoid. This information exists but but is scattered across Rate My Professors, Reddit threads, and word-of-mouth - there's no single place to search it. 

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

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


## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
300 characters
**Overlap:**
50 characters
**Why these choices fit your documents:**
Most RMP reviews are 2–5 sentences —
short, self-contained opinions. A 300-character chunk captures roughly one full
review or one distinct claim (e.g. "exams are curved" or "attendance is mandatory").
Larger chunks risk merging opinions about different aspects of a professor into a
single embedding, making retrieval less precise. The 50-character overlap ensures
that a sentence split across a chunk boundary is still retrievable from either side —
important when a key fact like a grading policy lands near a chunk edge. Reddit
threads are longer but still opinion-dense, so the same chunk size applies. HTML
artifacts, navigation text, and repeated site headers were stripped during cleaning
before chunking.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
`all-MiniLM-L6-v2` via `sentence-transformers` (runs locally, no
API key required)
**Production tradeoff reflection:**
`all-MiniLM-L6-v2` is fast, free, and runs
entirely locally with no rate limits, making it ideal for this project. However, it
has a 256-token context window, which is fine for short reviews but would truncate
longer documents. For a real deployment I would weigh several factors: a model like
`text-embedding-3-small` (OpenAI) offers higher accuracy and a longer context window
but adds API cost and latency per query. If UTD has international students writing
reviews in other languages, a multilingual model like
`paraphrase-multilingual-MiniLM-L12-v2` would be worth the tradeoff. For domain-
specific accuracy on academic text, a fine-tuned model on student review data could
outperform a general-purpose one. For this project's scale and document types,
`all-MiniLM-L6-v2` is the right choice.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
You are a helpful assistant for students at UT Dallas.
Answer questions using ONLY the provided course and professor review excerpts.
If the excerpts do not contain enough information to answer the question, say:
"I don't have enough information in my sources to answer that."
Always end your response with a line that says: Sources: [list the source filenames]

**How source attribution is surfaced in the response:**
 Source filenames are
included in two places: the LLM is instructed to list them at the end of its
response, and the `ask()` function also programmatically extracts unique source
names from the retrieved chunks and returns them separately. The Gradio interface
displays both the answer (with inline source citation) and a "Retrieved from" field
listing the source filenames.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about Professor Srinivasan's exam difficulty? | Exams are curved | Mixed opinions — moderately hard, curve mentioned with 50/35/10% weights. Sources: rmp1.txt, rmp2.txt, rmp5.txt | Partially relevant — pulled from multiple professors, not just Srinivasan | Partially accurate |
| 2 | Which intro CS professor is most recommended for beginners? | Srinivasan | Professor Ricks — "one of the best CS professors," fun lectures, straightforward exams. Sources: rmp9.txt, reddit3.txt, reddit4.txt | Relevant — Ricks is well-supported by the docs | Partially accurate — correct given available docs, but expected answer lacked a source |
| 3 | Do any professors curve final grades in the CS department? | Yes — Srinivasan and Hamdy | Yes — Davis and an unnamed professor curve; Khan does not. Sources: reddit3.txt, rmp5.txt, rmp2.txt, rmp9.txt, rmp6.txt | Relevant — multiple curving references retrieved | Partially accurate — confirmed curving exists but named different professors |
| 4 | What feedback do students give about CS advising at UTD? | Helpful but slow, inconsistent | "I don't have enough information in my sources to answer that." | Off-target — retrieved rmp9.txt and rmp5.txt, neither covers advising | Inaccurate — corpus gap, no advising content in any document |
| 5 | Which CS professor is known for giving detailed feedback on assignments? | Jessica Ouyang | Professor Ricks — described as giving "good feedback." Sources: rmp9.txt, rmp6.txt | Partially relevant — best available match in corpus | Inaccurate — Ouyang has no document in the corpus |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** "What feedback do students give about CS advising at UTD?"

**What the system returned:** I don't have enough information in my sources to
answer that." — correctly declined rather than hallucinating.

**Root cause (tied to a specific pipeline stage):** This is a corpus gap at the
Document Ingestion stage. All 10 collected documents are RMP professor reviews and
Reddit threads about specific courses. None of them discuss the CS advising office
or advising experiences. When the retrieval stage ran, the top chunks came from
rmp9.txt and rmp5.txt — professor reviews that happened to contain the word
"accessible" — but the LLM correctly determined those chunks didn't answer the
question. The failure is not in retrieval or generation; it is in document
collection. The evaluation plan included a question that no collected document
could answer.

**What you would change to fix it:** Add 1–2 Reddit threads specifically about
UTD CS advising experiences (search r/utdallas for "advising" or "academic advisor")
and re-embed. With relevant documents in the corpus, retrieval would return on-topic
chunks and the LLM could generate a grounded answer.


---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
Writing the chunking strategy
in planning.md before touching any code forced a concrete decision about chunk size
and overlap before implementation. When it came time to write `chunk_text()`, the
parameters (300 characters, 50 overlap) were already decided and justified — there
was no guessing. This also made it easy to verify the output: the spec said chunks
should capture "one full review or one distinct claim," so during the inspection step
I had a clear standard to check each printed chunk against.

**One way your implementation diverged from the spec, and why:**
The spec listed
the documents folder as `docs/` but the starter repo created a folder called
`documents/`. This required changing `DOCS_FOLDER` in `ingest.py` from `"docs"` to
`"documents"` (later renamed back to `docs`). The spec also listed Jessica Ouyang
as an expected answer in the evaluation plan, but no RMP page was collected for her.
This meant evaluation question 5 could never be answered correctly — a spec error
caught only during evaluation, not during planning.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* My Documents section (10 .txt source files) and Chunking
  Strategy section (300 chars, 50 overlap, source metadata required) from planning.md
- *What it produced:* Complete `ingest.py` with `load_documents()`, `clean_text()`,
  and `chunk_text()` functions, plus a `__main__` block that prints 5 random chunks
- *What I changed or overrode:* The original folder variable was set to `"docs"` but
  my starter repo used `"documents"` — I updated `DOCS_FOLDER` to match. I also
  verified the 5 printed chunks manually and confirmed they were readable before
  moving to embedding.

**Instance 2**
- *What I gave the AI:* My grounding requirement ("answer from retrieved context
  only; decline if insufficient") and Gradio interface spec (one text input, two
  text outputs: answer and sources)
- *What it produced:* Complete `query.py` with a system prompt enforcing grounding,
  and `app.py` with a Gradio interface showing answer and retrieved sources
- *What I changed or overrode:* I verified grounding by testing an out-of-scope
  question (parking at UTD) and confirmed the system declined rather than
  hallucinating. The system prompt language was kept as generated since it produced
  correct refusal behavior on the first test.