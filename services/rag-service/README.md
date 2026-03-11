# RAG Service

## What this service does
Indexes emergency documents and retrieves useful context using Qdrant.

## Inputs
- uploaded documents
- retrieval queries

## Outputs
- vectorized knowledge
- retrieved evidence

## Main endpoints
- `GET /health`
- `GET /documents`
- `POST /documents`
- `POST /search`

## Events published
None for now.

## Events consumed
None for now.

## How to run locally
1. install dependencies from `requirements.txt`
2. make sure Qdrant is running on `http://localhost:6333`
3. run `uvicorn app.main:app --reload --port 8004`

## Environment variables
- `QDRANT_URL`
- `QDRANT_COLLECTION_NAME`
- `EMBEDDING_SIZE`
- `CHUNK_SIZE_WORDS`
- `CHUNK_OVERLAP_WORDS`

## Phase 4 note
This service uses a simple local hash-based embedding method for the student MVP.
Later it can be replaced with a stronger embedding model or embedding API.
