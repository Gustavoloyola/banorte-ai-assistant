import json
import logging
import time
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Response
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Histogram,
    generate_latest,
)

from app.agent_service import execute_agent
from app.models import (
    AgentChatRequest,
    AgentChatResponse,
    MessageRequest,
    MessageResponse,
)
from app.services import detect_intent, execute_action
from app.tracing import configure_tracing


logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("banorte-ai-assistant")

REQUESTS_TOTAL = Counter(
    "banorte_requests_total",
    "Total de solicitudes procesadas",
)

INTENTS_TOTAL = Counter(
    "banorte_intents_total",
    "Total de intenciones detectadas",
    ["intent"],
)

ACTIONS_TOTAL = Counter(
    "banorte_actions_total",
    "Total de acciones ejecutadas",
    ["action"],
)

REQUEST_DURATION = Histogram(
    "banorte_request_duration_seconds",
    "Duración de las solicitudes",
)

AGENT_REQUESTS_TOTAL = Counter(
    "banorte_agent_requests_total",
    "Total de solicitudes procesadas por el agente ADK",
)

AGENT_ERRORS_TOTAL = Counter(
    "banorte_agent_errors_total",
    "Total de errores del agente ADK",
    ["type"],
)

AGENT_REQUEST_DURATION = Histogram(
    "banorte_agent_request_duration_seconds",
    "Duración de las solicitudes del agente ADK",
)

configure_tracing()
tracer = trace.get_tracer("banorte-ai-assistant")

app = FastAPI(
    title="Banorte AI Assistant",
    description="API bancaria con reglas, ADK, Gemini y MCP.",
    version="1.5.0",
)

FastAPIInstrumentor.instrument_app(app)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "status": "ok",
        "application": "Banorte AI Assistant",
        "version": "1.5.0",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/metrics")
def metrics() -> Response:
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.post("/analyze", response_model=MessageResponse)
def analyze_message(request: MessageRequest) -> MessageResponse:
    started_at = time.perf_counter()
    request_id = str(uuid4())

    with tracer.start_as_current_span("detect_intent") as intent_span:
        intent = detect_intent(request.message)
        intent_span.set_attribute("banorte.intent", intent)

    with tracer.start_as_current_span("execute_action") as action_span:
        action, result, response = execute_action(intent)
        action_span.set_attribute("banorte.action", action)

    duration_seconds = time.perf_counter() - started_at

    REQUESTS_TOTAL.inc()
    INTENTS_TOTAL.labels(intent=intent).inc()
    ACTIONS_TOTAL.labels(action=action).inc()
    REQUEST_DURATION.observe(duration_seconds)

    return MessageResponse(
        request_id=request_id,
        message=request.message,
        intent=intent,
        action=action,
        result=result,
        response=response,
    )


@app.post("/agent/chat", response_model=AgentChatResponse)
async def agent_chat(request: AgentChatRequest) -> AgentChatResponse:
    started_at = time.perf_counter()

    try:
        with tracer.start_as_current_span("adk_mcp_agent_execution"):
            session_id, agent_response = await execute_agent(
                message=request.message,
                user_id=request.user_id,
                session_id=request.session_id,
            )

        AGENT_REQUESTS_TOTAL.inc()
        AGENT_REQUEST_DURATION.observe(
            time.perf_counter() - started_at
        )

        return AgentChatResponse(
            session_id=session_id,
            response=agent_response,
        )

    except Exception as exc:
        error_text = str(exc)

        if "RESOURCE_EXHAUSTED" in error_text or "429" in error_text:
            AGENT_ERRORS_TOTAL.labels(type="quota_exceeded").inc()

            logger.error(
                json.dumps(
                    {
                        "event": "agent_request_failed",
                        "type": "quota_exceeded",
                        "user_id": request.user_id,
                    }
                )
            )

            raise HTTPException(
                status_code=429,
                detail=(
                    "La cuota temporal de Gemini se agotó. "
                    "Intenta nuevamente más tarde."
                ),
            ) from exc

        AGENT_ERRORS_TOTAL.labels(type="internal_error").inc()

        raise HTTPException(
            status_code=500,
            detail="Ocurrió un error al ejecutar el agente.",
        ) from exc
