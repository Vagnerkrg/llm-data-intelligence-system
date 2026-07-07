# Project Decisions

This document records important technical, architectural, and strategic decisions made during the evolution of the LLM Data Intelligence System.

The purpose of this document is to preserve project context, explain decisions, and support future development.

---

# 2026-07-06

# Decision 01 — Product-Oriented Architecture

## Context

This project will be developed as an AI platform and not as a simple notebook experimentation project.

The objective is to build a complete Data Intelligence solution capable of evolving into a real AI product.

## Decision

The system will follow a modular architecture focused on:

- scalability;
- maintainability;
- reusable components;
- future integrations;
- incremental evolution.

## Reason

A product-oriented architecture allows the platform to grow without requiring major structural changes in the future.

---

# Decision 02 — Initial Modular Architecture

## Decision

The project will be structured using independent modules inside the `src/` directory.

Each module will have a specific responsibility.

Initial architecture:
src/

├── llm/
├── data/
├── preprocessing/
├── embeddings/
├── index/
├── rag/
└── agents/


Responsibilities:

## llm

Responsible for:

- Large Language Model integrations;
- prompt management;
- model communication.

---

## data

Responsible for:

- data loading;
- dataset management;
- input validation.

---

## preprocessing

Responsible for:

- data preparation;
- cleaning processes;
- transformations.

---

## embeddings

Future semantic layer responsible for:

- vector representations;
- semantic understanding.

---

## index

Future search layer responsible for:

- indexing information;
- retrieval optimization.

---

## rag

Future Retrieval-Augmented Generation layer.

Responsible for:

- combining external knowledge with LLM responses;
- contextual retrieval.

---

## agents

Future intelligent automation layer.

Responsible for:

- autonomous workflows;
- tool usage;
- task execution.

---

# Decision 03 — Initial Dataset Domain

## Domain

Retail / E-commerce Intelligence

## Decision

The initial development will use structured sales data from the e-commerce domain.

## Reason

This domain allows the progressive construction of:

- sales analysis;
- business insights;
- natural language queries;
- automated reports;
- semantic search;
- RAG pipelines;
- intelligent agents.

The chosen domain provides a realistic business context for the evolution of the platform.

---

# Decision 04 — Requirements Architecture

## Context

As the AI Ecosystem grows, different projects may require different technology stacks.

## Decision

Dependencies will be separated by responsibility.

Current structure:

requirements/

├── base.txt
├── llm.txt
├── rag.txt
├── dev.txt
├── full.txt
└── lock.txt
~

The root file:
requirements.txt~


will act only as an installation shortcut.

Example:
-r requirements/full.txt


## Reason

This approach allows:

- easier dependency management;
- reduced conflicts;
- scalability across AI projects;
- reproducible environments.

---

# Decision 05 — Environment Reconstruction Strategy

## Context

During the initial setup, dependency organization required adjustments.

## Decision

The environment was reconstructed following a cleaner engineering approach instead of applying temporary fixes.

## Reason

When the foundation is inconsistent, rebuilding the environment creates a more reliable and reproducible base.

The project is still in the initial phase, making this the correct moment to establish standards.

---

# Decision 06 — Data Integrity Principles

The platform follows strict data handling rules.

## Rule 01 — Original Data Protection

The application never modifies the original file uploaded by the user.

All processing must create derived versions.

---

## Rule 02 — Reproducible Analysis

Every query and analysis should be reproducible.

The same input and configuration should generate equivalent results.

---

## Rule 03 — Grounded AI Responses

Every AI response must be based only on the available data and context provided.

The system should avoid unsupported information.

---

## Rule 04 — Exportable Intelligence

Generated analysis should be exportable.

Examples:

- reports;
- summaries;
- insights;
- visualizations.

---

## Rule 05 — Session Stability

Users should be able to start new sessions without affecting system stability.

---

# Decision 07 — Long-Term Product Vision

## Context

The project may evolve from a technical portfolio project into a commercial AI product.

## Decision

Future product exploration may consider two possible directions.

---

# Online Intelligence Platform

A platform focused on:

- research;
- information collection;
- discovery of opportunities;
- generation of solution ideas.

The objective would be helping users explore problems and identify possible solutions.

