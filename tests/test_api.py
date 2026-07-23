from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_analyze_fraud() -> None:
    response = client.post(
        "/analyze",
        json={
            "message": "Perdí mi tarjeta y veo un cargo que no reconozco"
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["intent"] == "fraude"
    assert body["action"] == "bloquear_tarjeta"
    assert body["result"]["status"] == "bloqueo_preventivo"
    assert body["request_id"]


def test_analyze_balance() -> None:
    response = client.post(
        "/analyze",
        json={"message": "Quiero consultar mi saldo"},
    )

    assert response.status_code == 200

    body = response.json()

    assert body["intent"] == "consulta_saldo"
    assert body["action"] == "consultar_saldo"
