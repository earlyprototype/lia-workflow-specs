import { readFileSync } from "node:fs";
import { JSDOM } from "jsdom";

// Mermaid initialises its label sanitiser when imported.
globalThis.window = new JSDOM("").window;
globalThis.document = window.document;
const { default: mermaid } = await import("mermaid");
mermaid.initialize({ startOnLoad: false, securityLevel: "strict" });

const errors = [];
for (const diagram of JSON.parse(readFileSync(0, "utf8"))) {
  try {
    await mermaid.parse(diagram);
    // Mermaid accepts a bare diagram declaration, even when it has no nodes.
    const body = diagram.replace(/^\s*%%.*$/gm, "").trim();
    const declarationOnly = /^(?:(?:graph|flowchart)\s+(?:TB|TD|BT|LR|RL)|stateDiagram(?:-v2)?)\s*;?$/i;
    errors.push(declarationOnly.test(body) ? "The diagram has no nodes" : null);
  } catch (error) {
    errors.push(error.message || String(error));
  }
}
process.stdout.write(JSON.stringify(errors));
