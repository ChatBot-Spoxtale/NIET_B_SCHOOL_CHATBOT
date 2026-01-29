from llm_model.retriever.universal_retriever import retrieve_chunks
from llm_model.llm.gemini_client import generate_answer
from llm_model.memory.chat_memory import add, get

def rank_chunks(chunks, query):
    q = query.lower().split()

    def score(chunk):
        text = (
            chunk.get("question", "") + " " +
            chunk.get("answer", "") + " " +
            " ".join(chunk.get("keywords", []))
        ).lower()

        overlap = sum(1 for w in q if w in text)

        if "what is" in chunk.get("question", "").lower():
            overlap += 5

        if "clubs and societies" in chunk.get("question", "").lower() and overlap < 3:
            overlap -= 3

        return overlap

    return sorted(chunks, key=score, reverse=True)


def chat(user_query: str):
    add("user", user_query)

    chunks = retrieve_chunks(user_query, top_k=5)

    chunks = rank_chunks(chunks, user_query)

    chunks = chunks[:3]

    if chunks:
        context = "\n\n".join(f"- {c['answer']}" for c in chunks)
    else:
        context = ""

    reply = generate_answer(context, user_query, get())
    add("assistant", reply)

    return reply
