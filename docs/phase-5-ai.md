# Phase 5 AI Orchestration

## Goal
Add a simple AI orchestration layer that combines incident data and retrieved evidence into grounded workflow outputs.

## What this phase includes
- AI orchestrator service
- workflow routing
- context collection
- RAG retrieval reuse
- LLM call when credentials exist
- safe fallback when credentials are missing
- React AI workflow panel

## Why fallback mode exists
This student project should still work even without an active LLM key.
So the orchestrator can run in two modes:
- `llm`
- `fallback`

This keeps the workflow explainable and demo-friendly.

## Workflow pattern
1. collect incident context
2. collect related tasks and notifications
3. retrieve relevant evidence from RAG
4. build a structured prompt
5. call the LLM if configured
6. otherwise use fallback planning logic
7. return structured output to the UI

## First workflow types
- triage
- response_plan
- public_advisory

## What this teaches
- orchestration versus raw prompting
- grounded prompting with evidence
- safe AI fallback design
- workflow-based AI architecture
