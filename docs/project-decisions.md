# Project Decisions

This document records important technical, architectural, and strategic decisions made during the evolution of the **LLM Data Intelligence System**.

The purpose of this document is to preserve project context, explain architectural choices, and maintain a historical record of system evolution.

---

# Decision 01 — Product-Oriented Architecture

## Date

2026-07-06

## Context

The project was defined as an AI platform foundation and not as a simple experimentation notebook.

The objective is to build a reusable Data Intelligence system capable of evolving into real AI applications.

## Decision

The system will follow a modular architecture focused on:

- scalability;
- maintainability;
- reusable components;
- independent evolution;
- future integrations.

## Reason

A product-oriented architecture allows the platform to evolve without requiring major structural redesigns.

---

# Decision 02 — Modular System Architecture

## Decision

The project will use independent modules inside the `src/` directory.

Each module must have a clear responsibility.

Current architecture:

src/

├── data/
├── preprocessing/
├── embeddings/
├── index/
├── rag/
├── analysis/
├── agents/
├── services/
├── llm/
└── application/


## Reason

Clear module boundaries improve maintainability, testing, and future expansion.

---

# Decision 03 — Initial Dataset Domain

## Domain

Retail / E-commerce Intelligence

## Decision

The initial development uses public e-commerce datasets.

Primary dataset:

Olist Dataset

## Reason

The domain enables progressive implementation of:

- business analysis;
- natural language queries;
- semantic search;
- RAG;
- intelligent agents;
- decision support systems.

---

# Decision 04 — Data Access Abstraction

## Context

The system requires controlled and reusable access to datasets.

## Decision

Create a dedicated data access layer.

Implemented:

src/data/

and:

src/analysis/dataframe_repository.py

Responsibilities:

- dataset loading;
- validation;
- controlled access;
- avoiding duplicated loading logic.

## Result

Data consumption became centralized and reusable across intelligence components.

---

# Decision 05 — Deterministic Data Processing

## Context

Automatic inference can generate inconsistent preprocessing behavior.

## Decision

Data transformations must follow deterministic rules.

## Benefits

- predictable pipeline behavior;
- reproducible results;
- easier debugging;
- improved reliability.

---

# Decision 06 — Requirements Architecture

## Context

The AI ecosystem may contain multiple projects with different technological requirements.

## Decision

Dependencies are separated by responsibility.

Structure:

requirements/

├── base.txt
├── llm.txt
├── rag.txt
├── dev.txt
├── full.txt
└── lock.txt

The root:

requirements.txt


acts as an installation shortcut.

## Reason

This improves:

- dependency management;
- reproducibility;
- scalability between projects.

---

# Decision 07 — LLM Abstraction Layer

## Decision

LLM integrations must remain isolated from business logic.

Implementation:

src/llm/

Responsibilities:

- abstract model communication;
- support multiple providers;
- avoid vendor lock-in.

Initial provider:

- Groq API.

## Reason

Future models and providers should be replaceable without modifying the core architecture.

---

# Decision 08 — RAG as an Independent Intelligence Layer

## Context

Knowledge retrieval is a fundamental capability of the platform.

## Decision

RAG is implemented as an independent intelligence layer.

Responsibilities:

- retrieve relevant information;
- provide contextual grounding;
- support natural language answers.

## Reason

Separating retrieval from generation improves flexibility and evaluation.

---

# Decision 09 — Hybrid Intelligence Architecture

## Date

2026-07-08

## Context

Pure RAG is insufficient for quantitative questions.

Structured analysis is required for accurate numerical answers.

## Decision

The system will combine:

- semantic retrieval;
- structured data analysis.

Implemented through:

HybridQueryEngine

The system decides between:

- RAG;
- Analysis;
- Hybrid execution.

## Reason

Different questions require different intelligence strategies.

---

# Decision 10 — Specialized Analysis Agent

## Date

2026-07-08

## Context

Data questions require dedicated analytical execution.

## Decision

Create specialized agents instead of placing all logic inside the application layer.

Implemented:

src/agents/data_analysis_agent.py

Capabilities:

- row counting;
- column inspection;
- category analysis;
- statistical operations.

---

# Decision 11 — Automated Testing as Development Standard

## Context

The project reached a maturity level where architectural evolution requires automated validation.

## Decision

Automated tests become part of the standard development workflow.

Every new module should include automated tests whenever applicable.

## Result

The project established a testing foundation validating:

- analysis components;
- services;
- application layer;
- API layer;
- intelligence workflows.

## Reason

Automated validation increases reliability, reduces regressions, and supports continuous evolution.

---

# Decision 12 — Separate Logging and Metrics Layers

## Date

2026-07-08

## Context

As the system grows, operational information and analytical monitoring data require different responsibilities.

## Decision

Maintain separate layers:

Logging:

- operational events;
- debugging information;
- execution traces.

Metrics:

- structured execution data;
- monitoring;
- evaluation;
- future dashboards.

## Reason

This separation improves scalability and avoids coupling operational logs with analytical data.

---

# Decision 13 — Extend Evaluation Instead of Creating a Separate Monitoring System

## Date

2026-07-08

## Context

The project already contained evaluation components.

Creating an independent monitoring system would duplicate responsibilities.

## Decision

Extend the existing evaluation architecture with monitoring capabilities.

Implemented:

- QualityMonitor;
- EvaluationHistory.

## Reason

Keeping evaluation and monitoring connected maintains architectural cohesion.

---

# Decision 14 — Hybrid Intelligence API Layer

## Context

The system evolved from an internal intelligence pipeline into an application layer.

A standardized external interface became necessary.

## Decision

