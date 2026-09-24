// docs/javascripts/mermaid.js
// Intercepts and enforces a publication-grade scientific theme for Mermaid.js

function isDarkMode() {
  return document.body ? document.body.getAttribute('data-md-color-scheme') === 'slate' : false;
}

function getScientificThemeConfig() {
  const dark = isDarkMode();

  const clusterBg = dark ? '#0f172a' : '#f8fafc';
  const clusterBorder = dark ? '#334155' : '#94a3b8';
  const textColor = dark ? '#f1f5f9' : '#0f172a';
  const nodeBg = dark ? '#1e293b' : '#ffffff';
  const nodeBorder = dark ? '#475569' : '#0f172a';
  const lineColor = dark ? '#94a3b8' : '#334155';

  return {
    startOnLoad: false,
    securityLevel: 'loose',
    theme: 'base',
    themeCSS: `
      .cluster rect {
        fill: ${clusterBg} !important;
        stroke: ${clusterBorder} !important;
      }
      .cluster text, .cluster span {
        fill: ${textColor} !important;
        color: ${textColor} !important;
      }
      .node rect, .node circle, .node ellipse, .node polygon, .node path {
        fill: ${nodeBg} !important;
        stroke: ${nodeBorder} !important;
      }
    `,
    themeVariables: dark
      ? {
          // --- Academic Dark (Slate) ---
          darkMode: true,
          background: '#0f172a',
          mainBkg: nodeBg,
          textColor: textColor,
          nodeBorder: nodeBorder,
          lineColor: lineColor,
          clusterBkg: clusterBg,
          clusterBorder: clusterBorder,
          titleColor: textColor,
          edgeLabelBackground: '#1e293b',

          // Uniform cluster/subgraph colors (replaces default rainbow cycling)
          cScale0: clusterBg,
          cScale1: clusterBg,
          cScale2: clusterBg,
          cScale3: clusterBg,
          cScale4: clusterBg,
          cScale5: clusterBg,
          cScaleLabel0: textColor,
          cScaleLabel1: textColor,
          cScaleLabel2: textColor,
          cScaleLabel3: textColor,
          cScaleLabel4: textColor,
          cScaleLabel5: textColor,

          primaryColor: '#1e293b',
          primaryTextColor: '#f8fafc',
          primaryBorderColor: '#d97706',
          fontFamily: 'Inter, system-ui, -apple-system, sans-serif',
          fontSize: '13px',
        }
      : {
          // --- Scientific Publishing Light (Journal / Print Ready) ---
          darkMode: false,
          background: '#ffffff',
          mainBkg: nodeBg,
          textColor: textColor,
          nodeBorder: nodeBorder,
          lineColor: lineColor,
          clusterBkg: clusterBg,
          clusterBorder: clusterBorder,
          titleColor: textColor,
          edgeLabelBackground: '#ffffff',

          // Uniform cluster/subgraph colors (replaces default rainbow cycling)
          cScale0: clusterBg,
          cScale1: clusterBg,
          cScale2: clusterBg,
          cScale3: clusterBg,
          cScale4: clusterBg,
          cScale5: clusterBg,
          cScaleLabel0: textColor,
          cScaleLabel1: textColor,
          cScaleLabel2: textColor,
          cScaleLabel3: textColor,
          cScaleLabel4: textColor,
          cScaleLabel5: textColor,

          primaryColor: '#f8fafc',
          primaryTextColor: '#0f172a',
          primaryBorderColor: '#0f172a',
          fontFamily: 'Inter, system-ui, -apple-system, sans-serif',
          fontSize: '13px',
        },
  };
}

// Hook into Mermaid: intercept Zensical's initialize calls to prevent theme wiping
if (window.mermaid) {
  const origInit = window.mermaid.initialize.bind(window.mermaid);

  window.mermaid.initialize = function (config) {
    const custom = getScientificThemeConfig();
    const mergedThemeCSS = (config && config.themeCSS ? config.themeCSS + '\n' : '') + custom.themeCSS;

    return origInit({
      ...config,
      ...custom,
      theme: custom.theme,
      themeCSS: mergedThemeCSS,
      themeVariables: {
        ...custom.themeVariables,
        ...(config && config.themeVariables ? config.themeVariables : {}),
      },
    });
  };

  // Perform initial configuration
  window.mermaid.initialize({ startOnLoad: false });
}

// Palette toggle listener (switch between light / slate dark modes)
function setupThemeObserver() {
  if (!document.body) {
    document.addEventListener('DOMContentLoaded', setupThemeObserver);
    return;
  }
  const observer = new MutationObserver((mutations) => {
    for (const mutation of mutations) {
      if (mutation.attributeName === 'data-md-color-scheme') {
        if (window.mermaid) {
          window.mermaid.initialize({ startOnLoad: false });
        }
      }
    }
  });
  observer.observe(document.body, { attributes: true, attributeFilter: ['data-md-color-scheme'] });
}

setupThemeObserver();