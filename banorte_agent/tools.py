from uuid import uuid4


def consultar_saldo(cliente_id: str) -> dict:
    """Consulta un saldo simulado."""
    return {
        "cliente_id": cliente_id,
        "saldo_disponible": 12500.00,
        "moneda": "MXN",
        "estado": "consulta_exitosa",
    }


def bloquear_tarjeta(cliente_id: str, motivo: str) -> dict:
    """Realiza un bloqueo preventivo simulado."""
    folio = f"FR-{str(uuid4())[:8].upper()}"

    return {
        "cliente_id": cliente_id,
        "estado": "bloqueo_preventivo",
        "motivo": motivo,
        "folio": folio,
    }


def consultar_credito(cliente_id: str) -> dict:
    """Consulta una oferta de crédito simulada."""
    return {
        "cliente_id": cliente_id,
        "elegible": True,
        "monto_maximo": 80000.00,
        "moneda": "MXN",
        "estado": "oferta_disponible",
    }


def consultar_estado_tarjeta(cliente_id: str) -> dict:
    """Consulta el estado simulado de una tarjeta."""
    return {
        "cliente_id": cliente_id,
        "ultimos_cuatro_digitos": "1234",
        "estado": "activa",
    }
