# Glossary

## Purpose

This document defines the official terminology used throughout the LLM Data Intelligence System.

The goal is to establish a common language between architecture, documentation, code, and future developments.

Terms defined here should be used consistently across the project.

---

# Architecture Terms

## AI Ecosystem

A collection of reusable AI capabilities, components, services, and applications built around a shared architectural foundation.

The LLM Data Intelligence System represents one of the first major platforms inside this ecosystem.

---

## Platform

The complete technological foundation that provides reusable capabilities for building AI applications.

A platform is composed of:

- core components;
- services;
- infrastructure;
- interfaces;
- applications.

---

## Core

The central layer of the architecture containing fundamental rules, abstractions, interfaces, and shared services.

The Core should remain independent from external technologies.

---

## Module

An independent software component responsible for a specific capability or responsibility.

A module should have:

- clear purpose;
- defined inputs and outputs;
- limited dependencies;
- testability.

---

## Service

A specialized module that provides a specific capability to other components.

Examples:

- Embedding Service;
- LLM Service;
- Retrieval Service.

---

# Data Terms

## Data Source

Any external origin of information consumed by the platform.

Examples:

- PDF files;
- CSV files;
- databases;
- APIs;
- websites;
- documents.

---

## Document

A logical unit of information processed by the platform.

A document may originate from different sources and may contain metadata.

Examples:

- PDF report;
- technical article;
- database record;
- text file.

---

## Chunk

A smaller fragment created from a document during preprocessing.

Chunks are used because language models and vector databases work better with smaller semantic units.

---

## Metadata

Additional information associated with a document or chunk.

Examples:

- source;
- creation date;
- author;
- category;
- identifier.

Metadata helps filtering, organization, and retrieval.

---

# AI and Retrieval Terms

## LLM (Large Language Model)

A language model capable of understanding and generating natural language.

Examples:

- GPT models;
- Claude models;
- Llama models.

---

## LLM Provider

A service or implementation responsible for providing access to a language model.

Examples:

- Groq;
- OpenAI;
- Anthropic;
- Google;
- Local model providers.

The platform should interact with providers through abstractions.

---

## Prompt

A structured instruction provided to an LLM to guide its response generation.

---

## Prompt Engineering

The process of designing, testing, and improving prompts to obtain reliable and controlled outputs.

---

## Embedding

A numerical representation of information that captures semantic meaning.

Embeddings allow comparison of similarity between texts.

---

## Embedding Model

A model responsible for transforming text into vector representations.

Examples:

- multilingual-e5-large;
- BGE;
- OpenAI embeddings.

---

## Vector

A numerical representation generated from embeddings.

Vectors allow semantic comparison and similarity searches.

---

## Vector Store

A system responsible for storing and searching vector representations.

Examples:

- ChromaDB;
- Qdrant;
- Pinecone;
- Weaviate.

---

## Retriever

A component responsible for retrieving relevant information from a knowledge source based on a query.

In RAG systems, the Retriever provides context to the LLM.

---

## RAG (Retrieval-Augmented Generation)

An architecture that combines information retrieval with language generation.

General flow:


User Query

↓

Retriever

↓

Relevant Context

↓

LLM

↓

Generated Response


---

# Pipeline Terms

## Pipeline

A predefined sequence of processing steps.

Example:

Load Data

↓

Process

↓

Generate Embeddings

↓

Store

↓

Retrieve

↓

Generate Response


---

## Workflow

A dynamic process capable of making decisions and selecting different execution paths.

---

## Orchestrator

A component responsible for coordinating multiple services and controlling execution flow.

The Orchestrator does not perform specialized tasks; it manages interaction between components.

---

# Development Terms

## Capability

A functional ability provided by the platform.

Capabilities represent long-term value independent of specific technologies.

Examples:

- Document Ingestion;
- Semantic Search;
- LLM Inference;
- Agent Execution.

---

## Infrastructure

External technologies and systems that support the platform.

Examples:

- databases;
- APIs;
- cloud services;
- storage systems.

---

## Application Layer

The layer responsible for exposing platform capabilities to users.

Examples:

- web applications;
- APIs;
- dashboards;
- interfaces.

---

## Agent

A component capable of reasoning, using tools, accessing information, and executing actions to achieve a defined objective.

---

## Tool

An external capability that an agent can use to perform actions.

Examples:

- database queries;
- APIs;
- calculations;
- search systems.

---

# Project Evolution Terms

## Architecture Decision Record (ADR)

A document that records important technical decisions, including context, alternatives, and consequences.

---

## Roadmap

A strategic plan describing the evolution stages and future capabilities of the platform.

---

## Release

A version of the platform considered stable enough to be delivered or used.

---

# Naming Convention

The project follows these conventions:

- Code identifiers use English.
- Folder names use English.
- Technical documentation uses English terminology when appropriate.
- Explanations and internal discussions may use Portuguese.

Consistency is more important than language choice.

---

# Final Principle

The vocabulary of the project should evolve carefully.

New terms should only be introduced when they represent a meaningful concept or capability.

The goal is clarity, consistency, and long-term maintainability.