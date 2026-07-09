# LLM Data Intelligence System - Architecture

**Current Version:** v0.7  
**Last Update:** 08-07-2026  

---

# 1. Visão Geral

O **LLM Data Intelligence System** é uma plataforma modular de inteligência de dados baseada em:

- Large Language Models (LLMs);
- Retrieval-Augmented Generation (RAG);
- embeddings;
- busca vetorial;
- agentes inteligentes;
- análise estruturada de dados.

O objetivo do sistema é permitir que usuários consultem dados utilizando linguagem natural, combinando conhecimento recuperado, análise estatística e agentes especializados para gerar respostas contextualizadas.

A arquitetura foi projetada pensando em uma evolução progressiva:

**Projeto técnico → Plataforma de inteligência de dados → Produto empresarial baseado em IA**

---

# 2. Evolução Arquitetural

## v0.1 — Fundação Inicial

Implementação da base técnica:

- estrutura modular do projeto;
- carregamento de dados;
- validação;
- pipeline inicial.

---

## v0.5 — RAG Foundation

Implementação das capacidades de recuperação de conhecimento:

- preprocessing;
- geração de embeddings;
- índice vetorial;
- busca semântica;
- recuperação de contexto.

---

## v0.6 — Evaluation & Routing

Evolução da arquitetura:

- avaliação de respostas;
- benchmark de perguntas;
- métricas de recuperação;
- roteamento inicial de consultas.

---

## v0.7 — Hybrid Intelligence Layer (Atual)

O sistema evoluiu de um mecanismo RAG para uma arquitetura híbrida.

Novos componentes:

- Data Analysis Engine;
- Analysis Router;
- Data Analysis Agent;
- Hybrid Query Engine;
- Decision Engine;
- Answer Generator;
- Application Layer.

---

# 3. Visão Arquitetural Atual

Fluxo principal:


            User Question
                  |
                  v
      Intelligence System
      Application Layer
                  |
                  v
      Hybrid Query Engine
                  |
      +-----------+-----------+
      |                       |
      v                       v

    RAG Engine          Analysis Engine
      |                       |
      v                       v

Vector Search          Data Analysis Agent
      |                       |
      +-----------+-----------+
                  |
                  v

          Decision Engine
                  |
                  v

         Answer Generator
                  |
                  v

         Final Response

        
---

# 4. Estrutura Atual de Componentes

## 4.1 Data Layer

Local:

src/data/

Responsável por:

- carregamento dos datasets;
- validação;
- preparação inicial dos dados.

---

## 4.2 Preprocessing Layer

Local:

src/preprocessing/

Responsável por:

- limpeza;
- transformação;
- preparação dos dados para processamento inteligente.

---

## 4.3 Embedding Layer

Local:

Responsável por:

- limpeza;
- transformação;
- preparação dos dados para processamento inteligente.

---

## 4.3 Embedding Layer

Local:

src/embeddings/

Responsável por:

- geração de embeddings;
- representação vetorial dos dados;
- preparação para busca semântica.

---

## 4.4 Vector Index Layer

Local:

src/index/

Responsável por:

- criação do índice vetorial;
- armazenamento dos vetores;
- recuperação por similaridade.

---

## 4.5 RAG Layer

Local:

src/rag/

Responsável por:

- recuperação de documentos;
- geração de contexto;
- integração com LLM.

Componente principal:

query_engine.py

---

# 5. Data Intelligence Layer

## Local:

src/analysis/

Nova camada adicionada na versão v0.7.

Responsável por executar análises estruturadas sobre dados.

Componentes:

dataframe_repository.py
statistics_engine.py
analysis_router.py

Responsabilidades:

- acesso aos datasets;
- operações estatísticas;
- identificação de perguntas analíticas;
- preparação de informações para agentes.

---

# 6. Agent Layer

Local:

src/agents/

Componente atual:

data_analysis_agent.py

Responsável por:

- interpretar perguntas analíticas;
- executar operações nos datasets;
- retornar resultados estruturados.

Primeiro agente especializado do sistema.

---

# 7. Service Layer

Local:

src/services/

Responsável pela orquestração dos serviços inteligentes.


## Hybrid Query Engine

Arquivo:

hybrid_query_engine.py

Responsável por:

- analisar intenção da pergunta;
- escolher fluxo RAG;
- escolher fluxo Analysis;
- combinar respostas híbridas.

Rotas disponíveis:

RAG
Analysis
Hybrid

---

## Decision Engine

Arquivo:

decision_engine.py

Responsável por decidir qual fonte possui a melhor resposta.

Avalia:

- resultado analítico;
- resposta RAG;
- disponibilidade de informação.

---

## Answer Generator

Arquivo:

answer_generator.py

Responsável por transformar resultados internos em respostas compreensíveis.


---

## Response Formatter

Arquivo:

response_formatter.py

Responsável pela padronização da apresentação das respostas.

---

# 8. Application Layer

Local:

src/application/

Componente:

intelligence_system.py

Representa o ponto principal de entrada da aplicação.

Responsabilidades:

- receber perguntas;
- executar o fluxo completo;
- conectar serviços;
- retornar resposta final.


Essa camada prepara o sistema para futuras interfaces:

- Web;
- Mobile;
- API;
- integrações externas.

---

# 9. Estrutura Atual do Projeto

src/

