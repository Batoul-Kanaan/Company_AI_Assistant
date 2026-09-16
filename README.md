# Company AI Assistant

A fictional-company internal AI assistant built with FastAPI, React, MongoDB, and Qdrant. The system lets user sign in, chat with an AI assistant, query company data, and search ingested internal documentation through a retrieval-augmented generation (RAG) workflow.

## What this project includes

We built and integrated the following capabilities:

- Secure user authentication and signup
  - MongoDB-backed user accounts
  - Password hashing with PBKDF2
  - Bearer token-based API access
  - Login and signup flow in the frontend

- AI assistant backend
  - FastAPI API for chat and internal tools
  - LLM orchestration using Ollama / LangChain-style tool calling
  - Session-aware conversation handling
  - Guardrails for internal response sanitation and user-scoped memory

- Company data support
  - Employee records
  - Ticket management
  - Policy records
  - Document ingestion and file handling

- Knowledge base and RAG
  - PDF ingestion pipeline
  - Text splitting and embeddings
  - Qdrant vector storage
  - Semantic search against company documentation

- Frontend interface
  - Login / sign up page
  - Chat experience for employees
  - Connected to the backend with bearer-token authentication

- Database and storage layers
  - MongoDB for app data and user metadata
  - Qdrant for vectorized document search

## Project structure

```text
company-ai-assistant/
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
├── backend/
│   └── app/
│       ├── agent/
│       ├── auth.py
│       ├── database/
│       ├── evaluation/
│       ├── ingestion/
│       ├── memory/
│       ├── models/
│       ├── routes/
│       ├── tools/
│       ├── main.py
│       └── uploads/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
└── .venv/
```

## Tech stack

- Backend: Python, FastAPI
- Frontend: React, Vite
- Database: MongoDB
- Vector store: Qdrant
- LLM: Ollama / local model integration
- Embeddings: SentenceTransformers-style embedding workflow
- Validation: Pydantic models and schema-driven interfaces

## What we implemented and improved

The project evolved from a basic prototype into a more complete internal assistant with production-minded improvements:

- Added authentication for frontend and backend
- Replaced hardcoded auth with real user storage in MongoDB
- Added signup/login endpoints and JWT-style bearer token handling
- Secured memory by scoping conversation history per user/session
- Hardened the agent by restricting tool output exposure to users
- Added employee directory support through the AI agent
- Improved response-time handling by reducing unnecessary tool calls and early greeting fast path
- Added document ingestion flow for PDFs and semantic search over stored company documentation
- Verified the data pipeline with MongoDB and Qdrant state checks
- Cleaned up the app structure to better reflect the active runtime flow

## Local setup

### 1) Prerequisites

Install the following:

- Python 3.10+
- Node.js 18+
- MongoDB running locally
- Docker installed for Qdrant if you want to run Qdrant in a container
- Optional: Ollama installed and a model available locally

### 2) Clone the repository

```bash
git clone https://github.com/Batoul-Kanaan/Company_AI_Assistant.git
cd Company_AI_Assistant
```

### 3) Set up the Python environment

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On Linux/macOS use:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4) Configure environment variables

Copy the example environment file:

```bash
copy .env.example .env
```

Then review and update values in `.env`:

```env
APP_ENV=development
AUTH_TOKEN_SECRET=replace-with-a-long-random-secret
MONGO_URI=mongodb://localhost:27017
MONGO_DATABASE=company_ai_assistant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=
QDRANT_COLLECTION=company_documents
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### 5) Start infrastructure services

#### MongoDB

Make sure MongoDB is running locally on the default port `27017`.

#### Qdrant

If using Docker:

```bash
docker run --rm -p 6333:6333 qdrant/qdrant
```

If your environment already uses port 6333, set Qdrant to another free port and update `QDRANT_URL` accordingly.

### 6) Run the backend

From the project root:

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- http://127.0.0.1:8000
- Swagger docs: http://127.0.0.1:8000/docs

### 7) Run the frontend

From the project root:

```bash
cd frontend
npm install
npm run dev
```

The frontend will usually run at:

- http://127.0.0.1:5173

## Authentication flow

The app supports:

- `POST /auth/signup`
- `POST /auth/login`
- Protected routes require a bearer token

The frontend stores the token and sends it in the `Authorization` header for secured calls.

## Chat and AI workflow

The main AI interaction happens through the `/chat` endpoint. The backend:

- receives the user message and session ID,
- identifies the correct user context,
- calls the agent,
- executes relevant tools when needed,
- uses the knowledge base to answer internal company questions,
- returns a final user-facing response.

## Document ingestion workflow

The ingestion pipeline supports loading internal PDFs into the system and vectorizing them for search. Typical flow:

1. Upload or reference a PDF document
2. Extract raw text
3. Chunk the content
4. Generate embeddings
5. Store vectors in Qdrant
6. Query relevant company documents during AI responses

## Notes and recommendations

- Keep `AUTH_TOKEN_SECRET` unique and strong in production environments.
- Use a real MongoDB instance and secure credentials in deployment.
- Prefer dedicated environment configuration for production, not the local development defaults.
- Ensure Qdrant is running before any ingestion/search workflow is executed.
- Keep the frontend and backend CORS settings aligned with your deployment URLs.

## Current status

The project is operational in local development and includes:

- frontend login/signup experience,
- secure MongoDB-backed authentication,
- company knowledge-base and document search,
- internal AI chat functionality,
- ticket, employee, and policy features,
- PDF ingestion and vector search integration.

This README is intended to give a practical overview of the project and the setup needed to run it locally.
