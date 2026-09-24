import Prism from "prismjs";

// Polyfill Prism on global scope so components like prism-cypher find it
if (typeof window !== "undefined") {
  (window as any).Prism = Prism;
}
if (typeof globalThis !== "undefined") {
  (globalThis as any).Prism = Prism;
}

export default Prism;
