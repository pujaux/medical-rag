import { useState, useRef, useEffect } from "react";

const API_URL = "http://localhost:8002";

const SUGGESTIONS = [
  "What is normal hemoglobin?",
  "What does high glucose mean?",
  "What is urinalysis?",
  "What does low ferritin mean?",
];

/* ── Animated neon bubble canvas ── */
function NeonBubbles() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    let animId;

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener("resize", resize);

    // Blush pink + blush purple — slightly richer than before
    const palette = [
      { r: 255, g: 200, b: 215 }, // warm blush pink
      { r: 245, g: 185, b: 210 }, // mid blush pink
      { r: 220, g: 185, b: 245 }, // blush purple
      { r: 200, g: 170, b: 240 }, // deeper blush purple
      { r: 255, g: 215, b: 228 }, // light petal pink
      { r: 210, g: 180, b: 248 }, // soft lilac
    ];

    const bubbles = Array.from({ length: 11 }, (_, i) => {
      const c = palette[i % palette.length];
      return {
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        r: 32 + Math.random() * 58,
        dx: (Math.random() - 0.5) * 0.35,
        dy: (Math.random() - 0.5) * 0.35,
        phase: Math.random() * Math.PI * 2,
        speed: 0.006 + Math.random() * 0.009,
        color: c,
        hx: -0.3,
        hy: -0.35,
      };
    });

    const drawCornerGlow = (cx, cy, radius, r, g, b) => {
      const grad = ctx.createRadialGradient(cx, cy, 0, cx, cy, radius);
      grad.addColorStop(0, `rgba(${r},${g},${b},0.28)`);
      grad.addColorStop(0.5, `rgba(${r},${g},${b},0.12)`);
      grad.addColorStop(1, `rgba(${r},${g},${b},0)`);
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    };

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // ── Purple corner glows (drawn first, behind bubbles) ──
      drawCornerGlow(0, 0, 300, 160, 110, 220);                                   // top-left purple
      drawCornerGlow(canvas.width, 0, 260, 180, 120, 235);                        // top-right purple
      drawCornerGlow(0, canvas.height, 240, 150, 100, 210);                       // bottom-left purple
      drawCornerGlow(canvas.width, canvas.height, 280, 170, 115, 230);            // bottom-right purple

      // ── Floating bubbles ──
      bubbles.forEach((b) => {
        b.phase += b.speed;
        b.x += b.dx + Math.sin(b.phase * 0.7) * 0.3;
        b.y += b.dy + Math.cos(b.phase * 0.5) * 0.3;

        if (b.x < -b.r) b.x = canvas.width + b.r;
        if (b.x > canvas.width + b.r) b.x = -b.r;
        if (b.y < -b.r) b.y = canvas.height + b.r;
        if (b.y > canvas.height + b.r) b.y = -b.r;

        const { r, g, b: bl } = b.color;
        const pulse = 0.11 + 0.05 * Math.sin(b.phase * 1.5);

        // outer soft halo
        const glow = ctx.createRadialGradient(b.x, b.y, b.r * 0.6, b.x, b.y, b.r * 1.45);
        glow.addColorStop(0, `rgba(${r},${g},${bl},0.13)`);
        glow.addColorStop(1, `rgba(${r},${g},${bl},0)`);
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.r * 1.45, 0, Math.PI * 2);
        ctx.fillStyle = glow;
        ctx.fill();

        // 3D glass body
        const body = ctx.createRadialGradient(
          b.x + b.r * b.hx, b.y + b.r * b.hy, b.r * 0.08,
          b.x, b.y, b.r
        );
        body.addColorStop(0, `rgba(255,255,255,${pulse + 0.28})`);
        body.addColorStop(0.3, `rgba(${r},${g},${bl},${pulse + 0.14})`);
        body.addColorStop(0.75, `rgba(${r},${g},${bl},${pulse + 0.07})`);
        body.addColorStop(1, `rgba(${Math.max(r-25,0)},${Math.max(g-25,0)},${Math.max(bl-25,0)},${pulse + 0.04})`);
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
        ctx.fillStyle = body;
        ctx.fill();

        // rim
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(${r},${g},${bl},${0.22 + 0.1 * Math.sin(b.phase * 2)})`;
        ctx.lineWidth = 0.9;
        ctx.stroke();

        // specular gleam
        const shine = ctx.createRadialGradient(
          b.x + b.r * b.hx * 0.9, b.y + b.r * b.hy * 0.9, 0,
          b.x + b.r * b.hx * 0.9, b.y + b.r * b.hy * 0.9, b.r * 0.34
        );
        shine.addColorStop(0, `rgba(255,255,255,${0.5 + 0.1 * Math.sin(b.phase)})`);
        shine.addColorStop(1, "rgba(255,255,255,0)");
        ctx.beginPath();
        ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
        ctx.fillStyle = shine;
        ctx.fill();
      });

      animId = requestAnimationFrame(draw);
    };

    draw();
    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", resize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: "fixed",
        inset: 0,
        pointerEvents: "none",
        zIndex: 0,
      }}
    />
  );
}

/* ── Main App ── */
export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [expandedSources, setExpandedSources] = useState({});
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async (text) => {
    const question = text || input;
    if (!question.trim()) return;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", text: question }]);
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();

      if (data.is_blocked) {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", text: data.message, blocked: true },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            text: data.answer,
            sources: data.sources,
            blocked: false,
          },
        ]);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Cannot connect to backend. Make sure FastAPI is running on port 8002.",
          blocked: true,
        },
      ]);
    }
    setLoading(false);
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const toggleSources = (i) =>
    setExpandedSources((prev) => ({ ...prev, [i]: !prev[i] }));

  return (
    <div
      className="min-h-screen flex flex-col"
      style={{
        background:
          "linear-gradient(135deg, #fdf0ee 0%, #fff5f5 25%, #f0faf0 55%, #f8f0fe 100%)",
        fontFamily: "'Inter', sans-serif",
      }}
    >
      {/* ── Animated neon bubbles layer ── */}
      <NeonBubbles />

      {/* Header */}
      <div
        className="relative px-6 py-4 flex items-center gap-4"
        style={{
          zIndex: 10,
          background: "rgba(255,255,255,0.55)",
          backdropFilter: "blur(18px)",
          borderBottom: "1px solid rgba(176,111,179,0.18)",
          boxShadow: "0 2px 24px rgba(176,111,179,0.08)",
        }}
      >
        <div
          className="w-10 h-10 rounded-xl flex items-center justify-center text-xl flex-shrink-0"
          style={{
            background:
              "linear-gradient(135deg, #ACD8AA, #B06FB3)",
            boxShadow: "0 4px 16px rgba(176,111,179,0.35)",
          }}
        >
          ⚕
        </div>
        <div>
          <h1
            className="font-bold text-base tracking-tight"
            style={{ color: "#2d1a3e" }}
          >
            Medical Report Q&A
          </h1>
          <p className="text-xs" style={{ color: "#7c6fa0" }}>
            Powered by RAG + Groq LLM (llama-3.3-70b)
          </p>
        </div>
        <div
          className="ml-auto flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium"
          style={{
            background: "rgba(172,216,170,0.2)",
            border: "1px solid rgba(172,216,170,0.5)",
            color: "#2d7a2a",
          }}
        >
          <span
            className="w-1.5 h-1.5 rounded-full animate-pulse"
            style={{ background: "#ACD8AA" }}
          />
          Live
        </div>
      </div>

      {/* Warning bar */}
      <div
        className="relative px-6 py-2 text-xs flex items-center gap-2"
        style={{
          zIndex: 10,
          background: "rgba(255,255,255,0.4)",
          backdropFilter: "blur(10px)",
          borderBottom: "1px solid rgba(176,111,179,0.08)",
          color: "#7a4a10",
        }}
      >
        ⚠️ For educational purposes only. Always consult your doctor for medical
        advice.
      </div>

      {/* Messages area */}
      <div
        className="relative flex-1 overflow-y-auto px-4 py-8 space-y-5 max-w-3xl mx-auto w-full"
        style={{ zIndex: 10 }}
      >
        {/* Empty state */}
        {messages.length === 0 && (
          <div className="text-center mt-12 px-4">
            <div
              className="w-20 h-20 rounded-2xl flex items-center justify-center text-4xl mx-auto mb-5"
              style={{
                background: "linear-gradient(135deg, #ACD8AA, #B06FB3)",
                boxShadow:
                  "0 0 0 8px rgba(176,111,179,0.12), 0 20px 60px rgba(176,111,179,0.3)",
              }}
            >
              ⚕️
            </div>
            <h2
              className="text-2xl font-bold mb-2"
              style={{ color: "#2d1a3e" }}
            >
              Ask about your medical results
            </h2>
            <p className="text-sm mb-8" style={{ color: "#6b7280" }}>
              Get clear explanations of blood tests, lab values, and medical
              terminology
            </p>
            <div className="flex flex-wrap gap-2 justify-center">
              {SUGGESTIONS.map((q) => (
                <button
                  key={q}
                  onClick={() => sendMessage(q)}
                  className="text-xs px-4 py-2 rounded-full transition-all duration-200 hover:scale-105"
                  style={{
                    background: "rgba(255,255,255,0.75)",
                    border: "1px solid rgba(176,111,179,0.25)",
                    color: "#6b21a8",
                    backdropFilter: "blur(12px)",
                    boxShadow: "0 2px 12px rgba(176,111,179,0.1)",
                  }}
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Messages */}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            {/* AI avatar */}
            {msg.role === "assistant" && (
              <div
                className="w-8 h-8 rounded-lg flex items-center justify-center text-sm mr-2 mt-1 flex-shrink-0"
                style={{
                  background: "linear-gradient(135deg, #ACD8AA, #B06FB3)",
                  boxShadow: "0 0 12px rgba(176,111,179,0.4)",
                }}
              >
                ⚕
              </div>
            )}

            <div className="max-w-xl">
              {/* Bubble */}
              <div
                className="rounded-2xl px-4 py-3 text-sm leading-relaxed"
                style={
                  msg.role === "user"
                    ? {
                        background:
                          "linear-gradient(135deg, #B06FB3, #ACD8AA)",
                        color: "#fff",
                        borderBottomRightRadius: "4px",
                        boxShadow: "0 4px 20px rgba(176,111,179,0.35)",
                      }
                    : msg.blocked
                    ? {
                        background: "rgba(254,226,226,0.85)",
                        border: "1px solid rgba(252,165,165,0.5)",
                        color: "#991b1b",
                        borderBottomLeftRadius: "4px",
                      }
                    : {
                        background: "rgba(255,255,255,0.72)",
                        backdropFilter: "blur(20px)",
                        border: "1px solid rgba(176,111,179,0.15)",
                        color: "#2d1a3e",
                        borderBottomLeftRadius: "4px",
                        boxShadow:
                          "0 4px 20px rgba(176,111,179,0.1)",
                      }
                }
              >
                {msg.blocked && <span className="mr-1">🚫</span>}
                <p className="whitespace-pre-wrap">{msg.text}</p>
              </div>

              {/* Sources */}
              {msg.sources && msg.sources.length > 0 && (
                <div className="mt-2 ml-1">
                  <button
                    onClick={() => toggleSources(i)}
                    className="flex items-center gap-1.5 text-xs transition-colors mb-2"
                    style={{ color: "#7c3aed" }}
                  >
                    <span>📚</span>
                    <span>
                      {msg.sources.length} source
                      {msg.sources.length > 1 ? "s" : ""} used
                    </span>
                    <span
                      style={{
                        display: "inline-block",
                        transition: "transform 0.2s",
                        transform: expandedSources[i]
                          ? "rotate(180deg)"
                          : "rotate(0deg)",
                      }}
                    >
                      ▾
                    </span>
                  </button>

                  {expandedSources[i] && (
                    <div className="space-y-2">
                      {msg.sources.map((s, j) => (
                        <div
                          key={j}
                          className="rounded-xl px-3 py-2.5 text-xs"
                          style={{
                            background: "rgba(255,255,255,0.8)",
                            border:
                              "1px solid rgba(176,111,179,0.2)",
                            backdropFilter: "blur(10px)",
                          }}
                        >
                          <div className="flex items-center gap-2 mb-1">
                            <span
                              className="font-medium"
                              style={{ color: "#5b21b6" }}
                            >
                              📄 {s.source}
                            </span>
                            <span
                              className="px-2 py-0.5 rounded-full"
                              style={{
                                background: "rgba(176,111,179,0.15)",
                                color: "#6d28d9",
                                fontSize: "10px",
                              }}
                            >
                              {s.category}
                            </span>
                          </div>
                          {s.content && (
                            <p style={{ color: "#6b7280" }}>
                              {s.content.slice(0, 150)}
                              {s.content.length > 150 ? "…" : ""}
                            </p>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* User avatar */}
            {msg.role === "user" && (
              <div
                className="w-8 h-8 rounded-lg flex items-center justify-center text-sm ml-2 mt-1 flex-shrink-0 font-bold"
                style={{
                  background:
                    "linear-gradient(135deg, #ACD8AA, #B06FB3)",
                  color: "#fff",
                  boxShadow: "0 0 12px rgba(172,216,170,0.4)",
                }}
              >
                P
              </div>
            )}
          </div>
        ))}

        {/* Typing indicator */}
        {loading && (
          <div className="flex justify-start items-start gap-2">
            <div
              className="w-8 h-8 rounded-lg flex items-center justify-center text-sm flex-shrink-0"
              style={{
                background: "linear-gradient(135deg, #ACD8AA, #B06FB3)",
                boxShadow: "0 0 12px rgba(176,111,179,0.35)",
              }}
            >
              ⚕
            </div>
            <div
              className="rounded-2xl px-4 py-3"
              style={{
                background: "rgba(255,255,255,0.72)",
                border: "1px solid rgba(176,111,179,0.15)",
                borderBottomLeftRadius: "4px",
                backdropFilter: "blur(20px)",
              }}
            >
              <div className="flex gap-1 items-center h-4">
                {[0, 150, 300].map((delay) => (
                  <div
                    key={delay}
                    className="w-2 h-2 rounded-full animate-bounce"
                    style={{
                      background: "#B06FB3",
                      animationDelay: `${delay}ms`,
                    }}
                  />
                ))}
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input bar */}
      <div
        className="relative px-4 py-4"
        style={{
          zIndex: 10,
          background: "rgba(255,255,255,0.5)",
          backdropFilter: "blur(18px)",
          borderTop: "1px solid rgba(176,111,179,0.12)",
        }}
      >
        <div className="max-w-3xl mx-auto flex gap-3">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKey}
            placeholder="Ask about your medical results..."
            className="flex-1 rounded-xl px-4 py-3 text-sm outline-none transition-all"
            style={{
              background: "rgba(255,255,255,0.8)",
              border: "1px solid rgba(176,111,179,0.25)",
              color: "#2d1a3e",
              backdropFilter: "blur(10px)",
              boxShadow: "0 2px 12px rgba(176,111,179,0.08)",
            }}
          />
          <button
            onClick={() => sendMessage()}
            disabled={loading || !input.trim()}
            className="px-5 py-3 rounded-xl text-sm font-semibold transition-all duration-200 hover:scale-105 active:scale-95 disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:scale-100"
            style={{
              background: "linear-gradient(135deg, #ACD8AA, #B06FB3)",
              color: "#fff",
              minWidth: "80px",
              boxShadow: "0 4px 20px rgba(176,111,179,0.4)",
            }}
          >
            {loading ? "..." : "Send ➤"}
          </button>
        </div>
        <p
          className="text-center text-xs mt-2"
          style={{ color: "rgba(107,114,128,0.6)" }}
        >
          Built by Puja Rani Bhuyan • Medical RAG System
        </p>
      </div>
    </div>
  );
}