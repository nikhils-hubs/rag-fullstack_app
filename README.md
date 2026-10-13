# RAG Full-Stack App
 
A full-stack Retrieval-Augmented Generation (RAG) chat application. It answers questions strictly from a private knowledge base (an e-book on muscle building) using hybrid retrieval, reranking and a grounded LLM prompt, with a React chat interface in front of a FastAPI backend.
 
## Highlights
 
- **End-to-end RAG pipeline**: PDF ingestion, cleaning, chapter-aware chunking, embedding, vector storage, retrieval, reranking and generation.
- **Hybrid search**: dense vector search (Chroma, MMR) combined with sparse keyword search (BM25).
- **Reciprocal Rank Fusion (RRF)** to merge the dense and sparse result lists into one ranking.
- **Multi-query expansion**: an LLM rewrites each user question into five semantically diverse queries to improve recall.
- **Cross-encoder reranking** with `BAAI/bge-reranker-v2-m3` to pick the most relevant chunks.
- **Grounded answers**: the prompt forces the model to answer only from retrieved context and return structured JSON.
- **Optional diagram generation**: the model can request an educational diagram, generated with FLUX.1-schnell.
- **Conversation memory**: a sliding window of recent turns is passed to the model.
- **Modern React UI** built with Vite and Tailwind CSS.
## Tech Stack
 
| Layer | Technologies |
|---|---|
| Frontend | React 19, Vite, Tailwind CSS 4, Axios, Lucide icons |
| Backend | Python 3, FastAPI, Uvicorn, Pydantic |
| RAG framework | LangChain (`langchain-chroma`, `langchain-community`, `langchain-huggingface`, `langchain-text-splitters`) |
| Vector database | ChromaDB (persistent, local) |
| Embeddings | `BAAI/bge-small-en-v1.5` (normalized) via HuggingFace |
| Sparse retrieval | BM25 (`rank-bm25` through LangChain `BM25Retriever`) |
| Reranker | `BAAI/bge-reranker-v2-m3` (FlagEmbedding) |
| LLM | `openai/gpt-oss-120b` served by Groq |
| Image generation | `black-forest-labs/FLUX.1-schnell` via HuggingFace Inference |
| Document parsing | `unstructured` (PDF partitioning) |
 
## Architecture
 
```
                        INGESTION (offline)
  PDF e-book -> unstructured -> chapter JSON -> RecursiveCharacterTextSplitter
                                                (800 chars, 100 overlap)
                                                        |
                                    bge-small-en-v1.5 embeddings
                                                        |
                                         ChromaDB (persisted)
 
                        QUERY (online)
  User question
       |
  Query expansion (LLM -> 5 query variants)
       |
       +--> Dense retrieval: Chroma, MMR (k=10, fetch_k=20), per variant
       +--> Sparse retrieval: BM25 (k=10)
                    |
        Reciprocal Rank Fusion
                    |
        Cross-encoder reranker (top 6 chunks)
                    |
  Grounded prompt + chat history -> LLM -> JSON { answer, generate_image, image_prompt }
                    |
        (optional) FLUX.1-schnell diagram
                    |
  FastAPI  POST /chat  ->  React chat UI
```
 
## How It Works
 
### 1. Ingestion and cleaning
`backend/data_cleaning/cleaning.py` parses the source PDF with `unstructured`, keeps only titles, narrative text and list items, detects chapter headings with a regex, and writes a structured JSON file (`chapter`, `text`) to the knowledge base folder.
 
### 2. Chunking
`backend/rag/rag_structure.py` loads the chapter JSON and splits it with `RecursiveCharacterTextSplitter` (chunk size 800, overlap 100, separators `\n\n`, `\n`, `. `, space). Every chunk carries metadata: a deterministic `chunk_id` (`chapter_<n>_chunk_<m>`), the chapter name and the chapter index.
 
### 3. Embedding and vector storage
Chunks are embedded with `BAAI/bge-small-en-v1.5` (normalized embeddings) and persisted in a ChromaDB collection (`muscle_growth`).
 
### 4. Retrieval
- **Query expansion**: the LLM produces five reworded queries that preserve the original intent.
- **Dense**: Chroma retriever with MMR for relevance plus diversity.
- **Sparse**: BM25 over all chunks for exact keyword matches.
- **RRF**: results from both retrievers are fused by reciprocal rank, `1 / (k + rank)` with `k = 60`.
- **Reranking**: the fused candidates are rescored with a cross-encoder and the top 6 are kept.
### 5. Generation
`backend/prompts/llm_prompt.py` holds a strict system prompt: answer only from context, never guess, simplify when asked, and return only JSON in the schema `{answer, generate_image, image_prompt}`. If the answer is not in the context, the model returns a fixed "not found" message.
 
### 6. API and UI
The FastAPI app exposes `POST /chat` (CORS-enabled for the Vite dev server). The React frontend provides a chat window with user and AI message bubbles, a typing indicator, an empty state, an auto-resizing input, a model selector and an attach button.
 
## Project Structure
 
```
rag-fullstack_app/
├── backend/
│   ├── app.py                  # FastAPI app and /chat endpoint
│   ├── rag/
│   │   ├── rag.py              # Retrieval, RRF, reranker, generation, history
│   │   ├── rag_structure.py    # Chunking, embeddings, Chroma ingestion
│   │   └── bm25.py             # BM25 retriever helper
│   ├── data_cleaning/cleaning.py   # PDF -> chapter JSON
│   ├── prompts/llm_prompt.py   # System prompt and query-expander prompt
│   ├── knowlegde_base/         # Source PDF, markdown and chapter JSON
│   ├── utils/                  # Path and JSON helpers
│   └── requirements.txt
└── Frontend-template/
    ├── src/
    │   ├── components/         # chat, Input and layout components
    │   ├── services/           # Axios API and chat service
    │   └── data/model.js       # Model options
    └── package.json
```
 
## Getting Started
 
### Prerequisites
- Python 3.10+
- Node.js 18+
- A [Groq](https://console.groq.com) API key
- A [HuggingFace](https://huggingface.co/settings/tokens) token (only needed for image generation)
### Backend
 
```bash
git clone https://github.com/nikhils-hubs/rag-fullstack_app.git
cd rag-fullstack_app
 
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
```
 
Create a `.env` file:
 
```env
GROQ_API_KEY=your_groq_key
HF_TOKEN=your_huggingface_token
```
 
Build the vector database (first run only), then start the API from the project root:
 
```bash
python -m backend.rag.rag_structure
mkdir -p generated_image
uvicorn backend.app:app --reload --port 8000
```
 
To try the full hybrid pipeline (query expansion, MMR, BM25, RRF, reranking) in the terminal:
 
```bash
python -m backend.rag.rag
```
 
### Frontend
 
```bash
cd Frontend-template
npm install
npm run dev
```
 
Open http://localhost:5173. The UI calls the API at http://localhost:8000.
 
## API
 
`POST /chat`
 
```json
// request
{ "message": "Why is muscle called the organ of longevity?" }
 
// response
{ "message_to_send": "..." }
```
 
## Roadmap
 
- Wire the full hybrid pipeline (expansion, BM25, RRF, reranker) into the `/chat` endpoint.
- Return source chunks and chapter citations with every answer.
- Per-session conversation memory instead of a global history.
- Streaming responses.
- Retrieval evaluation (recall@k, MRR) and answer-faithfulness checks.
- Dockerize backend and frontend.
