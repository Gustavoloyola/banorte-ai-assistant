import sys

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
)
from mcp import StdioServerParameters


mcp_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=["-m", "mcp_server.server"],
        ),
        timeout=30,
    )
)


root_agent = Agent(
    name="banorte_banking_agent",
    model="gemini-flash-latest",
    description=(
        "Agente bancario que consume herramientas externas "
        "mediante Model Context Protocol."
    ),
    instruction="""
Eres un asistente bancario para un MVP simulado.

Interpreta la solicitud del usuario y elige la herramienta MCP adecuada.

Reglas:
- Solicita cliente_id cuando no esté presente.
- Para robo, pérdida o cargos no reconocidos, usa bloquear_tarjeta.
- Las operaciones son simuladas.
- No inventes saldos, folios ni resultados.
- Nunca solicites NIP, CVV, contraseña ni número completo de tarjeta.
- Responde en español y de manera breve.
""",
    tools=[mcp_tools],
)
