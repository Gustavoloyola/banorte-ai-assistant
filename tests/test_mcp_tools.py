from mcp_server.server import (
    bloquear_tarjeta,
    consultar_credito,
    consultar_estado_tarjeta,
    consultar_saldo,
)


def test_consultar_saldo() -> None:
    result = consultar_saldo("CLI-TEST-1001")

    assert result["cliente_id"] == "CLI-TEST-1001"
    assert result["saldo_disponible"] == 12500.00
    assert result["moneda"] == "MXN"


def test_bloquear_tarjeta() -> None:
    result = bloquear_tarjeta(
        "CLI-TEST-2002",
        "cargo no reconocido",
    )

    assert result["cliente_id"] == "CLI-TEST-2002"
    assert result["estado"] == "bloqueo_preventivo"
    assert result["folio"].startswith("FR-")


def test_consultar_credito() -> None:
    result = consultar_credito("CLI-TEST-3003")

    assert result["elegible"] is True
    assert result["monto_maximo"] == 80000.00


def test_consultar_estado_tarjeta() -> None:
    result = consultar_estado_tarjeta("CLI-TEST-4004")

    assert result["estado"] == "activa"
    assert result["ultimos_cuatro_digitos"] == "1234"
