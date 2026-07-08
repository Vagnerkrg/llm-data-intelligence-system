# 🚀 LLM Data Intelligence System (RAG + Agents)

## 🎯 Objetivo

Este projeto tem como objetivo construir um sistema completo de **Data Intelligence baseado em LLMs**, integrando análise de dados estruturados, embeddings, bancos de dados vetoriais, arquitetura RAG (Retrieval-Augmented Generation) e agentes inteligentes com ferramentas personalizadas.

O sistema será desenvolvido de forma incremental, simulando um ambiente real de engenharia de software aplicado a Inteligência Artificial.

---

## 🧠 Proposta do Sistema

O sistema permitirá:

- Análise de dados estruturados com Pandas
- Geração de embeddings para representação semântica
- Armazenamento e busca em banco de dados vetorial
- Recuperação de contexto via RAG
- Geração de respostas com LLMs (Groq)
- Criação de agentes inteligentes com ferramentas personalizadas

---

## 🏗️ Arquitetura Inicial

```text
Dados Estruturados (CSV / Pandas)
   ↓
Processamento e Limpeza
   ↓
Embeddings
   ↓
Banco Vetorial
   ↓
RAG (Retrieval-Augmented Generation)
   ↓
LLM (Groq)
   ↓
Agentes Inteligentes
   ↓
Sistema de Resposta

## 📁 Estrutura do Projeto

- `src/` → código principal do sistema  
- `notebooks/` → experimentos e testes  
- `data/` → datasets  
- `models/` → modelos e artefatos  
- `requirements.txt` → dependências  
- `.gitignore` → arquivos ignorados  
- `README.md` → documentação do projeto  

##Estrutura do projeto em foco v0,1

                LLM Data Intelligence System


        Data Layer
             |
             |
   ---------------------
   |                   |
Structured Data    Knowledge Base
(Pandas/SQL)       (Embeddings)
   |                   |
   |              Vector Database
   |                   |
   -------> Intelligence Layer
                    |
                  RAG
                    |
                  LLM
                    |
                Agent Layer
                    |
               Applications


##Estrutura do projeto em foco Atuallização v0.2

                    USER QUESTION
                         |
                         v
                 QueryRouter
                         |
                         v
              +----------------+
              | Domain Routing |
              +----------------+
                         |
                         v
              Metadata Filtering
                         |
                         v
                Vector Retrieval
                         |
              +----------+----------+
              |                     |
        score suficiente       score baixo
              |                     |
              v                     v
        usa contexto        busca global
              |
              v
          Prompt Template
              |
              v
             LLM
              |
              v
          Final Answer