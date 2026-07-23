# Banorte AI Assistant

Asistente bancario experimental construido con FastAPI, Google ADK, Gemini, MCP, Docker y Kubernetes.

## Arquitectura

```text
Cliente
  |
  v
FastAPI
  |
  +--> /health
  +--> /metrics
  +--> /analyze
  +--> /agent/chat
             |
             v
        Google ADK
             |
             v
          Gemini
             |
             v
        MCP Toolset
             |
             +--> consultar_saldo
             +--> bloquear_tarjeta
             +--> consultar_credito
             +--> consultar_estado_tarjeta
```

## Tecnologías

- Python 3.13
- FastAPI
- Google ADK
- Gemini
- Model Context Protocol
- Prometheus
- OpenTelemetry
- Docker
- Kubernetes
- Pytest
- GitHub Actions

## Funcionalidades

- API REST documentada con Swagger.
- Clasificación determinística de solicitudes bancarias.
- Agente conversacional con memoria de sesión.
- Herramientas bancarias expuestas mediante MCP.
- Métricas Prometheus.
- Trazas con OpenTelemetry.
- Manejo controlado de errores y cuota de Gemini.
- Despliegue mediante Docker y Kubernetes.
- Pipeline CI con pruebas y construcción automática.

## Estructura del proyecto

```text
app/
banorte_agent/
mcp_server/
k8s/
tests/
.github/workflows/
Dockerfile
requirements.txt
```

## Configuración local

Crea un archivo `.env` en la raíz del proyecto:

```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=TU_API_KEY
```

El archivo `.env` está excluido del repositorio mediante `.gitignore`.

## Ejecución local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Swagger:

```text
http://localhost:8000/docs
```

## Endpoints

### Estado del servicio

```http
GET /health
```

### Métricas Prometheus

```http
GET /metrics
```

### Análisis determinístico

```http
POST /analyze
```

Ejemplo:

```json
{
  "message": "Perdí mi tarjeta y veo un cargo que no reconozco"
}
```

### Agente ADK con MCP

```http
POST /agent/chat
```

Ejemplo:

```json
{
  "message": "Quiero consultar mi saldo. Mi cliente_id es CLI-1001.",
  "user_id": "demo-user",
  "session_id": null
}
```

## Herramientas MCP

- `consultar_saldo`
- `bloquear_tarjeta`
- `consultar_credito`
- `consultar_estado_tarjeta`

Los datos utilizados por estas herramientas son simulados.

## Pruebas

```powershell
python -m pytest -v
```

Cobertura actual:

- health check;
- análisis de fraude;
- consulta de saldo;
- pruebas directas de las cuatro herramientas MCP.

## Docker

```powershell
docker build -t banorte-ai-assistant:1.5.0 .
docker run --env-file .env -p 8000:8000 banorte-ai-assistant:1.5.0
```

## Kubernetes

```powershell
kubectl apply -f .\k8s\deployment.yaml
kubectl apply -f .\k8s\service.yaml
kubectl rollout status deployment/banorte-ai-assistant
kubectl get pods
kubectl port-forward service/banorte-ai-service 8000:8000
```

## CI/CD

Cada push o pull request ejecuta automáticamente:

1. instalación de dependencias;
2. pruebas con pytest;
3. validación de sintaxis;
4. construcción de la imagen Docker.

Workflow:

```text
.github/workflows/ci.yml
```

## Observabilidad

- Métricas Prometheus.
- Trazas OpenTelemetry.
- Logs estructurados.
- Identificación de solicitudes.
- Manejo controlado de errores HTTP.
- Respuesta `429` cuando se agota la cuota de Gemini.

## Seguridad

- `.env` excluido de Git.
- API key fuera del código fuente.
- Secret de Kubernetes para variables sensibles.
- La API key no se copia en la imagen Docker.
- Datos bancarios exclusivamente simulados.

## Estado del proyecto

MVP funcional con FastAPI, Google ADK, Gemini, MCP, Docker, Kubernetes, Prometheus, OpenTelemetry, Pytest y GitHub Actions.
