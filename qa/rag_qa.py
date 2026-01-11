from langchain_community.llms import Ollama


def answer_question(vectorstore, question, k=5):
    docs = vectorstore.similarity_search(question, k=k)

    context = "\n\n".join(
        f"[Source {i+1}]\n{doc.page_content}"
        for i, doc in enumerate(docs)
    )

    prompt = f"""
You are an academic assistant.
Answer the question STRICTLY using the provided sources.
If the answer is not contained in the sources, say: "I do not know based on the provided documents."

Sources:
{context}

Question:
{question}

Answer (academic, precise):
"""

    llm = Ollama(
        model="llama3.1:8b",
        temperature=0.0
    )

    return llm.invoke(prompt), docs
