"""Servidor MCP (stdio) — Exercício 4.2 (Aula 6: MCP).

Expõe duas ferramentas que um agente/LLM pode chamar via MCP. Cada ferramenta
traduz a chamada MCP em uma requisição HTTP para a API REST do 4.1, que continua
sendo a fonte do dado.

    Agente / LLM  --MCP-->  este servidor  --HTTP-->  API 4.1 (localhost:8000)
"""

import logging

import httpx
from mcp.server.fastmcp import FastMCP

# Silencia logs do FastMCP e do httpx. O cliente herda o stderr deste processo;
# o autograder funde stderr no stdout e faz json.loads do resultado, então
# qualquer log ("Processing request...", "HTTP Request...") quebraria o parse.
logging.disable(logging.CRITICAL)

API = "http://localhost:8000"

mcp = FastMCP("tarefas-mcp")


@mcp.tool()
def criar_tarefa(titulo: str) -> dict:
    """Cria uma tarefa na API e devolve o objeto criado."""
    resp = httpx.post(f"{API}/tarefas", json={"titulo": titulo}, timeout=10)
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
def listar_tarefas() -> list:
    """Lista todas as tarefas da API e devolve uma lista."""
    resp = httpx.get(f"{API}/tarefas", timeout=10)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    mcp.run()  # transporte stdio por padrão
