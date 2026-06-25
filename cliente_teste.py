"""Cliente de teste — Exercício 4.2.

Sobe o servidor_mcp.py via stdio, exercita as duas ferramentas e imprime no
stdout um ÚNICO envelope JSON (e nada mais). É esse envelope que o autograder lê.

Qualquer log deve ir para o stderr; o stdout carrega só o JSON.
"""

import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def _blocos_json(resultado):
    """Decodifica o JSON de cada bloco textual do resultado."""
    valores = []
    for bloco in resultado.content:
        texto = getattr(bloco, "text", None)
        if texto is None:
            continue
        valores.append(json.loads(texto))
    return valores


def _parse_objeto(resultado):
    """Resultado de uma tool que devolve um objeto (dict)."""
    structured = getattr(resultado, "structuredContent", None)
    if isinstance(structured, dict):
        # FastMCP embrulha retornos não-dict em {"result": ...}.
        if set(structured.keys()) == {"result"}:
            return structured["result"]
        return structured
    return _blocos_json(resultado)[0]


def _parse_lista(resultado):
    """Resultado de uma tool que devolve uma lista.

    Conforme a versão do SDK, a lista pode chegar como structuredContent
    ({"result": [...]}), como um único bloco textual com o array, ou como um
    bloco textual por item. Os três casos são normalizados para uma lista.
    """
    structured = getattr(resultado, "structuredContent", None)
    if isinstance(structured, dict) and "result" in structured:
        return structured["result"]

    valores = _blocos_json(resultado)
    if len(valores) == 1 and isinstance(valores[0], list):
        return valores[0]
    return valores


async def main() -> dict:
    params = StdioServerParameters(command=sys.executable, args=["servidor_mcp.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            nomes = [t.name for t in tools.tools]

            criar = await session.call_tool("criar_tarefa", {"titulo": "tarefa via mcp"})
            listar = await session.call_tool("listar_tarefas", {})

            return {
                "tools": nomes,
                "criar_resultado": _parse_objeto(criar),
                "listar_resultado": _parse_lista(listar),
            }


if __name__ == "__main__":
    print(json.dumps(asyncio.run(main())))
