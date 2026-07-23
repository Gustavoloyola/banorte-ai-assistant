from uuid import uuid4

from mcp.server.fastmcp import FastMCP


mcp = FastMCP("banorte-banking-tools")


@mcp.tool()
def consultar_saldo(cliente_id: str) -> dict:
    """Consulta el saldo disponible simulado de un cliente."""
    return {
        "cliente_id": cliente_id,
        "saldo_disponible": 12500.00,
        "moneda": "MXN",
        "estado": "consulta_exitosa",
    }


@mcp.tool()
def bloquear_tarjeta(cliente_id: str, motivo: str) -> dict:
    """Realiza un bloqueo preventivo simulado de tarjeta."""
    folio = f"FR-{str(uuid4())[:8].upper()}"

    return {
        "cliente_id": cliente_id,
        "estado": "bloqueo_preventivo",
        "motivo": motivo,
        "folio": folio,
    }


@mcp.tool()
def consultar_credito(cliente_id: str) -> dict:
    """Consulta una oferta de crédito simulada para un cliente."""
    return {
        "cliente_id": cliente_id,
        "elegible": True,
        "monto_maximo": 80000.00,
        "moneda": "MXN",
        "estado": "oferta_disponible",
    }


@mcp.tool()
def consultar_estado_tarjeta(cliente_id: str) -> dict:
    """Consulta el estado simulado de una tarjeta."""
    return {
        "cliente_id": cliente_id,
        "ultimos_cuatro_digitos": "1234",
        "estado": "activa",
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
