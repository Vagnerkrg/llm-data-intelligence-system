# Technical Backlog

## V1.4 / V1.5 - RAG Document Evolution

Melhorias planejadas para evolução da camada de documentos sem alterar a implementação atual.

### 1. Adicionar IDs nos documentos

Objetivo:

Adicionar identificadores únicos aos documentos gerados pelo `DocumentBuilder`.

Motivação:

* Permitir rastreamento da origem dos documentos.
* Facilitar atualização ou remoção de documentos no vector store.
* Melhorar auditoria e controle dos dados recuperados pelo RAG.

Exemplo futuro:

```json
{
    "text": "Produto cadastrado no marketplace...",
    "metadata": {
        "source": "products",
        "type": "product",
        "record_id": 12345
    }
}
```

---

### 2. Melhorar metadata dos documentos

Objetivo:

Expandir as informações armazenadas junto aos documentos semânticos.

Possíveis novos campos:

* dataset de origem;
* identificador do registro;
* data de criação;
* versão do documento;
* informações de processamento.

Exemplo futuro:

```json
{
    "metadata": {
        "source": "products",
        "type": "product",
        "dataset": "olist",
        "version": "1.0",
        "created_at": "2026-07-08"
    }
}
```

Benefícios:

* maior rastreabilidade;
* explicabilidade das respostas;
* melhor gerenciamento do índice vetorial.

---

### 3. Trocar retorno para objeto Document na integração com Vector Store

Objetivo:

Adaptar o formato dos documentos quando o projeto integrar uma camada de armazenamento vetorial.

Estado atual:

```python
{
    "text": "...",
    "metadata": {}
}
```

Possível evolução:

```python
Document(
    page_content="...",
    metadata={}
)
```

Motivação:

Compatibilidade com frameworks e bancos vetoriais utilizados no pipeline RAG.

Essa mudança deve acontecer somente quando a camada de vector store estiver implementada.

---

### 4. Adicionar testes unitários específicos

Objetivo:

Criar cobertura de testes para a camada de dados.

Testes planejados:

```
tests/
├── test_data_loader.py
├── test_validator.py
├── test_document_builder.py
└── test_summary_builder.py
```

Cenários:

* carregamento correto dos datasets;
* validação de dados;
* geração de documentos;
* geração dos resumos analíticos;
* comportamento com datasets vazios ou incompletos.

---

## Status

Itens registrados como backlog.

Nenhuma refatoração será realizada na versão atual.

A implementação atual permanece estável enquanto novas funcionalidades são adicionadas.


## V1.6 - Real Data Intelligence Layer

### Completed

- Added data contracts:
  - DataSource
  - DatasetInfo
  - LoadResult

- Integrated OlistDataLoader with data contracts

- Added data layer tests:
  - test_models.py
  - test_validators.py
  - test_data_loader.py

### Validation

- Full test suite:
  - 49 tests passing

### Next

- Implement Preprocessing Layer