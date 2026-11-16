# Multi-Agent-Research-System
Multi-agent research system that plans, retrieves, analyzes, and writes cited reports, built with Python, LangChain, LangGraph, RAG, and OpenAI.

# Multi-Agent Research System

An autonomous research assistant that coordinates specialized AI agents to turn a
question into a structured, source-backed report. Built with **Python, LangChain,
LangGraph, Retrieval-Augmented Generation (RAG), and the OpenAI API**.

## Overview
Instead of a single prompt, the system uses a graph of cooperating agents, each
with a focused role. LangGraph manages state and control flow between them, and
RAG grounds the answers in retrieved documents to reduce hallucination.

## How it works
1. **Planner agent**: breaks the research question into sub-tasks.
2. **Retriever agent (RAG)**: embeds and searches a vector store for relevant sources.
3. **Analyst agent**: synthesizes findings and checks them against the retrieved evidence.
4. **Writer agent**: drafts the final report with citations.
5. **Reviewer agent** (optional): critiques the draft and loops back for revision.

## Key features
- Multi-agent orchestration with stateful LangGraph workflows
- RAG pipeline: document loading, chunking, embeddings, vector search
- Source-grounded answers with citations
- Modular agents and tools that are easy to extend or swap
- Configurable OpenAI models via environment variables.
