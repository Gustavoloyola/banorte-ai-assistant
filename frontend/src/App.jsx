import { useState } from "react";
import "./App.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

function App() {
  const [clienteId, setClienteId] = useState("CLI-5005");
  const [userId, setUserId] = useState("frontend-demo");
  const [sessionId, setSessionId] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [analysis, setAnalysis] = useState(null);

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Hola, soy Banorte AI. Puedo ayudarte a consultar saldo, revisar tu tarjeta, conocer ofertas de crédito o reportar un posible fraude.",
    },
  ]);

  const quickActions = [
    {
      label: "Consultar saldo",
      text: "Quiero consultar mi saldo",
      icon: "$",
    },
    {
      label: "Estado de tarjeta",
      text: "Quiero revisar el estado de mi tarjeta",
      icon: "▣",
    },
    {
      label: "Oferta de crédito",
      text: "Quiero saber si tengo una oferta de crédito",
      icon: "↑",
    },
    {
      label: "Reportar fraude",
      text: "Perdí mi tarjeta y veo un cargo que no reconozco",
      icon: "!",
    },
  ];

  const completeMessage = (text) => {
    const cleanClientId = clienteId.trim();

    if (!cleanClientId) {
      return text;
    }

    return `${text}. Mi cliente_id es ${cleanClientId}.`;
  };

  const sendMessage = async (customMessage = null) => {
    const text = customMessage ?? message;

    if (!text.trim() || loading) {
      return;
    }

    setLoading(true);
    setError("");

    setMessages((current) => [
      ...current,
      {
        role: "user",
        text,
      },
    ]);

    try {
      const response = await fetch(`${API_BASE_URL}/agent/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: completeMessage(text),
          user_id: userId.trim() || "frontend-demo",
          session_id: sessionId.trim() || null,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "No fue posible completar la solicitud."
        );
      }

      if (data.session_id) {
        setSessionId(data.session_id);
      }

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          text: data.response,
        },
      ]);

      setMessage("");
    } catch (requestError) {
      const errorMessage =
        requestError instanceof Error
          ? requestError.message
          : "Ocurrió un error inesperado.";

      setError(errorMessage);

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          text: `No pude completar la operación: ${errorMessage}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const analyzeMessage = async () => {
    if (!message.trim() || loading) {
      return;
    }

    setLoading(true);
    setError("");
    setAnalysis(null);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "No fue posible analizar la solicitud.");
      }

      setAnalysis(data);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Ocurrió un error inesperado."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-symbol">
            <span className="brand-line brand-line-one"></span>
            <span className="brand-line brand-line-two"></span>
            <span className="brand-line brand-line-three"></span>
          </div>

          <div>
            <div className="brand-name">BANORTE</div>
            <div className="brand-ai">AI ASSISTANT</div>
          </div>
        </div>

        <div className="profile-card">
          <div className="profile-avatar">GL</div>

          <div>
            <span className="profile-label">Sesión de demostración</span>
            <strong>Experiencia bancaria inteligente</strong>
          </div>
        </div>

        <section className="sidebar-section">
          <h3>Datos de sesión</h3>

          <label htmlFor="clienteId">Cliente ID</label>
          <input
            id="clienteId"
            value={clienteId}
            onChange={(event) => setClienteId(event.target.value)}
            placeholder="CLI-5005"
          />

          <label htmlFor="userId">Usuario</label>
          <input
            id="userId"
            value={userId}
            onChange={(event) => setUserId(event.target.value)}
            placeholder="frontend-demo"
          />

          <label htmlFor="sessionId">Session ID</label>
          <input
            id="sessionId"
            value={sessionId}
            onChange={(event) => setSessionId(event.target.value)}
            placeholder="Se genera automáticamente"
          />
        </section>

        <section className="sidebar-section">
          <h3>Acciones rápidas</h3>

          <div className="quick-actions">
            {quickActions.map((action) => (
              <button
                key={action.label}
                type="button"
                className="quick-action"
                onClick={() => sendMessage(action.text)}
                disabled={loading}
              >
                <span className="quick-icon">{action.icon}</span>
                <span>{action.label}</span>
              </button>
            ))}
          </div>
        </section>

        <div className="security-note">
          <span className="security-icon">✓</span>
          <div>
            <strong>Entorno seguro</strong>
            <p>Datos simulados para fines demostrativos.</p>
          </div>
        </div>
      </aside>

      <main className="content">
        <header className="topbar">
          <div>
            <span className="eyebrow">BANCA DIGITAL INTELIGENTE</span>
            <h1>¿En qué podemos ayudarte hoy?</h1>
            <p>
              Consulta productos bancarios y ejecuta operaciones simuladas
              mediante inteligencia artificial y herramientas MCP.
            </p>
          </div>

          <div className="topbar-status">
            <span className="status-dot"></span>
            Servicios disponibles
          </div>
        </header>

        <section className="overview">
          <article className="overview-card">
            <span className="overview-icon">API</span>
            <div>
              <small>Backend</small>
              <strong>FastAPI activo</strong>
              <span>Puerto 8001</span>
            </div>
          </article>

          <article className="overview-card">
            <span className="overview-icon">AI</span>
            <div>
              <small>Agente</small>
              <strong>Google ADK</strong>
              <span>Gemini + memoria</span>
            </div>
          </article>

          <article className="overview-card">
            <span className="overview-icon">MCP</span>
            <div>
              <small>Herramientas</small>
              <strong>4 operaciones</strong>
              <span>Servicios bancarios</span>
            </div>
          </article>

          <article className="overview-card">
            <span className="overview-icon">K8S</span>
            <div>
              <small>Infraestructura</small>
              <strong>Kubernetes</strong>
              <span>Imagen 1.5.0</span>
            </div>
          </article>
        </section>

        <section className="workspace">
          <article className="chat-card">
            <div className="card-header">
              <div>
                <span className="card-kicker">ASISTENTE VIRTUAL</span>
                <h2>Conversación bancaria</h2>
              </div>

              <div className="assistant-state">
                <span className={loading ? "pulse-dot loading" : "pulse-dot"}></span>
                {loading ? "Procesando" : "Disponible"}
              </div>
            </div>

            <div className="messages">
              {messages.map((item, index) => (
                <div
                  key={`${item.role}-${index}`}
                  className={`message-row ${item.role}`}
                >
                  {item.role === "assistant" && (
                    <div className="assistant-avatar">B</div>
                  )}

                  <div className={`message ${item.role}`}>
                    <span>
                      {item.role === "assistant" ? "Banorte AI" : "Tú"}
                    </span>
                    <p>{item.text}</p>
                  </div>
                </div>
              ))}

              {loading && (
                <div className="message-row assistant">
                  <div className="assistant-avatar">B</div>
                  <div className="message assistant typing">
                    <span>Banorte AI</span>
                    <div className="typing-dots">
                      <i></i>
                      <i></i>
                      <i></i>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {error && (
              <div className="error-message">
                <strong>No fue posible completar la operación</strong>
                <span>{error}</span>
              </div>
            )}

            <div className="composer">
              <textarea
                value={message}
                onChange={(event) => setMessage(event.target.value)}
                placeholder="Ejemplo: quiero consultar mi saldo..."
                rows="4"
                onKeyDown={(event) => {
                  if (event.key === "Enter" && !event.shiftKey) {
                    event.preventDefault();
                    sendMessage();
                  }
                }}
              ></textarea>

              <div className="composer-footer">
                <span>Enter para enviar · Shift + Enter para nueva línea</span>

                <div className="composer-buttons">
                  <button
                    type="button"
                    className="secondary-button"
                    onClick={analyzeMessage}
                    disabled={loading || !message.trim()}
                  >
                    Analizar intención
                  </button>

                  <button
                    type="button"
                    className="primary-button"
                    onClick={() => sendMessage()}
                    disabled={loading || !message.trim()}
                  >
                    {loading ? "Procesando..." : "Enviar solicitud"}
                  </button>
                </div>
              </div>
            </div>
          </article>

          <aside className="result-card">
            <div className="card-header">
              <div>
                <span className="card-kicker">ANÁLISIS</span>
                <h2>Resultado técnico</h2>
              </div>
            </div>

            {analysis ? (
              <div className="analysis-content">
                <div className="analysis-field">
                  <span>Intención detectada</span>
                  <strong>{analysis.intent}</strong>
                </div>

                <div className="analysis-field">
                  <span>Acción seleccionada</span>
                  <strong>{analysis.action}</strong>
                </div>

                <div className="analysis-field full">
                  <span>Respuesta</span>
                  <strong>{analysis.response || "Sin respuesta"}</strong>
                </div>

                <div className="json-result">
                  <span>Payload</span>
                  <pre>{JSON.stringify(analysis, null, 2)}</pre>
                </div>
              </div>
            ) : (
              <div className="empty-result">
                <div className="empty-icon">◎</div>
                <h3>Sin análisis todavía</h3>
                <p>
                  Escribe una solicitud y selecciona
                  <strong> Analizar intención</strong>.
                </p>
              </div>
            )}

            <div className="technology-list">
              <span>Stack integrado</span>

              <div className="technology-tags">
                <em>FastAPI</em>
                <em>Gemini</em>
                <em>ADK</em>
                <em>MCP</em>
                <em>Prometheus</em>
                <em>OpenTelemetry</em>
              </div>
            </div>
          </aside>
        </section>
      </main>
    </div>
  );
}

export default App;