├── agents/
│ └── data_analysis_agent.py
│
├── analysis/
│ ├── dataframe_repository.py
│ ├── statistics_engine.py
│ └── analysis_router.py
│
├── application/
│ └── intelligence_system.py
│
├── data/
│
├── embeddings/
│
├── evaluation/
│
├── index/
│
├── llm/
│
├── preprocessing/
│
├── query/
│
├── rag/
│
├── services/
│ ├── hybrid_query_engine.py
│ ├── decision_engine.py
│ ├── answer_generator.py
│ └── response_formatter.py
│
└── pipeline.py


---

# 10. Dataset Atual

Dataset principal utilizado:

data/raw/olist/

Base utilizada para simulação empresarial.

Inclui:

- clientes;
- pedidos;
- produtos;
- vendedores;
- pagamentos;
- avaliações;
- localização.

---

# 11. Capacidades Implementadas v0.7

## Consulta Analítica

Exemplo:

Quantos produtos existem?
Resposta:
O dataset products possui 32951 registros.

---

## Análise Estatística

Exemplo: 

Qual categoria possui mais produtos?
Resposta:
A categoria com maior quantidade de produtos é 'cama_mesa_banho', com 3029 registros.



---

## Busca Semântica

Exemplo:

Quais produtos aparecem nos dados?

Utilizando:

- embeddings;
- vector search;
- RAG.


---

# 12. Visão de Produto Futuro

A arquitetura está sendo construída considerando uma futura plataforma comercial.


Possíveis canais:

- navegador;
- aplicativo;
- API;
- WhatsApp;
- Email.


Possíveis funcionalidades:

- upload de planilhas;
- atualização automática de dados;
- histórico de consultas;
- dashboards;
- alertas inteligentes;
- integrações empresariais.


Exemplo de uso:

Uma pequena empresa envia uma planilha atualizada de estoque.

O sistema:

1. processa os dados;
2. atualiza sua base de conhecimento;
3. analisa informações;
4. responde perguntas;
5. envia alertas pelos canais configurados.

---

# 13. Próximos Marcos

## v0.8 — Interface Layer

Planejado:

- API;
- autenticação;
- histórico;
- interface web inicial.


---

## v0.9 — Business Intelligence Layer

Planejado:

- dashboards;
- indicadores;
- relatórios automáticos;
- alertas.


---

## v1.0 — AI Data Intelligence Platform

Objetivo:

Transformar a arquitetura atual em uma plataforma completa de inteligência de dados para empresas.


---

# 14. Estratégia de Documentação

A documentação acompanha a evolução do código.

Cada versão deve registrar:

- decisões arquiteturais;
- novos módulos;
- funcionalidades implementadas;
- próximos passos.

Objetivos:

- rastreabilidade técnica;
- documentação de autoria;
- proteção intelectual;
- preparação para comercialização futura.

## API Layer

The system now includes an API presentation layer responsible for exposing intelligence capabilities through HTTP endpoints.

Current flow:

Client
↓
FastAPI Router
↓
Application Layer
↓
IntelligenceSystem
↓
HybridQueryEngine
↓
DecisionEngine
↓
Response

The API layer is responsible for:

* validating incoming requests
* managing dependencies
* formatting responses
* exposing intelligence capabilities externally

---

# Agent Intelligence Architecture Evolution - V1.8

## Overview

A V1.8 introduces the first foundation of an agent-based architecture.

The system evolves from a predefined intelligence pipeline into a modular architecture where agents can coordinate specialized tools.

The objective is to allow future intelligent workflows based on:

- reasoning;
- tool selection;
- task execution;
- specialized capabilities.

---

# Previous Architecture

Before V1.8, the main execution flow was:

User

↓

Intelligence System

↓

Hybrid Query Engine

↓

+----------------+
| |
| RAG Processing |
| |
| Analysis |
| |
+----------------+

↓

Decision Engine

↓

Answer Generation


This architecture successfully combined:

- semantic retrieval;
- structured data analysis;
- response evaluation.

However, execution paths were predefined.

---

# Agent-Based Architecture

V1.8 introduces an agent coordination layer.

New architecture:

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

# Component Responsibilities

## Agent Controller

Responsible for:

- coordinating agent execution;
- managing workflow decisions;
- interacting with available tools;
- preparing future reasoning capabilities.

---

## Agent Registry

Responsible for:

- maintaining available agents;
- supporting agent discovery;
- enabling future specialized agents.

---

## Tool Registry

Responsible for:

- registering available tools;
- exposing capabilities to agents;
- allowing dynamic tool selection.

---

## Tools Layer

Tools represent independent system capabilities.

Examples:

RAG Tool

Analytics Tool

Search Tool

Data Tool


Each tool should:

- have a clear responsibility;
- expose a standardized interface;
- avoid duplicated business logic.

---

# Architectural Evolution

The platform evolution:

RAG Pipeline

↓

Hybrid Intelligence System

↓

Agent-Based Intelligence Platform

↓

Multi-Agent AI Ecosystem


---

# Future Extensions

The architecture prepares the system for:

- Function Calling;
- ReAct Agents;
- Planning systems;
- Multi-agent workflows;
- Autonomous task execution;
- External tool integrations.

---

# V1.8 Current Status

Implemented:

- Agent Controller foundation;
- Agent Registry foundation;
- Tool architecture foundation;
- Analytics Tool integration.

Validation:

71 automated tests passing


The architecture is now prepared for the next evolution phase:
dynamic tool execution and intelligent agent workflows.


