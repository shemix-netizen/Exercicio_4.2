# Exercício 4.2 — Servidor MCP local que consome a API (4.1)

Módulo 3 — Construindo interfaces · Aula 6: MCP

Um servidor **MCP** (Model Context Protocol) que fica na frente da API REST de
TODO list construída no [Exercício 4.1](../Exercicio_4.1). Um LLM não fala HTTP —
ele fala MCP. Este servidor é a **camada do meio**: expõe ferramentas que um
agente pode chamar e as implementa fazendo chamadas HTTP à API 4.1.

```
Agente / LLM  ──MCP──▶  servidor_mcp.py  ──HTTP──▶  API 4.1 (localhost:8000)
```

## Ferramentas expostas

| Ferramenta       | Assinatura                          | O que faz                                   |
| ---------------- | ----------------------------------- | ------------------------------------------- |
| `criar_tarefa`   | `criar_tarefa(titulo: str) -> dict` | faz `POST /tarefas` e devolve a tarefa criada |
| `listar_tarefas` | `listar_tarefas() -> list`          | faz `GET /tarefas` e devolve uma lista        |

## Estrutura

```
.
├── servidor_mcp.py      # servidor MCP (stdio) — tools que chamam a API 4.1
├── cliente_teste.py     # sobe o servidor via stdio e imprime o envelope JSON
├── requirements.txt     # mcp, httpx
├── README.md
└── .autograde-exercise  # conteúdo: 4.2
```

## Como rodar localmente

**Terminal A** — suba a API do 4.1 (reinicie para a loja ficar limpa):

```bash
# no repositório do 4.1
uvicorn app.main:app --port 8000
```

**Terminal B** — neste repositório (4.2):

```bash
pip install -r requirements.txt
python cliente_teste.py
```

Deve imprimir um único envelope JSON no stdout, por exemplo:

```json
{
  "tools": ["criar_tarefa", "listar_tarefas"],
  "criar_resultado": {"id": 1, "titulo": "tarefa via mcp", "concluida": false},
  "listar_resultado": [{"id": 1, "titulo": "tarefa via mcp", "concluida": false}]
}
```

> A API do 4.1 precisa estar no ar em `localhost:8000` durante a validação,
> porque as ferramentas do MCP a chamam. O `id` e o `concluida` só podem vir da
> API REST — é assim que o autograder comprova que a ferramenta realmente chamou
> a API, e não devolveu um valor fixo.

## Reflexão (Aula 6)

No 4.1, quem chama precisa falar HTTP: conhecer o host e a porta, o método
(`POST`/`GET`), a rota `/tarefas`, o formato do corpo JSON e os códigos de status.

No 4.2, o agente só precisa saber que existe uma ferramenta `criar_tarefa(titulo)`.

**O que o MCP escondeu, em uma frase:** o MCP tornou irrelevante para quem chama
todo o protocolo de transporte HTTP da API — host, porta, verbo, rota e formato
do corpo —, deixando visível apenas a intenção (`criar_tarefa`, `listar_tarefas`)
e seus argumentos. Esse é o ganho de abstração da Aula 6.
