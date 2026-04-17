import { useState, useRef, useCallback, useEffect } from "react";

const NODES = [
  // Internacional
  { id: "ai-act", label: "AI Act UE", layer: "internacional", x: 500, y: 60, color: "#6366f1" },
  // Federal Vigente
  { id: "lgpd", label: "LGPD\nLei 13.709/2018", layer: "federal-vigente", x: 200, y: 180, color: "#0ea5e9" },
  { id: "eca-digital", label: "ECA Digital\nLei 15.211/2025", layer: "federal-vigente", x: 500, y: 180, color: "#0ea5e9" },
  { id: "nr1", label: "NR-1\nRisco Psicossocial", layer: "federal-vigente", x: 800, y: 180, color: "#0ea5e9" },
  // Federal Tramitando
  { id: "pl2338", label: "PL 2338/2023\nMarco IA", layer: "federal-tramitando", x: 150, y: 320, color: "#f59e0b" },
  { id: "pl4-2025", label: "PL 4/2025\nLivro VI CC Digital", layer: "federal-tramitando", x: 380, y: 320, color: "#f59e0b" },
  { id: "pl4675", label: "PL 4675/2025\nMercados Digitais", layer: "federal-tramitando", x: 610, y: 320, color: "#f59e0b" },
  { id: "plp152", label: "PLP 152/2025\nResponsab. Plataformas", layer: "federal-tramitando", x: 840, y: 320, color: "#f59e0b" },
  { id: "plp74", label: "PLP 74/2026\nGovernança Digital", layer: "federal-tramitando", x: 1050, y: 250, color: "#f59e0b" },
  { id: "pl278", label: "REDATA\nPL 278/2026", layer: "federal-tramitando", x: 1050, y: 350, color: "#f59e0b" },
  // Apensados PL 2338
  { id: "apens-identidade", label: "Identidade Digital", layer: "apensados", x: 0, y: 450, color: "#8b5cf6" },
  { id: "apens-vieses", label: "Vieses Algorítmicos", layer: "apensados", x: 110, y: 450, color: "#8b5cf6" },
  { id: "apens-escrita", label: "Escrita Humana", layer: "apensados", x: 220, y: 450, color: "#8b5cf6" },
  { id: "apens-autoral", label: "Autoral IA", layer: "apensados", x: 330, y: 450, color: "#8b5cf6" },
  { id: "apens-selo", label: "Selo Conteúdo\nSintético", layer: "apensados", x: 0, y: 530, color: "#8b5cf6" },
  { id: "apens-saude", label: "Saúde Mental", layer: "apensados", x: 110, y: 530, color: "#8b5cf6" },
  { id: "apens-marca", label: "Marca d'Água", layer: "apensados", x: 220, y: 530, color: "#8b5cf6" },
  // Estadual
  { id: "pr-lei", label: "Paraná\nLei 22.324/2024", layer: "estadual", x: 700, y: 450, color: "#10b981" },
  { id: "pa-vazio", label: "Pará\n(vazio normativo)", layer: "estadual", x: 870, y: 450, color: "#6b7280" },
  // Produto
  { id: "et-advisory", label: "Et Alii Advisory", layer: "produto", x: 400, y: 640, color: "#ec4899" },
  { id: "et-tech", label: "Et Alii Tech", layer: "produto", x: 560, y: 640, color: "#ec4899" },
  { id: "et-academy", label: "Et Alii Academy", layer: "produto", x: 720, y: 640, color: "#ec4899" },
];

const EDGES = [
  { from: "ai-act", to: "pl2338", label: "inspira" },
  { from: "ai-act", to: "eca-digital", label: "ancora" },
  { from: "lgpd", to: "pl2338", label: "complementa" },
  { from: "lgpd", to: "pl4-2025", label: "ancora" },
  { from: "eca-digital", to: "pl2338", label: "ancora" },
  { from: "nr1", to: "pl2338", label: "apensado" },
  { from: "pl2338", to: "apens-identidade", label: "apensado" },
  { from: "pl2338", to: "apens-vieses", label: "apensado" },
  { from: "pl2338", to: "apens-escrita", label: "apensado" },
  { from: "pl2338", to: "apens-autoral", label: "apensado" },
  { from: "pl2338", to: "apens-selo", label: "apensado" },
  { from: "pl2338", to: "apens-saude", label: "apensado" },
  { from: "pl2338", to: "apens-marca", label: "apensado" },
  { from: "ai-act", to: "pr-lei", label: "inspira" },
  { from: "pl2338", to: "et-advisory", label: "oportunidade" },
  { from: "lgpd", to: "et-advisory", label: "oportunidade" },
  { from: "eca-digital", to: "et-tech", label: "oportunidade" },
  { from: "pl278", to: "et-advisory", label: "oportunidade" },
  { from: "plp74", to: "et-tech", label: "oportunidade" },
];

