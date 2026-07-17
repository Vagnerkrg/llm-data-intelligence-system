# System Architecture

## Objective

Provide a canonical reference for the current architecture of the LLM Data Intelligence System, including the major layers, responsibilities, and evolution path.

## Context

The system started as a data-oriented RAG pipeline and evolved into a hybrid intelligence platform combining retrieval, structured analytics, agents, planning, evaluation, and self-improvement capabilities.

## Architecture overview

The platform is organized around layered responsibilities:

- Data layer: ingestion, validation, preparation, and storage.
- Intelligence layer: embeddings, vector retrieval, RAG, analysis, and decision support.
- Agent layer: planning, tool selection, execution, feedback, and adaptation.
- Application layer: orchestration of user interaction and business-oriented workflows.

## Current architectural model

```text
User Query
  -> Application Layer
  -> Hybrid Intelligence Layer
  -> Retrieval / Analysis / Agent Execution
  -> Decision and Response Generation
```

## Key decisions

- Modular architecture to preserve maintainability.
- Separation between retrieval and structured analysis.
- Introduce agents as specialized execution components.
- Support autonomous evaluation and self-improvement as future architectural extensions.

## Implementation current state

The repository already contains code under modules such as data, preprocessing, embeddings, index, rag, analysis, agents, llm, and application, which align with the architecture described here.

## Evolution path

The architecture continues to move toward a more autonomous and self-improving platform through the evolution of planning, execution, decision, autonomy, and learning layers.

## Related references

- [architecture_principles.md](architecture_principles.md)
- [adr_index.md](adr_index.md)
- [../ai_intelligence/llm_and_rag.md](../ai_intelligence/llm_and_rag.md)
- [../ai_intelligence/agent_system.md](../ai_intelligence/agent_system.md)
- [../ai_intelligence/self_improvement.md](../ai_intelligence/self_improvement.md)
