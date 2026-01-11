import re
from langchain_community.llms import Ollama


def answer_question(vectorstore, question, k=5):
    docs = vectorstore.similarity_search(question, k=k)

    context_blocks = []
    for i, doc in enumerate(docs):
        context_blocks.append(
            f"[Source {i+1}]\n{doc.page_content}"
        )

    context = "\n\n".join(context_blocks)

    prompt = f"""
You are an academic assistant.

RULES (STRICT):
1. Use ONLY the information contained in the sources below.
2. Every factual claim MUST be followed by an inline citation in the form [Source X].
3. If the sources do not contain sufficient information, respond EXACTLY with:
   "I do not know based on the provided documents."
4. Do NOT use prior knowledge.
5. Write in a precise academic style.

STRUCTURE YOUR ANSWER EXACTLY AS FOLLOWS:

1. Definition / Core statement  
2. Description or mechanism  
3. Key implications or conclusions  
4. Limitations of the available information (if applicable)

Sources:
{context}

Question:
{question}

Answer:
"""

    llm = Ollama(
        model="llama3.1:8b",
        temperature=0.0
    )

    answer = llm.invoke(prompt)

    # 🔒 Academic safety check: require citations
    has_citations = re.search(r"\[Source\s+\d+\]", answer)

    if not has_citations:
        return (
            "The model generated an answer without explicit source citations. "
            "This response has been blocked to maintain academic integrity.",
            docs,
        )

    return answer, docs
