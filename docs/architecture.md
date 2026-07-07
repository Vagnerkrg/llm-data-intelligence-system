Arquitetura modular desde a versão inicial.

Cada responsabilidade será isolada em um módulo independente para facilitar futuras integrações com bancos vetoriais, RAG e agentes inteligentes.

Status do checklist:

🟢 README → ainda não.
🟡 Kanban → ainda não.
🔵 Architecture → SIM ✅

Registrar essas regras.


Regra 01

A aplicação nunca altera o arquivo original enviado pelo usuário.

------------------------

Regra 02

Toda consulta deve ser reproduzível.

------------------------

Regra 03

Toda resposta da IA deve ser baseada apenas nos dados carregados.

------------------------

Regra 04

Toda análise pode ser exportada.

------------------------

Regra 05

O usuário pode iniciar uma nova sessão sem perder estabilidade.

#Mudamos o requeriments.txt para pasta requeriments que vai conter os requerimentos dividos em arquivos para cada parte do projeto. iniciamos assim 


requirements/

base.txt
llm.txt
dev.txt

Não estamos "desistindo" do ambiente. Estamos aplicando um princípio muito usado em engenharia:

Se a base está inconsistente, é mais barato reconstruí-la corretamente do que tentar remendá-la.

Como ainda estamos no início do LLM Data Intelligence System, perderemos apenas alguns minutos e ganharemos uma base muito mais confiável.

O que construiremos hoje

Quando terminar, teremos algo parecido com:

Vamos criar o Ambiente Base IA v1.0

Nossa estrutura ficará assim:

llm-data-intelligence-system/

├── requirements/
│   ├── base.txt
│   ├── llm.txt
│   ├── rag.txt
│   ├── dev.txt
│   └── full.txt
│
├── src/
├── notebooks/
├── docs/
├── tests/
├── .env.example
├── README.md
└── requirements.txt   ← apenas um "atalho"