/**
 * Episteme - Luminous Constellation Theory Graph
 *
 * An expansive, organic 3D knowledge graph visualizer:
 * - Volumetric, interconnected graph topology (no rigid pyramid tiers or ellipse rings)
 * - Dynamic emergence: empirical literature clusters -> entity relations -> unified theory net
 * - Living ambient motion & interactive 3D mouse parallax
 * - Coherence wave ripples across graph topology upon verification
 */
(() => {
  'use strict';

  function initTheoryNetCanvas() {
    const canvas = document.getElementById('theorynet-hero-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const statusTextEl = document.getElementById('hero-status-text');
    const statusDotEl = document.querySelector('.glp-hero__status-dot');
    const replayBtn = document.getElementById('hero-replay-btn');
    const tooltipEl = document.getElementById('hero-node-tooltip');

    // Display & Retina DPI scaling
    let width = 0;
    let height = 0;
    let dpr = Math.min(window.devicePixelRatio || 1, 2);

    function resize() {
      const rect = canvas.parentElement.getBoundingClientRect();
      width = rect.width;
      height = rect.height || Math.min(window.innerHeight * 0.85, 720);
      canvas.width = Math.floor(width * dpr);
      canvas.height = Math.floor(height * dpr);
      canvas.style.width = `${width}px`;
      canvas.style.height = `${height}px`;
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.scale(dpr, dpr);
    }

    resize();
    window.addEventListener('resize', resize, { passive: true });

    // 3D Camera & Smooth Mouse Parallax
    const prefersReducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let targetRotX = 0.28; // Subtle downward pitch for deep 3D perspective
    let targetRotY = 0.65; // Isometric angle
    let rotX = targetRotX;
    let rotY = targetRotY;
    let mouseX = 0;
    let mouseY = 0;
    let isHovering = false;
    let hoveredNode = null;

    function handlePointerMove(clientX, clientY) {
      const rect = canvas.getBoundingClientRect();
      isHovering = true;
      mouseX = (clientX - rect.left) / width - 0.5;
      mouseY = (clientY - rect.top) / height - 0.5;
      if (!prefersReducedMotion) {
        targetRotY = 0.65 + mouseX * 0.28;
        targetRotX = 0.28 - mouseY * 0.22;
      }
    }

    canvas.addEventListener('mousemove', (e) => {
      handlePointerMove(e.clientX, e.clientY);
    }, { passive: true });

    canvas.addEventListener('mouseleave', () => {
      isHovering = false;
      targetRotX = 0.28;
      targetRotY = 0.65;
      hoveredNode = null;
      canvas.style.cursor = 'default';
      if (tooltipEl) tooltipEl.classList.remove('is-visible');
    }, { passive: true });

    canvas.addEventListener('touchstart', (e) => {
      if (e.touches && e.touches.length > 0) {
        handlePointerMove(e.touches[0].clientX, e.touches[0].clientY);
      }
    }, { passive: true });

    canvas.addEventListener('touchmove', (e) => {
      if (e.touches && e.touches.length > 0) {
        handlePointerMove(e.touches[0].clientX, e.touches[0].clientY);
      }
    }, { passive: true });

    window.addEventListener('touchstart', (e) => {
      if (!canvas.contains(e.target) && (!tooltipEl || !tooltipEl.contains(e.target))) {
        isHovering = false;
        hoveredNode = null;
        if (tooltipEl) tooltipEl.classList.remove('is-visible');
      }
    }, { passive: true });

    // 3D Projection
    function project(x, y, z, cx, cy, scale) {
      const cosY = Math.cos(rotY);
      const sinY = Math.sin(rotY);
      const x1 = x * cosY - z * sinY;
      const z1 = z * cosY + x * sinY;

      const cosX = Math.cos(rotX);
      const sinX = Math.sin(rotX);
      const y2 = y * cosX - z1 * sinX;
      const z2 = z1 * cosX + y * sinX;

      return {
        px: cx + x1 * scale,
        py: cy - y2 * scale,
        depth: z2
      };
    }

    // Volumetric 3D Theory Graph Nodes (Organic, expansive layout)
    const nodes = [
      // Cluster 1: Empirical Literature & Evidence (Sky Blue)
      { id: 'E1', label: 'Empirical Text Span [p.42]', layer: 'L1', type: 'data', x: -0.68, y: -0.32, z: 0.28, spawnTime: 0.4, meta: { role: 'Empirical Text Span', doc: 'Schurz (2014) §3.2, p.42' } },
      { id: 'E2', label: 'Context Chunk [Doc A]', layer: 'L1', type: 'data', x: -0.42, y: -0.56, z: -0.15, spawnTime: 0.8, meta: { role: 'Context Chunk', doc: 'Lakatos (1978) Doc A' } },
      { id: 'E3', label: 'Empirical Evidence Datum', layer: 'L1', type: 'data', x: -0.12, y: -0.42, z: 0.52, spawnTime: 1.2, meta: { role: 'Empirical Evidence', doc: 'Thagard (1989) Table 1' } },
      { id: 'E4', label: 'Corpus Chunk [Doc B]', layer: 'L1', type: 'data', x: -0.72, y: -0.05, z: -0.38, spawnTime: 1.6, meta: { role: 'Corpus Chunk', doc: 'Stegmüller (1976) Doc B' } },
      { id: 'E5', label: 'Citation Anchor [Doc C]', layer: 'L1', type: 'data', x: -0.34, y: -0.18, z: -0.46, spawnTime: 2.0, meta: { role: 'Citation Anchor', doc: 'Quine (1951) §4, p.24' } },

      // Cluster 2: Extracted Entities & Semantic Relational Hubs (Purple / Violet)
      { id: 'A1', label: 'Structural Invariance', layer: 'L2', type: 'entity', x: -0.28, y: 0.12, z: 0.18, spawnTime: 3.2, meta: { role: 'Structural Invariance', formula: 'Inv(M_p, T)' } },
      { id: 'H1', label: 'Minimal Poset Bound', layer: 'L2', type: 'entity', x: 0.12, y: -0.24, z: 0.26, spawnTime: 3.6, meta: { role: 'Poset Minimum', formula: 'inf(P_E) >= θ' } },
      { id: 'C1', label: 'Concept Core (Hub)', layer: 'L2', type: 'hub', x: 0.04, y: 0.16, z: -0.12, spawnTime: 4.4, isHub: true, meta: { role: 'Central Concept Hub', formula: 'Int(C_1) ⊆ M_p' } },
      { id: 'H2', label: 'Dialectical Relation', layer: 'L2', type: 'entity', x: 0.48, y: -0.14, z: -0.28, spawnTime: 4.0, meta: { role: 'Dialectical Relation', formula: 'Coh(H_1, H_2) > 0' } },
      { id: 'A2', label: 'Conservation Core', layer: 'L2', type: 'entity', x: 0.38, y: 0.14, z: 0.38, spawnTime: 3.4, meta: { role: 'Conservation Law', formula: 'Cons(Core, App)' } },
      { id: 'C2', label: 'Symmetry Structure', layer: 'L2', type: 'entity', x: -0.08, y: 0.42, z: 0.34, spawnTime: 4.8, meta: { role: 'Symmetry Operator', formula: 'Sym(M) ≅ Aut(T)' } },

      // Cluster 3: Theoretical Hypotheses & Axiomatic Core (Gold & Royal Blue)
      { id: 'H3', label: 'Unification Poset', layer: 'L3', type: 'hypo', x: 0.32, y: 0.48, z: -0.18, spawnTime: 6.8, meta: { role: 'Unification Poset', formula: 'U_E(T) = 0.894' } },
      { id: 'H4', label: 'Coherence Closure', layer: 'L3', type: 'hypo', x: 0.62, y: 0.28, z: 0.12, spawnTime: 7.2, meta: { role: 'Coherence Closure', formula: 'Ψ_echo = 0.942' } },
      { id: 'M_app', label: 'Intended Applications', layer: 'L3', type: 'entity', x: 0.66, y: -0.38, z: 0.24, spawnTime: 5.2, meta: { role: 'Intended Applications', formula: 'I ⊆ M_pp' } },
      { id: 'T_core', label: 'Axiomatic Theory Core', layer: 'L3', type: 'axiom', x: 0.18, y: 0.58, z: 0.08, spawnTime: 8.2, isApex: true, meta: { role: 'Axiomatic Theory Core', formula: 'T = <M_p, M, M_pp, C, I>', coherence: '0.942 (Optimal)' } }
    ];

    const nodeMap = {};
    nodes.forEach(n => { nodeMap[n.id] = n; });

    // Lineage resolution for interactive hover
    function getLineage(nodeId) {
      const lineageNodes = new Set([nodeId]);
      let added = true;
      while (added) {
        added = false;
        edges.forEach(e => {
          if (lineageNodes.has(e.to) && !lineageNodes.has(e.from)) {
            lineageNodes.add(e.from);
            added = true;
          }
          if (lineageNodes.has(e.from) && !lineageNodes.has(e.to)) {
            lineageNodes.add(e.to);
            added = true;
          }
        });
      }
      return lineageNodes;
    }

    // Rich Graph Edges (Organic multidirectional connectivity)
    const edges = [
      // Phase 1: Intra-literature connections
      { from: 'E1', to: 'E2', tStart: 1.0, tEnd: 2.2, isSubtle: true },
      { from: 'E3', to: 'E2', tStart: 1.4, tEnd: 2.6, isSubtle: true },
      { from: 'E4', to: 'E5', tStart: 1.8, tEnd: 3.0, isSubtle: true },
      { from: 'E5', to: 'E1', tStart: 2.0, tEnd: 3.1, isSubtle: true },

      // Phase 2: Extraction from Literature into Entities & Hubs
      { from: 'E1', to: 'A1', tStart: 2.8, tEnd: 4.0 },
      { from: 'E4', to: 'A1', tStart: 3.0, tEnd: 4.2 },
      { from: 'E2', to: 'H1', tStart: 3.4, tEnd: 4.6 },
      { from: 'E3', to: 'H1', tStart: 3.6, tEnd: 4.8 },
      { from: 'E5', to: 'C1', tStart: 3.8, tEnd: 5.0 },
      { from: 'E3', to: 'A2', tStart: 4.0, tEnd: 5.2 },
      { from: 'E5', to: 'H2', tStart: 4.2, tEnd: 5.4 },
      { from: 'E3', to: 'M_app', tStart: 4.6, tEnd: 5.8 },

      // Phase 3: Relational maturation & cross-entity bridging
      { from: 'A1', to: 'C1', tStart: 5.0, tEnd: 6.0 },
      { from: 'H1', to: 'C1', tStart: 5.2, tEnd: 6.2 },
      { from: 'H2', to: 'C1', tStart: 5.4, tEnd: 6.4 },
      { from: 'A2', to: 'C1', tStart: 5.6, tEnd: 6.6 },
      { from: 'A1', to: 'C2', tStart: 5.8, tEnd: 6.8 },
      { from: 'A2', to: 'M_app', tStart: 6.0, tEnd: 7.0 },
      { from: 'H1', to: 'H2', tStart: 6.2, tEnd: 7.2 },

      // Phase 4: Theory synthesis & Convergence onto Core
      { from: 'C2', to: 'T_core', tStart: 7.2, tEnd: 8.2 },
      { from: 'C1', to: 'H3', tStart: 7.4, tEnd: 8.4 },
      { from: 'C1', to: 'H4', tStart: 7.6, tEnd: 8.6 },
      { from: 'A2', to: 'H4', tStart: 7.8, tEnd: 8.8 },
      { from: 'H2', to: 'H4', tStart: 8.0, tEnd: 9.0 },
      { from: 'M_app', to: 'H4', tStart: 8.2, tEnd: 9.2 },
      { from: 'H3', to: 'T_core', tStart: 8.6, tEnd: 9.6 },
      { from: 'H4', to: 'T_core', tStart: 8.8, tEnd: 9.8 },
      { from: 'C1', to: 'T_core', tStart: 9.0, tEnd: 10.0 }
    ];

    // Colors
    const colors = {
      canvas: '#FFFFFF',
      edgeSettled: 'rgba(148, 163, 184, 0.42)',
      edgeSubtle: 'rgba(2, 132, 199, 0.22)',
      edgeActive: '#2563EB',
      edgeWave: '#059669',
      types: {
        data: { border: '#0284C7', fill: '#E0F2FE', glow: 'rgba(2, 132, 199, 0.30)' },
        entity: { border: '#7C3AED', fill: '#EDE9FE', glow: 'rgba(124, 58, 237, 0.30)' },
        hub: { border: '#6366F1', fill: '#EEF2FF', glow: 'rgba(99, 102, 241, 0.40)' },
        hypo: { border: '#2563EB', fill: '#DBEAFE', glow: 'rgba(37, 99, 235, 0.30)' },
        axiom: { border: '#D97706', fill: '#FEF3C7', glow: 'rgba(217, 119, 6, 0.45)' }
      }
    };

    // Cycle & Animation Timing
    let constructionTime = 0;
    let ambientTime = 0;
    const COMPLETE_TIME = 11.2;
    let isComplete = false;
    let animId = null;
    let isVisible = true;

    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((entries) => {
        isVisible = entries[0].isIntersecting;
      }, { threshold: 0.05 });
      io.observe(canvas);
    }

    if (replayBtn) {
      replayBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        constructionTime = 0;
        isComplete = false;
        if (statusDotEl) statusDotEl.classList.remove('is-verified');
      });
    }

    function updateStatus(t) {
      if (!statusTextEl) return;

      if (t < 3.0) {
        statusTextEl.textContent = 'Extracting literature spans...';
        if (statusDotEl) statusDotEl.classList.remove('is-verified');
      } else if (t < 6.8) {
        statusTextEl.textContent = 'Structuring entity relations...';
        if (statusDotEl) statusDotEl.classList.remove('is-verified');
      } else if (t < 10.0) {
        statusTextEl.textContent = 'Synthesizing TheoryNet...';
        if (statusDotEl) statusDotEl.classList.remove('is-verified');
      } else {
        statusTextEl.textContent = 'TheoryNet Verified';
        if (statusDotEl) statusDotEl.classList.add('is-verified');
      }
    }

    // Main Render Loop
    function render() {
      animId = requestAnimationFrame(render);
      if (!isVisible) return;

      if (prefersReducedMotion) {
        constructionTime = COMPLETE_TIME;
        isComplete = true;
        rotX = targetRotX;
        rotY = targetRotY;
      } else {
        rotX += (targetRotX - rotX) * 0.05;
        rotY += (targetRotY - rotY) * 0.05;

        if (constructionTime < COMPLETE_TIME) {
          constructionTime += 0.016;
        } else {
          isComplete = true;
        }
        ambientTime += 0.016;
      }

      const t = constructionTime;
      updateStatus(t);

      // Clear Canvas
      ctx.fillStyle = colors.canvas;
      ctx.fillRect(0, 0, width, height);

      // Generously sized scale that fills the visual container
      const maxScale = width > 1400 ? 460 : (width > 960 ? 400 : 340);
      const scale = Math.min(width * 0.44, height * 0.52, maxScale);
      const cx = width * 0.48;
      const cy = height * 0.50;

      // Soft ambient radial glow
      const bgGlow = ctx.createRadialGradient(cx, cy, 20, cx, cy, scale * 1.3);
      bgGlow.addColorStop(0, 'rgba(239, 246, 255, 0.70)');
      bgGlow.addColorStop(0.5, 'rgba(248, 250, 252, 0.45)');
      bgGlow.addColorStop(1, 'rgba(255, 255, 255, 0)');
      ctx.fillStyle = bgGlow;
      ctx.fillRect(0, 0, width, height);

      // Active Lineage for Hovered Node
      const activeLineage = hoveredNode ? getLineage(hoveredNode.id) : null;

      // 1. DRAW EDGES (Back-to-Front Depth Sorted)
      // Luminous heartbeat wave: triggers upon completion and then periodically every 9s as a gentle traveling ripple
      const isAmbientWave = isComplete && (ambientTime % 9.0 < 1.6);
      const waveActive = (t >= 9.6 && t < 11.2) || isAmbientWave;
      const wavePhase = (t >= 9.6 && t < 11.2)
        ? ((t - 9.6) / 1.6)
        : ((ambientTime % 9.0) / 1.6);

      const sortedEdges = edges.map(e => {
        const u = nodeMap[e.from];
        const v = nodeMap[e.to];
        if (!u || !v) return null;

        // Subtle ambient breathing float for organic feel
        const uFloatY = Math.sin(ambientTime * 1.5 + u.x * 3) * 0.02;
        const vFloatY = Math.sin(ambientTime * 1.5 + v.x * 3) * 0.02;

        const pu = project(u.x, u.y + uFloatY, u.z, cx, cy, scale);
        const pv = project(v.x, v.y + vFloatY, v.z, cx, cy, scale);
        return {
          edge: e,
          u,
          v,
          pu,
          pv,
          depth: (pu.depth + pv.depth) * 0.5
        };
      }).filter(Boolean);

      sortedEdges.sort((a, b) => a.depth - b.depth);

      sortedEdges.forEach(item => {
        const { edge: e, u, v, pu, pv } = item;
        if (t < e.tStart) return;

        const progress = Math.min(1.0, (t - e.tStart) / (e.tEnd - e.tStart));
        const currPx = pu.px + (pv.px - pu.px) * progress;
        const currPy = pu.py + (pv.py - pu.py) * progress;

        const isLineageEdge = activeLineage && activeLineage.has(e.from) && activeLineage.has(e.to);
        const isDimmed = activeLineage && !isLineageEdge;

        ctx.save();
        ctx.beginPath();
        ctx.moveTo(pu.px, pu.py);
        ctx.lineTo(currPx, currPy);

        if (e.isSubtle) {
          ctx.strokeStyle = colors.edgeSubtle;
          ctx.lineWidth = 1.1;
          ctx.setLineDash([3, 4]);
          if (isDimmed) ctx.globalAlpha = 0.10;
          else if (isLineageEdge) {
            ctx.strokeStyle = colors.edgeActive;
            ctx.lineWidth = 2.0;
            ctx.setLineDash([]);
          }
          ctx.stroke();
        } else if (progress < 1.0) {
          ctx.strokeStyle = colors.edgeActive;
          ctx.lineWidth = 2.0;
          ctx.stroke();

          // Glowing vector head
          ctx.beginPath();
          ctx.arc(currPx, currPy, 3.2, 0, Math.PI * 2);
          ctx.fillStyle = '#2563EB';
          ctx.fill();

          ctx.beginPath();
          ctx.arc(currPx, currPy, 7, 0, Math.PI * 2);
          ctx.fillStyle = 'rgba(37, 99, 235, 0.28)';
          ctx.fill();
        } else if (isDimmed) {
          ctx.globalAlpha = 0.08;
          ctx.strokeStyle = colors.edgeSettled;
          ctx.lineWidth = 1.0;
          ctx.stroke();
        } else if (isLineageEdge) {
          ctx.globalAlpha = 1.0;
          ctx.strokeStyle = '#2563EB';
          ctx.lineWidth = 2.4;
          ctx.stroke();
        } else {
          if (waveActive) {
            // Wave travels outward and downward from apex (y=0.58) across the graph
            const waveFront = wavePhase * 1.4;
            const edgeElevation = 0.65 - (u.y + v.y) * 0.5;
            const distFromWave = Math.abs(waveFront - edgeElevation);

            if (distFromWave < 0.22) {
              const intensity = 1.0 - (distFromWave / 0.22);
              ctx.strokeStyle = `rgba(5, 150, 105, ${0.35 + intensity * 0.60})`;
              ctx.lineWidth = 1.2 + intensity * 1.2;
            } else {
              ctx.strokeStyle = colors.edgeSettled;
              ctx.lineWidth = 1.2;
            }
          } else {
            ctx.strokeStyle = colors.edgeSettled;
            ctx.lineWidth = 1.2;
          }
          ctx.stroke();
        }
        ctx.restore();
      });

      // 2. DRAW GRAPH NODES (Back-to-Front Depth Sorted)
      let currentHover = null;
      let minDistance = 26;

      const activeNodes = nodes.filter(n => t >= n.spawnTime);
      activeNodes.sort((a, b) => {
        const floatYa = Math.sin(ambientTime * 1.5 + a.x * 3) * 0.02;
        const floatYb = Math.sin(ambientTime * 1.5 + b.x * 3) * 0.02;
        const pa = project(a.x, a.y + floatYa, a.z, cx, cy, scale);
        const pb = project(b.x, b.y + floatYb, b.z, cx, cy, scale);
        return pa.depth - pb.depth;
      });

      activeNodes.forEach(n => {
        const floatY = Math.sin(ambientTime * 1.5 + n.x * 3) * 0.02;
        const p = project(n.x, n.y + floatY, n.z, cx, cy, scale);
        const style = colors.types[n.type] || colors.types.entity;

        if (isHovering) {
          const dx = (mouseX + 0.5) * width - p.px;
          const dy = (mouseY + 0.5) * height - p.py;
          const dist = Math.hypot(dx, dy);
          if (dist < minDistance) {
            minDistance = dist;
            currentHover = n;
          }
        }

        const isNodeHovered = hoveredNode && hoveredNode.id === n.id;
        const isLineageNode = !activeLineage || activeLineage.has(n.id);
        const isDimmed = activeLineage && !isLineageNode;
        const baseRadius = n.isApex ? 8.5 : (n.isHub ? 7.0 : 5.4);
        const radius = isNodeHovered ? baseRadius * 1.35 : baseRadius;

        ctx.save();
        if (isDimmed) ctx.globalAlpha = 0.12;

        // Spawn pulse ring
        const timeSinceSpawn = t - n.spawnTime;
        if (timeSinceSpawn < 0.8) {
          const progress = timeSinceSpawn / 0.8;
          ctx.beginPath();
          ctx.arc(p.px, p.py, radius + progress * 20, 0, Math.PI * 2);
          ctx.strokeStyle = style.glow;
          ctx.lineWidth = 1.8 * (1 - progress);
          ctx.stroke();
        }

        // Luminous breathing halo
        const ambientPulse = Math.sin(ambientTime * 2.2 + n.x * 4) * 1.5;
        ctx.beginPath();
        ctx.arc(p.px, p.py, radius + 4 + (n.isApex ? ambientPulse * 1.6 : 0), 0, Math.PI * 2);
        ctx.fillStyle = isNodeHovered ? style.glow : (n.isApex ? 'rgba(217, 119, 6, 0.22)' : (n.isHub ? 'rgba(99, 102, 241, 0.18)' : 'rgba(255, 255, 255, 0.88)'));
        ctx.fill();

        // Node disc
        ctx.beginPath();
        ctx.arc(p.px, p.py, radius, 0, Math.PI * 2);
        ctx.fillStyle = style.fill;
        ctx.fill();
        ctx.strokeStyle = style.border;
        ctx.lineWidth = isNodeHovered ? 2.4 : (n.isApex ? 2.6 : 2.0);
        ctx.stroke();

        // Bright jewel center
        ctx.beginPath();
        ctx.arc(p.px, p.py, radius * 0.36, 0, Math.PI * 2);
        ctx.fillStyle = style.border;
        ctx.fill();

        // 3 Key Anchor Landmarks (Clean typography, zero box clutter)
        const isAnchor = n.id === 'E1' || n.id === 'C1' || n.id === 'T_core';
        if (isAnchor && !isNodeHovered) {
          const fadeIn = Math.min(1.0, Math.max(0.0, (t - n.spawnTime) / 0.8));
          if (fadeIn > 0.01) {
            ctx.save();
            ctx.globalAlpha = (isDimmed ? 0.20 : 0.88) * fadeIn;
            ctx.font = n.id === 'T_core'
              ? '600 11.5px "Inter", -apple-system, sans-serif'
              : '550 11px "Inter", -apple-system, sans-serif';

            if (n.id === 'E1') {
              ctx.fillStyle = '#0369A1';
              ctx.textAlign = 'right';
              ctx.textBaseline = 'middle';
              ctx.fillText('Literature & Evidence', p.px - radius - 8, p.py);
            } else if (n.id === 'C1') {
              ctx.fillStyle = '#6D28D9';
              ctx.textAlign = 'left';
              ctx.textBaseline = 'middle';
              ctx.fillText('Concept Core', p.px + radius + 8, p.py - 3);
            } else if (n.id === 'T_core') {
              ctx.fillStyle = '#B45309';
              ctx.textAlign = 'left';
              ctx.textBaseline = 'middle';
              ctx.fillText('Theory Core', p.px + radius + 9, p.py);
            }
            ctx.restore();
          }
        }

        // Hover label (shows specific node details for any hovered node)
        if (isNodeHovered) {
          ctx.font = '600 11.5px "Inter", -apple-system, sans-serif';
          ctx.fillStyle = '#0F172A';
          ctx.textAlign = 'left';
          ctx.textBaseline = 'middle';
          ctx.fillText(n.label, p.px + radius + 9, p.py);
        }

        ctx.restore();
      });

      hoveredNode = currentHover;
      canvas.style.cursor = hoveredNode ? 'pointer' : 'default';

      // Update Tooltip
      if (hoveredNode && tooltipEl) {
        const meta = hoveredNode.meta || {};
        const layerTitle = hoveredNode.layer === 'L1' ? 'Empirical Literature' : (hoveredNode.layer === 'L2' ? 'Extracted Entity' : 'TheoryNet Core');
        tooltipEl.innerHTML = `
          <div class="glp-hero__tooltip-header">
            <span class="glp-hero__tooltip-tag glp-hero__tooltip-tag--${hoveredNode.layer}">${hoveredNode.layer}: ${layerTitle}</span>
            <span class="glp-hero__tooltip-id">${hoveredNode.id}</span>
          </div>
          <div class="glp-hero__tooltip-title">${hoveredNode.label}</div>
          <div class="glp-hero__tooltip-body">
            ${meta.doc ? `<div class="glp-hero__tooltip-row"><span class="glp-hero__tooltip-label">Source:</span><span class="glp-hero__tooltip-val">${meta.doc}</span></div>` : ''}
            ${meta.formula ? `<div class="glp-hero__tooltip-row"><span class="glp-hero__tooltip-label">Formula:</span><span class="glp-hero__tooltip-val">${meta.formula}</span></div>` : ''}
            ${meta.coherence ? `<div class="glp-hero__tooltip-row"><span class="glp-hero__tooltip-label">Coherence:</span><span class="glp-hero__tooltip-val">${meta.coherence}</span></div>` : ''}
          </div>
        `;

        const floatY = Math.sin(ambientTime * 1.5 + hoveredNode.x * 3) * 0.02;
        const hp = project(hoveredNode.x, hoveredNode.y + floatY, hoveredNode.z, cx, cy, scale);
        const tipX = Math.min(width - 270, Math.max(16, hp.px + 18));
        const tipY = Math.min(height - 140, Math.max(16, hp.py - 40));
        tooltipEl.style.left = `${tipX}px`;
        tooltipEl.style.top = `${tipY}px`;
        tooltipEl.classList.add('is-visible');
      } else if (tooltipEl) {
        tooltipEl.classList.remove('is-visible');
      }
    }

    render();
  }

  if (document.readyState === 'complete') {
    setTimeout(initTheoryNetCanvas, 150);
  } else {
    window.addEventListener('load', () => {
      setTimeout(initTheoryNetCanvas, 150);
    }, { once: true });
  }
})();
