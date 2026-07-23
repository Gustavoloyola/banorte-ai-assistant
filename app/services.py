from uuid import uuid4


FRAUD_WORDS = [
    "fraude",
    "robo",
    "robaron",
    "perdí mi tarjeta",
    "perdi mi tarjeta",
    "cargo no reconocido",
    "cargo que no reconozco",
    "compra que no reconozco",
    "no reconozco",
    "yo no hice",
]

BALANCE_WORDS = [
    "saldo",
    "dinero disponible",
    "cuánto dinero tengo",
    "cuanto dinero tengo",
]

CARD_WORDS = [
    "tarjeta",
    "plástico",
    "plastico",
]

CREDIT_WORDS = [
    "crédito",
    "credito",
    "préstamo",
    "prestamo",
    "financiamiento",
]


def detect_intent(message: str) -> str:
    normalized_message = message.lower().strip()

    if any(word in normalized_message for word in FRAUD_WORDS):
        return "fraude"

    if any(word in normalized_message for word in BALANCE_WORDS):
        return "consulta_saldo"

    if any(word in normalized_message for word in CREDIT_WORDS):
        return "credito"

    if any(word in normalized_message for word in CARD_WORDS):
        return "tarjeta"

    return "otro"


def block_card() -> dict[str, str]:
    case_id = f"FR-{str(uuid4())[:8].upper()}"

    return {
        "status": "bloqueo_preventivo",
        "case_id": case_id,
    }


def get_balance() -> dict[str, str | float]:
    return {
        "currency": "MXN",
        "available_balance": 12500.00,
    }


def get_credit_options() -> dict[str, str | float | bool]:
    return {
        "eligible": True,
        "maximum_amount": 80000.00,
        "currency": "MXN",
    }


def get_card_status() -> dict[str, str]:
    return {
        "status": "activa",
        "last_four_digits": "1234",
    }


def execute_action(intent: str) -> tuple[str, dict, str]:
    if intent == "fraude":
        result = block_card()

        return (
            "bloquear_tarjeta",
            result,
            (
                "Se realizó un bloqueo preventivo y se generó el reporte "
                f"{result['case_id']}."
            ),
        )

    if intent == "consulta_saldo":
        result = get_balance()

        return (
            "consultar_saldo",
            result,
            (
                "Tu saldo disponible simulado es de "
                f"${result['available_balance']:,.2f} MXN."
            ),
        )

    if intent == "credito":
        result = get_credit_options()

        return (
            "consultar_credito",
            result,
            (
                "Tienes una oferta de crédito simulada de hasta "
                f"${result['maximum_amount']:,.2f} MXN."
            ),
        )

    if intent == "tarjeta":
        result = get_card_status()

        return (
            "consultar_estado_tarjeta",
            result,
            "Tu tarjeta terminación 1234 se encuentra activa.",
        )

    return (
        "escalar_asesor",
        {"status": "pendiente"},
        "No pude identificar la solicitud. Será canalizada con un asesor.",
    )
