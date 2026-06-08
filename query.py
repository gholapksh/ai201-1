import os
from groq import Groq
from dotenv import load_dotenv
from embed import retrieve

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful assistant for students at UT Dallas.
Answer questions using ONLY the provided course and professor review excerpts.
If the excerpts do not contain enough information to answer the question, say:
"I don't have enough information in my sources to answer that."
Always end your response with a line that says: Sources: [list the source filenames]"""


def ask(question, k=5):
    chunks = retrieve(question, k=k)

    # Build context block from retrieved chunks
    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(f"[{i+1}] (from {chunk['source']})\n{chunk['text']}")
    context = "\n\n".join(context_parts)

    user_message = f"""Here are relevant excerpts from student reviews:

{context}

Question: {question}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.2,
    )

    answer = response.choices[0].message.content
    sources = list(set(chunk["source"] for chunk in chunks))

    return {
        "answer": answer,
        "sources": sources,
        "chunks": chunks
    }


if __name__ == "__main__":
    # Quick grounding test
    result = ask("What do students say about Professor Ricks?")
    print(result["answer"])
    print("\nSources:", result["sources"])

    # Test out-of-scope refusal
    result2 = ask("What is the parking situation at UTD?")
    print("\n---Out of scope test---")
    print(result2["answer"])