const LAYER_LABELS = {
  "internacional": "Internacional",
  "federal-vigente": "Federal Vigente",
  "federal-tramitando": "Federal Tramitando",
  "apensados": "Apensados PL 2338",
  "estadual": "Estadual",
  "produto": "Produto / Serviço",
};

const NODE_DETAILS = {
  "ai-act": {
    title: "AI Act — União Europeia",
    status: "Vigente (2024–2026 phased)",
    summary: "Primeiro marco regulatório abrangente de IA do mundo. Classificação por risco: proibido, alto, limitado, mínimo. Referência para legislações nacionais.",
    impacto: "Alto — referência direta para PL 2338 e ECA Digital",
  },
  "lgpd": {
    title: "LGPD — Lei Geral de Proteção de Dados",
    status: "Vigente desde 2020",
    summary: "Lei 13.709/2018. Proteção de dados pessoais, consentimento, direitos do titular, ANPD.",
    impacto: "Fundacional — âncora de compliance para todas as instâncias IPII",
  },
  "eca-digital": {
    title: "ECA Digital — Lei 15.211/2025",
    status: "Vigente desde 2025",
    summary: "Proteção de crianças e adolescentes no ambiente digital. Responsabilidade de plataformas. Base para Hubstry CaaS.",
    impacto: "Alto — produto âncora do ecossistema Gonçalves et Alii",
  },
  "nr1": {
    title: "NR-1 — Risco Psicossocial",
    status: "Vigente (Portaria MTE 1.419/2024)",
    summary: "Gestão de riscos psicossociais no trabalho. IA em RH gera obrigação de avaliação. Intersecção crítica com PL 2338.",
    impacto: "Médio-alto — novo vetor de compliance para empresas com IA em RH",
  },
  "pl2338": {
    title: "PL 2338/2023 — Marco Legal da IA",
    status: "Tramitando (Câmara)",
    summary: "Marco regulatório brasileiro de IA. Classificação por risco, responsabilidade civil, transparência, direitos. Texto base aprovado no Senado em 2024.",
    impacto: "Crítico — produto central do LexScan / LexGraph",
  },
  "et-advisory": {
    title: "Et Alii Advisory",
    status: "Produto ativo",
    summary: "Consultoria jurídico-tecnológica. LexScan Diagnóstico, QuantumReady Assessment, BELLUM Dual-Use. Serviço de alto valor agregado.",
    impacto: "Produto — Gonçalves et Alii",
  },
  "et-tech": {
    title: "Et Alii Tech",
    status: "Produto ativo",
    summary: "LexWatch Monitor (assinatura), LexGraph API (B2B), Hubstry CaaS (white label). Receita recorrente.",
    impacto: "Produto — Gonçalves et Alii / Hubstry Deep Tech",
  },
  "et-academy": {
    title: "Et Alii Academy",
    status: "Em estruturação",
    summary: "Formação em Direito Digital, IA e Compliance. Cursos, workshops, certificações. Funil de clientes para Advisory e Tech.",
    impacto: "Produto — Gonçalves et Alii",
  },
};

const CANVAS_W = 1130;
const CANVAS_H = 720;
const NODE_R = 48;

function getNodeCenter(node) {
  return { x: node.x + NODE_R, y: node.y + NODE_R };
}

