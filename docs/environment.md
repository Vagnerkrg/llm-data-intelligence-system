# Environment

## Project Environment

Project:

LLM Data Intelligence System


Python Version:

3.12


Virtual Environment:

venv


Location:

./venv


---

# Development Environment

Operating System:

Windows


Shell:

PowerShell


Development Workflow:

- VS Code
- Python Virtual Environment
- Git Version Control


---

# Core Dependencies

The project uses:

- Python
- Pandas
- NumPy
- Scikit-learn
- Jupyter
- LlamaIndex
- Transformers
- Embedding libraries
- Vector search libraries
- LLM API clients


The dependency structure is organized by responsibility:

requirements/

├── base.txt
├── llm.txt
├── rag.txt
├── dev.txt
├── full.txt
└── lock.txt


The root `requirements.txt` works as an installation shortcut.


---

# Virtual Environment

## Activate Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1

Deactivate Environment
deactivate

Installation

Install dependencies:

pip install -r requirements.txt

Environment Verification

Check Python version:

python --version

Check installed packages:

pip list

Verify project modules:

python -m compileall src/

Development Validation

Interactive validation can be executed through Python:

python

Example:

from src.application.intelligence_system import IntelligenceSystem

system = IntelligenceSystem()

system.ask(
    "Quantos produtos existem?"
)

The application layer validates the complete flow:

User Question

        ↓

Hybrid Query Engine

        ↓

Analysis / RAG

        ↓

Decision Engine

        ↓

Answer Generator

        ↓

Final Response

Project Environment Principles

The environment should remain stable and reproducible.

Development rules:

dependencies should be changed with technical justification;
environment modifications must be documented;
original datasets must remain protected;
generated artifacts must be separated from source data;
changes should preserve project reproducibility.
Current Environment Status

Validated components:

✅ Python environment configured

✅ Virtual environment operational

✅ Dependencies installed

✅ Data loading working

✅ Data preprocessing working

✅ Embeddings generation working

✅ Vector index available

✅ RAG pipeline operational

✅ Data analysis layer operational

✅ Hybrid intelligence flow operational

✅ Application layer validated

Maintenance Guidelines

Future environment changes should include:

documentation update;
dependency review;
compatibility validation;
Git commit history preservation.

The environment is considered part of the project foundation and must evolve together with the architecture.

