# Scientific RAG App (Local, Free, Academic-Safe)

A fully local, free, and academically safe Retrieval-Augmented Generation (RAG) web application for question answering over scientific documents.

The system allows users to upload scientific materials (PDF, DOCX, TXT) and ask theoretical or analytical questions. All answers are generated **strictly based on the provided documents**, with enforced inline citations and structural constraints.

No external APIs. No token limits. No data leakage.

---

## Key Features

- **Fully local inference**
  - Uses Ollama with locally hosted large language models
  - No OpenAI, no cloud APIs, no usage limits

- **Academic Safe Mode**
  - Answers grounded strictly in uploaded documents
  - Mandatory inline citations (`[Source X]`)
  - Automatic blocking of uncited or hallucinated responses
  - Explicit epistemic fallback when information is missing

- **Structured academic output**
  - Fixed response structure:
    1. Definition / core statement  
    2. Description or mechanism  
    3. Key implications or conclusions  
    4. Limitations of available information  

- **Optimized for CPU**
  - FAISS vector search (offline)
  - Outline-first generation to reduce latency
  - Optional caching for repeated questions

- **Transparent retrieval**
  - Retrieved source fragments are always visible to the user
  - Full auditability of model outputs

---

## Architecture Overview

'''text
User
└─> Streamlit UI
├─ File upload (PDF / DOCX / TXT)
├─ Question input
└─ Answer + retrieved sources
│
▼
Document loaders
│
▼
Text chunking
│
▼
Embeddings (sentence-transformers)
│
▼
FAISS vector store
│
▼
RAG pipeline
│
▼
Local LLM (Ollama)
```

---

## Models Used

### Primary LLM (Answer Generation)
- **LLaMA 3.1 8B** (via Ollama)
  - Used for academically structured answer generation
  - Enforced source grounding and citation constraints
  - Zero-temperature inference for minimal hallucinations

### Auxiliary LLM (Optional, Optimization Layer)
- **Qwen 2.5 7B** (via Ollama)
  - Used optionally for fast relevance estimation and context selection
  - Does not generate final answers
  - Can be disabled without affecting correctness

> The auxiliary model is part of an optional dual-model optimization layer.
> The system remains fully functional with the primary model alone.

---

## Installation

### Requirements

- Python 3.10+
- 8–16 GB RAM recommended
- Windows / Linux / macOS
- Ollama installed locally

---

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/rag_science_app.git
cd rag_science_app
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/Scripts/activate  # Windows (Git Bash)
source venv/bin/activate      # Linux / macOS
```

### 3. Install dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Install Ollama and pull model
Install Ollama from: https://ollama.com
Then pull the required models:
```bash
ollama pull llama3.1:8b qwen2.5:7b
```

---

## Running the Application
```bash
streamlit run app.py
```
The application will open in your browser.

---

## Usage Workflow
1. Upload one or more scientific documents (PDF, DOCX, TXT)
2. Wait for vector database construction (FAISS)
3. Ask a question related only to the uploaded materials
4. Review:
    - Structured academic answer
    - Inline citations
    - Retrieved source fragments

If the answer cannot be derived from the documents, the system will respond with:
```csharp
I do not know based on the provided documents.
```

---

## Academic Safety Mechanisms

The system is designed with **explicit epistemic safeguards** to prevent hallucinations and ungrounded content. Academic safety is enforced at multiple independent layers.

### 1. Retrieval-grounded generation
All answers are generated strictly from document fragments retrieved via FAISS. The language model never operates in an open-book mode.

### 2. Prompt-level epistemic constraints
The generation prompt explicitly enforces the following rules:
- Use only the provided sources
- Do not rely on prior or external knowledge
- Refuse to answer when information is insufficient

### 3. Mandatory inline citations
Every factual statement must be followed by an inline citation in the format: [Source X]


### 4. Programmatic citation validation
After generation, responses are automatically validated using pattern matching.  
If no valid citations are detected, the answer is **blocked at the application level** and replaced with an academic integrity warning.

### 5. Retrieval safety fallback
When optional optimization layers (e.g. auxiliary model–based context selection) return insufficient or empty context, the system automatically falls back to standard FAISS-based retrieval to guarantee adequate source coverage.

All safety mechanisms are implemented **in code**, not delegated to model compliance.

---

## Structured Academic Output

All valid answers follow a fixed academic structure:

1. **Definition / Core statement**  
2. **Description or mechanism**  
3. **Key implications or conclusions**  
4. **Limitations of the available information**

This structure is enforced at the prompt level and is consistent across queries, making outputs suitable for:
- exam preparation,
- structured note-taking,
- academic discussion,
- preliminary literature synthesis.

---

## Outline-First Answer Generation

To improve performance on CPU-only systems, the application uses an **outline-first generation strategy**.

Instead of immediately generating full paragraphs, the model produces:
- short bullet-point outlines,
- one to two points per section,
- each point with explicit citations.

This approach:
- significantly reduces generation time,
- preserves academic correctness,
- produces concise, exam-ready content.

Full narrative expansion can be added later if needed, but is intentionally disabled by default.

---

## Performance Considerations

The system is optimized for correctness and epistemic safety rather than raw speed.

Key design decisions include:
- FAISS for fast, offline vector search
- Context trimming before generation
- Outline-first answer generation
- Optional caching for repeated queries

On CPU-only setups, inference latency is primarily determined by:
- model size,
- output length,
- available CPU cores.

Optional dual-model optimization (fast relevance estimation → accurate answer generation) may improve performance in some environments, but is not guaranteed to reduce latency on all hardware and can be safely disabled.

---

## Limitations

- No OCR support for scanned PDFs
- No persistent vector storage across sessions
- Not optimized for multi-user deployment
- CPU inference may be slow for long-form outputs
- Auxiliary optimization layers may not benefit all hardware configurations

---

## Intended Use Cases

This tool is designed for:

- studying and reviewing scientific literature,
- exam preparation,
- creating structured academic notes,
- teaching and demonstrations of safe RAG systems,
- research prototyping with local models.

It is **not intended** for:
- generating uncited academic content,
- ghostwriting manuscripts,
- replacing critical reading or peer review.

---

## Ethical Use

Users are responsible for adhering to academic integrity standards and institutional policies.  
The tool is designed to assist understanding and synthesis, not to replace scholarly work.

---

## License

This project is provided for research and educational purposes.  
No warranty is provided. Use at your own responsibility.

---

## Acknowledgements

- Ollama  
- LangChain  
- FAISS  
- Sentence-Transformers  
- Streamlit  