export default function LexGraph() {
  const [selected, setSelected] = useState(null);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [zoom, setZoom] = useState(1);
  const [dragging, setDragging] = useState(false);
  const [dragStart, setDragStart] = useState(null);
  const svgRef = useRef(null);

  const handleWheel = useCallback((e) => {
    e.preventDefault();
    setZoom((z) => Math.min(2.5, Math.max(0.3, z - e.deltaY * 0.001)));
  }, []);

  useEffect(() => {
    const el = svgRef.current;
    if (!el) return;
    el.addEventListener("wheel", handleWheel, { passive: false });
    return () => el.removeEventListener("wheel", handleWheel);
  }, [handleWheel]);

  const onMouseDown = (e) => {
    if (e.target === svgRef.current || e.target.tagName === "svg") {
      setDragging(true);
      setDragStart({ x: e.clientX - pan.x, y: e.clientY - pan.y });
    }
  };
  const onMouseMove = (e) => {
    if (dragging && dragStart) {
      setPan({ x: e.clientX - dragStart.x, y: e.clientY - dragStart.y });
    }
  };
  const onMouseUp = () => { setDragging(false); setDragStart(null); };

  const selectedNode = selected ? NODES.find((n) => n.id === selected) : null;
  const details = selected ? NODE_DETAILS[selected] : null;

  return (
    <div style={{ background: "#0f172a", minHeight: "100vh", fontFamily: "Inter, sans-serif", color: "#e2e8f0" }}>
      {/* Header */}
      <div style={{ padding: "16px 24px", borderBottom: "1px solid #1e293b", display: "flex", alignItems: "center", gap: 16 }}>
        <div>
          <h1 style={{ margin: 0, fontSize: 20, fontWeight: 700, color: "#f1f5f9" }}>LexGraph</h1>
          <p style={{ margin: 0, fontSize: 12, color: "#64748b" }}>Arquitetura Regulatória Digital Brasileira · abr/2026 · Gonçalves et Alii</p>
        </div>
        <div style={{ marginLeft: "auto", display: "flex", gap: 8 }}>
          {Object.entries(LAYER_LABELS).map(([key, label]) => {
            const node = NODES.find((n) => n.layer === key);
            return (
              <div key={key} style={{ display: "flex", alignItems: "center", gap: 4, fontSize: 11, color: "#94a3b8" }}>
                <div style={{ width: 10, height: 10, borderRadius: "50%", background: node?.color || "#666" }} />
                {label}
              </div>
            );
          })}
        </div>
      </div>

      <div style={{ display: "flex", height: "calc(100vh - 65px)" }}>
        {/* Canvas */}
        <svg
          ref={svgRef}
          style={{ flex: 1, cursor: dragging ? "grabbing" : "grab", background: "#0f172a" }}
          onMouseDown={onMouseDown}
          onMouseMove={onMouseMove}
          onMouseUp={onMouseUp}
          onMouseLeave={onMouseUp}
        >
          <defs>
            <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
              <path d="M0,0 L0,6 L8,3 z" fill="#334155" />
            </marker>
          </defs>
          <g transform={`translate(${pan.x},${pan.y}) scale(${zoom})`}>
            {/* Layer bands */}
            {[
              { y: 30, h: 100, label: "Internacional", color: "#1e1b4b" },
              { y: 148, h: 108, label: "Federal Vigente", color: "#0c2340" },
              { y: 284, h: 108, label: "Federal Tramitando", color: "#1c1404" },
              { y: 418, h: 130, label: "Apensados / Estadual", color: "#150c2e" },
              { y: 608, h: 90, label: "Produto", color: "#1a0a1a" },
            ].map((band) => (
              <rect key={band.y} x={-20} y={band.y} width={CANVAS_W + 40} height={band.h}
                fill={band.color} rx={4} opacity={0.5} />
            ))}

            {/* Edges */}
            {EDGES.map((e, i) => {
              const from = NODES.find((n) => n.id === e.from);
              const to = NODES.find((n) => n.id === e.to);
              if (!from || !to) return null;
              const fc = getNodeCenter(from);
              const tc = getNodeCenter(to);
              const mx = (fc.x + tc.x) / 2;
              const my = (fc.y + tc.y) / 2;
              return (
                <g key={i}>
                  <line x1={fc.x} y1={fc.y} x2={tc.x} y2={tc.y}
                    stroke="#334155" strokeWidth={1.5} markerEnd="url(#arrow)" opacity={0.6} />
                  <text x={mx} y={my - 4} fill="#475569" fontSize={9} textAnchor="middle">{e.label}</text>
                </g>
              );
            })}

            {/* Nodes */}
            {NODES.map((node) => {
              const cx = node.x + NODE_R;
              const cy = node.y + NODE_R;
              const isSelected = selected === node.id;
              const lines = node.label.split("\n");
              return (
                <g key={node.id} style={{ cursor: "pointer" }} onClick={() => setSelected(node.id === selected ? null : node.id)}>
                  <circle cx={cx} cy={cy} r={NODE_R}
                    fill={node.color + "22"}
                    stroke={isSelected ? node.color : node.color + "88"}
                    strokeWidth={isSelected ? 3 : 1.5} />
                  {lines.map((line, i) => (
                    <text key={i} x={cx} y={cy + (i - (lines.length - 1) / 2) * 13}
                      fill={isSelected ? "#f1f5f9" : "#cbd5e1"}
                      fontSize={10} textAnchor="middle" fontWeight={isSelected ? 600 : 400}>
                      {line}
                    </text>
                  ))}
                </g>
              );
            })}
          </g>
        </svg>

        {/* Sidebar */}
        {selectedNode && (
          <div style={{
            width: 280, padding: 20, borderLeft: "1px solid #1e293b",
            background: "#0f172a", overflowY: "auto", flexShrink: 0,
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 16 }}>
              <div style={{ width: 12, height: 12, borderRadius: "50%", background: selectedNode.color }} />
              <span style={{ fontSize: 11, color: "#64748b", textTransform: "uppercase", letterSpacing: 1 }}>
                {LAYER_LABELS[selectedNode.layer]}
              </span>
            </div>
            <h2 style={{ margin: "0 0 8px", fontSize: 16, color: "#f1f5f9" }}>
              {details?.title || selectedNode.label.replace("\n", " ")}
            </h2>
            {details?.status && (
              <div style={{
                display: "inline-block", padding: "2px 8px", borderRadius: 4,
                background: selectedNode.color + "33", color: selectedNode.color,
                fontSize: 11, marginBottom: 12,
              }}>
                {details.status}
              </div>
            )}
            {details?.summary && (
              <p style={{ fontSize: 13, color: "#94a3b8", lineHeight: 1.6, margin: "0 0 12px" }}>
                {details.summary}
              </p>
            )}
            {details?.impacto && (
              <div style={{ padding: 10, background: "#1e293b", borderRadius: 6 }}>
                <div style={{ fontSize: 10, color: "#64748b", marginBottom: 4, textTransform: "uppercase" }}>Impacto</div>
                <div style={{ fontSize: 12, color: "#cbd5e1" }}>{details.impacto}</div>
              </div>
            )}
            <div style={{ marginTop: 16 }}>
              <div style={{ fontSize: 11, color: "#64748b", marginBottom: 8 }}>Conexões</div>
              {EDGES.filter((e) => e.from === selected || e.to === selected).map((e, i) => {
                const other = NODES.find((n) => n.id === (e.from === selected ? e.to : e.from));
                return (
                  <div key={i} style={{
                    display: "flex", alignItems: "center", gap: 6,
                    padding: "4px 0", borderBottom: "1px solid #1e293b", cursor: "pointer",
                  }}
                    onClick={() => setSelected(other?.id || null)}
                  >
                    <div style={{ width: 8, height: 8, borderRadius: "50%", background: other?.color || "#666", flexShrink: 0 }} />
                    <span style={{ fontSize: 11, color: "#94a3b8" }}>{e.label}</span>
                    <span style={{ fontSize: 11, color: "#cbd5e1", marginLeft: "auto" }}>{other?.label.split("\n")[0]}</span>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div style={{
        position: "fixed", bottom: 0, left: 0, right: 0,
        padding: "6px 24px", background: "#0a0f1e",
        borderTop: "1px solid #1e293b", display: "flex", gap: 16, fontSize: 11, color: "#475569",
      }}>
        <span>⚖️ Gonçalves et Alii — goncalvesetalii.github.io</span>
        <span>🔬 Instituto PCIHᶟ</span>
        <span>🧠 Gabinete Polimata do Atlântico Sul</span>
        <span style={{ marginLeft: "auto" }}>Scroll: zoom · Drag: pan · Click nó: detalhes</span>
      </div>
    </div>
  );
}
