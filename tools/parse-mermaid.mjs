import { readFileSync } from "node:fs";
import { JSDOM } from "jsdom";

// Mermaid initialises its label sanitiser when imported.
globalThis.window = new JSDOM("").window;
globalThis.document = window.document;
const { default: mermaid } = await import("mermaid");
mermaid.initialize({ startOnLoad: false, securityLevel: "strict" });

// These grammars expose their elements through diagram-specific databases.
const elementCounts = {
  sequence: db => db.getActors().size,
  gitGraph: db => db.getCommitsArray().length,
  c4: db => db.getC4ShapeArray().length + db.getRels().length,
  pie: db => db.getSections().size,
  quadrantChart: db => db.getQuadrantData().points.length,
  xychart: db => db.getXYChartData().plots.length,
  radar: db => db.getAxes().length,
  block: db => db.getBlocks().length,
  packet: db => db.getPacket().length,
  treeView: db => db.getRoot().children.length,
  ishikawa: db => Number(Boolean(db.getRoot())),
  eventmodeling: db => db.getState().boxes.length,
  venn: db => db.getSubsetData().length,
  wardley: db => db.getWardleyData().nodes.length,
  cynefin: db => db.getTransitions().length + [...db.getDomains().values()].flatMap(domain => domain.items).length,
};

async function hasWorkflowElement({ type, db, text }) {
  if (db.getVertices) {
    // Mermaid creates an implicit vertex for "style A" even without an A statement.
    const vertices = [...db.getVertices().values()];
    if (!vertices.length) return false;
    if (db.getEdges().length || vertices.some(v => v.type || !v.styles.length)) return true;
    const withoutStyles = text.replace(/(^|[;\n])[ \t]*style[ \t]+[^;\n]*/gi, "$1");
    const structural = await mermaid.mermaidAPI.getDiagramFromText(withoutStyles);
    return structural.db.getVertices().size > 0;
  }
  if (elementCounts[type]) return elementCounts[type](db) > 0;
  const elements = db.getData?.()?.nodes ?? db.getNodes?.() ?? db.getTasks?.() ?? db.getRules?.();
  return Boolean(elements?.length);
}

const errors = [];
for (const diagram of JSON.parse(readFileSync(0, "utf8"))) {
  try {
    // parse applies diagram-local configuration before constructing the database.
    await mermaid.parse(diagram);
    const parsed = await mermaid.mermaidAPI.getDiagramFromText(diagram);
    errors.push(await hasWorkflowElement(parsed) ? null : "The diagram has no workflow elements");
  } catch (error) {
    errors.push(error.message || String(error));
  }
}
process.stdout.write(JSON.stringify(errors));