---

# Private Enterprise Intelligence Solution

A controlled environment focused on:

- company data;
- privacy;
- historical information;
- internal intelligence;
- secure workflows.

This model would prioritize local or private usage for organizations.

---

## Status

Strategic idea for future exploration.

Not part of the current development scope.

Current priority remains:

- technical development;
- architecture;
- validation;
- creation of a solid AI product foundation.

---

# Decision 08 — Product Readiness Future Phase

## Objective

After technical validation, the project may enter a future phase called:

Product Readiness


Possible evaluation areas:

- architecture stabilization;
- testing;
- documentation;
- deployment strategy;
- user experience;
- brand evaluation;
- software protection strategy;
- privacy documentation;
- commercial preparation.

---

## Intellectual Property and Protection Notes

During development, the project will maintain:

- Git history;
- version control;
- technical documentation;
- architecture records;
- development decisions.

These elements create a historical record of project evolution.

Future protection activities may include professional evaluation of:

- trademark registration;
- software registration;
- contracts;
- privacy documentation;
- business structure.

---

## Status

Future planning.

The current priority remains building a technically strong and validated product.

---

# Notes

This document should be updated whenever important architectural, technical, or strategic decisions are made.

The goal is to preserve the reasoning behind the evolution of the LLM Data Intelligence System.

docs/

├── environment.md
│   → Como recriar o ambiente

├── architecture.md
│   → Como o sistema funciona

└── project-decisions.md
    → Por que as decisões foram tomadas



    # Decision 09 — Initial Data Loading Layer

## Context

The first functional component of the platform was the data loading layer.

## Decision

The project will use a dedicated data loader module responsible for accessing raw datasets without modifying original files.

Implementation:

src/data/data_loader.py


## Validation

The Olist orders dataset was successfully loaded into a Pandas DataFrame.

Validation confirmed:

- correct environment configuration;
- correct dataset path;
- successful CSV loading;
- compatibility with Pandas processing.

## Status

Completed.


## 2026-07-07

### Preprocessing determinístico

Foi decidido substituir a conversão automática de datas baseada em inferência por uma abordagem baseada em regras determinísticas.

A etapa de preprocessing agora identifica colunas relacionadas a datas através de padrões de nomenclatura, garantindo:

- maior previsibilidade do pipeline;
- resultados reproduzíveis;
- redução de warnings e comportamentos inesperados;
- melhor compatibilidade com futuras evoluções do sistema.

O componente continua seguindo os princípios definidos:

- não modificar os arquivos originais;
- trabalhar através de cópias dos DataFrames;
- manter cada responsabilidade isolada em módulos independentes;
- permitir evolução incremental da arquitetura.

## 2026-07-07

### Arquitetura da camada LLM

Foi decidido criar uma camada independente para gerenciamento dos modelos de linguagem.

A integração com LLMs será isolada dentro do módulo:

src/llm/

Responsabilidades definidas:

- llm_client.py
  - representar a interface genérica de comunicação com modelos de linguagem;
  - evitar dependência direta do restante da aplicação com um fornecedor específico.

- groq_client.py
  - implementar inicialmente a comunicação com a Groq API;
  - concentrar configurações e chamadas específicas do provedor.

- README.md
  - manter documentação interna sobre decisões, testes e evoluções da camada.

Essa arquitetura permite futuras integrações com diferentes provedores de LLM sem necessidade de alterações nas demais camadas do sistema.

Princípios mantidos:

- baixo acoplamento entre componentes;
- evolução incremental;
- componentes reutilizáveis;
- preparação futura para RAG e agentes inteligentes.

---

## 2026-07-07

## Integração inicial com LLM externa

Foi implementada a primeira camada de integração com modelos de linguagem utilizando Groq API através do LlamaIndex.

A camada LLM foi isolada em módulos independentes dentro de `src/llm/`, permitindo futuras substituições de provedores de modelos sem impacto nas demais camadas da aplicação.

A autenticação foi configurada utilizando variáveis de ambiente através de arquivo `.env`, mantendo informações sensíveis fora do controle de versão.

A primeira chamada ao modelo foi validada com sucesso, confirmando a comunicação entre a aplicação e o serviço externo de LLM.
