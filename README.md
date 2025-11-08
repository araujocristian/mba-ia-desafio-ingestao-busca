# Desafio MBA Engenharia de Software com IA - Full Cycle

O projeto consiste em um pipeline completo de Ingestão, Armazenamento e Busca semântica de documentos PDF usando tecnologias modernas de IA:
- Ingestão de PDFs em Postgres (pgvector) via LangChain
- Busca semântica e chat (CLI) usando Google Gemini

Este guia explica como configurar o ambiente, ingerir documentos e executar o chat.

## Pré-requisitos

- macOS, Linux ou WSL2
- Docker e Docker Compose (para o banco Postgres com pgvector)
- Python 3.11+ (recomendado) e `pip`
- Chave da API do Google (Google AI Studio) para usar Gemini

## Subir o Postgres (pgvector) com Docker

O repositório já contém um `docker-compose.yml` que sobe o Postgres 17 com a extensão `pgvector` habilitada automaticamente.

```bash
docker compose up -d
```

Serviços criados:
- `postgres`: banco na porta 5432 (exposta em `localhost:5432`)
- `bootstrap_vector_ext`: job que cria a extensão `vector` no banco `rag`

## Configurar variáveis de ambiente (.env)

Crie um arquivo `.env` na raiz do projeto com as chaves abaixo. Ajuste os valores conforme necessário.

```env
# Chave do Google para embeddings e LLM (Gemini)
GOOGLE_API_KEY=coloque_sua_chave_do_google_aqui

# URL de conexão do Postgres (usando driver psycopg)
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag

# Nome da coleção/tabela do pgvector usada pelo LangChain
PG_VECTOR_COLLECTION_NAME=documentos

# Caminho do PDF a ser ingerido (arquivo local)
PDF_PATH=./meus_pdfs/exemplo.pdf

# Opcional: modelo de embedding (default: models/gemini-embedding-001)
# GOOGLE_EMBEDDING_MODEL=models/gemini-embedding-001
```

Observações:
- O `.env` é lido automaticamente pelos scripts via `python-dotenv`.
- `bootstrap_vector_ext` já cria a extensão `vector` no banco `rag`.

## Instalar dependências (ambiente local)

Recomendado usar um ambiente virtual.

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Ingestão de documentos (PDF)

O script `src/ingest.py` lê o PDF definido em `PDF_PATH`, faz o split do texto, gera embeddings com Gemini e grava no Postgres via `langchain-postgres` (pgvector).

```bash
python src/ingest.py
```

Se tudo correr bem, os vetores serão salvos na coleção definida em `PG_VECTOR_COLLECTION_NAME`.

## Rodar o chat (CLI)

O chat usa busca semântica no Postgres para montar o contexto e responde com o modelo `gemini-2.5-flash`.

```bash
python src/chat.py
```

Digite sua pergunta quando solicitado. Para sair, use `sair`, `exit` ou `quit`.

## Busca programática (opcional)

Você pode chamar a função de busca diretamente em um shell Python:

```bash
python -c 'from src.search import search_prompt; print(search_prompt("Qual é o assunto do documento?"))'
```

## Como funciona (resumo)

- `src/ingest.py`: carrega PDF (PyPDFLoader), faz split (RecursiveCharacterTextSplitter), gera embeddings (GoogleGenerativeAIEmbeddings) e escreve no Postgres (PGVector).
- `src/search.py`: busca top-k chunks similares no Postgres e pede para o LLM (Gemini) responder apenas com base no contexto.
- `src/chat.py`: interface de linha de comando, pergunta ao usuário e exibe a resposta.

## Solução de problemas (Troubleshooting)

- Erro: "Environment variable X is not set"
	- Verifique se o `.env` contém todas: `GOOGLE_API_KEY`, `DATABASE_URL`, `PG_VECTOR_COLLECTION_NAME`, `PDF_PATH`.

- Erro de conexão ao Postgres
	- Confirme `docker compose up -d` e se a porta 5432 está livre. Teste `psql postgresql://postgres:postgres@localhost:5432/rag`.

- Extensão `vector` não encontrada
	- O `docker-compose.yml` já cria a extensão; suba novamente os serviços. Se necessário, execute manualmente: `CREATE EXTENSION IF NOT EXISTS vector;` no banco `rag`.

- Problemas com a chave do Google
	- Verifique `GOOGLE_API_KEY` no `.env` e se o projeto no Google AI Studio tem acesso aos modelos usados.

## Estrutura do projeto

```
.
├─ docker-compose.yml        # Postgres 17 + pgvector
├─ requirements.txt          # Dependências Python
├─ README.md                 # Este guia
└─ src/
	 ├─ ingest.py              # Ingestão do PDF para o pgvector
	 ├─ search.py              # Busca e prompt para o LLM (Gemini)
	 └─ chat.py                # CLI de perguntas e respostas
```