# AI-Powered Legal Document Drafting System

## Overview

This project is a grounded AI legal drafting workflow designed to process noisy legal documents and generate citation-backed legal summaries and internal memos.

The system focuses on:

* OCR + PDF ingestion
* semantic retrieval
* grounded generation
* evidence traceability
* human-in-the-loop learning
* adaptive drafting improvements

The architecture prioritizes:

* reliability
* inspectability
* modular engineering
* reviewer-friendly transparency

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/legal-ai-system.git

cd legal-ai-system
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create `.env`

```env
GEMINI_API_KEY=your_api_key
```

---

## 4. Run Streamlit Application

```bash
streamlit run streamlit_app.py
```

---

# Run Instructions

## Workflow

### Step 1

Upload a legal PDF document.

### Step 2

System performs:

* OCR
* parsing
* chunking
* embedding generation

### Step 3

User asks a legal drafting/query question.

Example:

```text
What are the notice requirements in this agreement?
```

### Step 4

System retrieves relevant evidence chunks.

### Step 5

Grounded memo is generated with citations.

### Step 6

Operator can:

* inspect evidence
* edit memo
* save corrections

### Step 7

System extracts reusable drafting patterns and injects them into future prompts.

---

# Short Architecture Overview

```text
PDF Upload
    ↓
OCR + Parsing
    ↓
Chunking
    ↓
Embeddings
    ↓
ChromaDB Vector Store
    ↓
Retrieval + Reranking
    ↓
Grounded Memo Generation
    ↓
Evidence Citations
    ↓
Operator Edits
    ↓
Pattern Learning
    ↓
Adaptive Prompt Injection
```

---

# Core Components

| Component              | Purpose                         |
| ---------------------- | ------------------------------- |
| PaddleOCR              | OCR for scanned legal documents |
| PyMuPDF                | PDF parsing                     |
| Gemini Embeddings      | Semantic vector generation      |
| ChromaDB               | Vector storage                  |
| Cross-Encoder Reranker | Retrieval precision improvement |
| Gemini LLM             | Grounded memo generation        |
| SQLite                 | Edit memory storage             |
| Streamlit              | Reviewer-facing UI              |

---

# Assumptions and Tradeoffs

## Assumptions

* Input documents are primarily English legal documents.
* Legal memos are generated only from retrieved evidence.
* Human edits represent useful drafting preferences.
* Retrieval quality is more important than large-scale fine-tuning.

---

## Tradeoffs

### Why Prompt-Based Learning Instead of Fine-Tuning?

Prompt-based adaptive learning was chosen because it:

* reduces infrastructure complexity
* enables rapid iteration
* improves explainability
* avoids expensive model retraining

---

### Why ChromaDB?

ChromaDB was selected because it:

* supports lightweight local deployment
* integrates easily with embeddings
* allows metadata-backed retrieval
* is fast to prototype

---

### Why Single-Document Workflow?

The system intentionally focuses on:

* one document at a time
* grounded memo generation

instead of:

* multi-agent orchestration
* enterprise-scale infrastructure

This keeps the scope realistic while maximizing reliability and inspectability.

---

# Sample Inputs and Outputs

## Sample Input Query

```text
What notice requirements exist in the agreement?
```

---

## Sample Retrieved Evidence

```text
page_2_chunk_5

COMMISSION may terminate this Agreement for its convenience any time,
in whole or part, by giving CONSULTANT thirty-day written notice.
```

---

## Sample Generated Output

```markdown
# Case Fact Summary

The COMMISSION may terminate the agreement with thirty-day written notice
(page_2_chunk_5).

Insurance policies require thirty-day prior cancellation notice
(page_4_chunk_4).
```

---

## Sample Learned Pattern

```json
{
  "pattern": "stronger compliance language",
  "frequency": 3
}
```

---

# Evaluation Approach

The system was evaluated using:

* synthetic legal contracts
* notice clauses
* insurance provisions
* procedural legal language

Evaluation focused on:

| Metric                  | Goal                           |
| ----------------------- | ------------------------------ |
| OCR Accuracy            | Reliable text extraction       |
| Retrieval Precision     | Relevant chunk retrieval       |
| Citation Correctness    | Proper evidence grounding      |
| Hallucination Reduction | Avoid unsupported claims       |
| Learning Adaptation     | Prompt improvement after edits |

---

# Evaluation Results

| Evaluation Area     | Result                                       |
| ------------------- | -------------------------------------------- |
| OCR Extraction      | Successfully extracted scanned legal clauses |
| Retrieval Quality   | Relevant clauses consistently retrieved      |
| Grounding           | Generated outputs cited supporting chunks    |
| Evidence Inspection | Users could inspect supporting evidence      |
| Adaptive Learning   | Editing patterns influenced future prompts   |

---

# Key Strengths

This system demonstrates:

* grounded legal generation
* evidence traceability
* modular architecture
* human-feedback learning
* adaptive prompt engineering
* retrieval-aware drafting

---

# Future Improvements

Potential future enhancements include:

* multi-document reasoning
* clause classification
* confidence scoring
* legal ontology integration
* citation highlighting UI
* automated benchmarking dashboard

---

# Conclusion

This project prioritizes:

* grounded AI generation
* inspectability
* practical engineering
* human-in-the-loop improvement

rather than large-scale infrastructure or complex multi-agent systems.

The result is a focused, reviewer-friendly legal drafting workflow demonstrating reliable retrieval-augmented generation and adaptive drafting behavior.