Introduce a FastAPI-based API layer.

The API exposes intelligence capabilities through standardized contracts.

Architecture:

User Request

↓

FastAPI

↓

Application Layer

↓

Intelligence System

↓

Hybrid Intelligence

↓

Response

## Benefits

- standardized communication;
- easier integrations;
- isolated API responsibilities;
- improved testing.

## Consequence

The API layer must not contain business logic.

Responsibilities:

API Layer:
- validation;
- contracts;
- formatting.

Application Layer:
- orchestration.

Services Layer:
- intelligence execution.

---

# Decision 15 — Centralized Configuration and Error Handling

## Context

Multiple application layers require consistent configuration and error behavior.

## Decision

Adopt centralized configuration management.

Implemented:

- environment variables;
- application settings;
- shared constants;
- centralized exceptions.

## Benefits

- maintainability;
- deployment flexibility;
- consistent API behavior;
- production preparation.

---

# Decision 16 — Request Context Tracking

## Date

2026-07-08

## Context

Multiple intelligence layers require request traceability.

## Decision

Adopt request context tracking using ContextVar.

## Benefits

- request tracing;
- improved debugging;
- observability foundation;
- future monitoring compatibility.

---

# Decision 17 — Response Intelligence Layer

## Date

2026-07-08

## Decision

Internal system outputs must be separated from user-facing responses.

Implemented:

answer_generator.py

response_formatter.py

## Reason

This allows future interfaces:

- web applications;
- APIs;
- mobile applications;
- dashboards.

---

# Decision 18 — Data Intelligence Expansion Architecture

## Context

The system evolved beyond simple data analysis.

A reusable analytical architecture was required.

## Decision

Separate analytical responsibilities into:

DataFrameRepository

↓

AnalyticsEngine

↓

DataIntelligenceService

↓

Agents


## Reason

This improves:

- scalability;
- maintainability;
- reuse of analytical capabilities.

---

# Decision 19 — Intellectual Property and Project History Preservation

## Context

The project represents a long-term engineering asset.

## Decision

Maintain:

- Git history;
- documentation;
- architecture records;
- development decisions;
- version milestones.

## Reason

Historical records preserve technical evolution and support future product development.

---

# Decision 20 — Agent Intelligence Architecture Preparation

## Status

Planning for V1.8

## Context

The next evolution requires moving from response generation into intelligent task execution.

## Decision

Introduce an agent-based architecture with specialized tools.

Future architecture:

User

↓

Agent Controller

↓

Tool Registry

↓

+----------------+
|                |
|  RAG Tool      |
|                |
|  Analytics Tool|
|                |
|  Search Tool   |
|                |
|  Data Tool     |
|                |
+----------------+

↓

Response Generation

## Planned Concepts

- Function Tools;
- Function Calling;
- Agent Layer;
- Query Engine Tools;
- ReAct Agents;
- Tool Registry.

## Reason

Agents allow the system to select capabilities dynamically and execute more complex workflows.

---

# Current Documentation Structure

docs/

├── architecture.md
│ System architecture

├── current_status.md
│ Current implementation status

├── development_log.md
│ Historical evolution

├── roadmap.md
│ Strategic future evolution

└── project-decisions.md
Reasons behind technical decisions

---

# Update Policy

This document should be updated whenever a significant:

- architectural;
- technical;
- strategic;

decision is made.

The objective is preserving the reasoning behind the evolution of the LLM Data Intelligence System.

---

# Decision: Introduce Agent Controller and Tool Registry Architecture

## Date

2026-07-08

## Context

O sistema evoluiu de uma arquitetura baseada em pipeline híbrido,
com componentes especializados de RAG e análise de dados,
para uma plataforma com necessidade de execução dinâmica de capacidades.

A arquitetura existente possuía agentes especializados,
porém a coordenação ainda dependia de fluxos previamente definidos.

Para suportar futuras capacidades agentic,
foi necessário criar uma camada responsável por controlar agentes
e disponibilizar ferramentas de forma organizada.

---

## Decision

Introduzir uma arquitetura baseada em:

- Agent Controller;
- Agent Registry;
- Tool Registry;
- Specialized Tools.

Fluxo definido:

User

↓

Agent Controller

↓

Tool Registry

↓

+----------------+
| |
| RAG Tool |
| |
| Analytics Tool|
| |
| Search Tool |
| |
| Data Tool |
| |
+----------------+

↓

Response Generation



---

## Initial Implementation

Criados:

src/agents/agent_controller.py

src/agents/agent_registry.py

src/agents/tools/


Primeira ferramenta:

src/agents/tools/analytics_tool.py


---

## Reason

A separação entre agentes e ferramentas permite:

- maior modularidade;
- reutilização de capacidades;
- evolução para Function Calling;
- suporte a múltiplos agentes especializados;
- criação de workflows inteligentes.

---

## Architectural Impact

A responsabilidade das camadas passa a ser:

### Agent Controller

Responsável por:

- coordenar execução;
- decidir próximos passos;
- controlar interação com ferramentas.

---

### Tool Registry

Responsável por:

- registrar ferramentas disponíveis;
- permitir descoberta dinâmica;
- fornecer capacidades aos agentes.

---

### Tools

Responsáveis por:

- executar ações específicas;
- encapsular lógica operacional;
- manter interfaces independentes.

---

## Consequence

Novas capacidades inteligentes devem preferencialmente ser adicionadas
como ferramentas especializadas, evitando aumento de complexidade
nos agentes principais.

A arquitetura fica preparada para futuras implementações:

- Function Calling;
- ReAct Agents;
- Planning;
- Multi-Agent Workflows;
- Autonomous Task Execution.







