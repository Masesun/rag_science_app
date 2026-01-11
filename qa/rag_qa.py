import re
import streamlit as st
from langchain_community.llms import Ollama


def select_relevant_sources(question, docs):
    summaries = []
    for i, doc in enumerate(docs):
        snippet = doc.page_content[:300].replace("\n", " ")
        summaries.append(f"[Source {i+1}] {snippet}")

    summary_text = "\n".join(summaries)

    prompt = f"""
You are an academic assistant.

RULES (STRICT):
1. Use ONLY the information contained in the sources below.
2. Do NOT write full paragraphs.
3. For each section, write MAXIMUM 1–2 bullet points.
4. Each bullet point MUST include an inline citation [Source X].
5. If the sources do not contain sufficient information, respond EXACTLY with:
   "I do not know based on the provided documents."

OUTPUT FORMAT (STRICT):

1. Definition / Core statement:
- ...

2. Description or mechanism:
- ...

3. Key implications or conclusions:
- ...

4. Limitations of the available information:
- ...

Sources:
{summary_text}

Question:
{question}

Answer:
"""


    fast_llm = Ollama(
        model="qwen2.5:3b",
        temperature=0.0,
        num_ctx=1024,
        num_thread=8
    )

    response = fast_llm.invoke(prompt)

    indices = []
    for part in response.split(","):
        part = part.strip()
        if part.isdigit():
            indices.append(int(part) - 1)

    return indices[:2]



@st.cache_data(show_spinner=False)
def cached_llm_answer(question, k):
    vectorstore = st.session_state["vectorstore"]

    initial_docs = vectorstore.similarity_search(question, k=k)
    selected_indices = select_relevant_sources(question, initial_docs)

    docs = [initial_docs[i] for i in selected_indices if i < len(initial_docs)]
    if len(docs) < 2:
        docs = initial_docs[:k]

    context_blocks = []
    for i, doc in enumerate(docs):
        context_blocks.append(
            f"[Source {i+1}]\n{doc.page_content[:1500]}"
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
        temperature=0.0,
        num_ctx=2048,
        num_thread=8
    )

    answer = llm.invoke(prompt)

    if not re.search(r"\[Source\s+\d+\]", answer):
        answer = (
            "The model generated an answer without explicit source citations. "
            "This response has been blocked to maintain academic integrity."
        )

    return answer, docs



def answer_question(question, k=5):
    return cached_llm_answer(question, k)
