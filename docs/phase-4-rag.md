# Phase 4 RAG

## Goal
Add a simple RAG pipeline using Qdrant.

## What this phase includes
- a RAG service
- document ingestion
- text chunking
- local embedding generation
- vector storage in Qdrant
- semantic retrieval
- knowledge search UI

## Why the embedding is simple
For this student MVP, the embedding step uses a local hash-based embedding method.

This is not as strong as a production embedding model, but it is useful because:
- it is free
- it is simple to understand
- it works without extra paid infrastructure
- it keeps the focus on the RAG pipeline itself

Later, this embedding function can be replaced by:
- an embedding API
- a local sentence transformer
- a provider embedding model

## RAG pipeline in this project
1. user adds a knowledge document
2. rag-service splits it into chunks
3. each chunk is turned into a vector
4. vectors are stored in Qdrant
5. user sends a search query
6. rag-service turns the query into a vector
7. Qdrant returns the nearest chunks
8. frontend shows the evidence

## What Phase 4 teaches
- what chunking is
- why embeddings are needed
- what a vector database does
- how retrieval works before LLM generation
- why RAG is retrieval plus generation, not only retrieval

## What is still missing after Phase 4
The system can now retrieve evidence, but it does not yet generate an AI answer from that evidence.
That will happen in Phase 5 with AI orchestration.
