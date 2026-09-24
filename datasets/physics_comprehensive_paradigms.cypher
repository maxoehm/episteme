// ==============================================================================
// Grund GLP - Comprehensive Example Dataset: Physics Paradigm Shift
// Demonstrates: ALL 5 Pillars of Theory Metrics (Topology, Coherence, Empirical Power, Dynamics, Metatheoretical)
// 
// Scenario: The shift from Newtonian Mechanics to General Relativity, including
// anomalies (Mercury's orbit), immunizing stratagems (Planet Vulcan), and 
// analogical support (Electrostatics).
// ==============================================================================

// MATCH (n) DETACH DELETE n;

// ==========================================
// 1. EMPIRICAL POWER & T-THEORETICITY 
// (Shared observation laws, indicators, and primitives)
// ==========================================
CREATE (pt_mass:PrimitiveTerm {id: "PT_MASS", name: "Inertial Mass"})
CREATE (pt_dist:PrimitiveTerm {id: "PT_DIST", name: "Spatial Distance"})

CREATE (ei_tele:EmpiricalIndicator {id: "EI_TELE", name: "Telescope Astrometry", precision: 0.95})
CREATE (tc_orbit:TheoreticalConstruct {id: "TC_ORBIT", name: "Planetary Orbital Path"})
CREATE (ei_tele)-[:MEASURES]->(tc_orbit)
CREATE (tc_orbit)-[:DETERMINED_BY]->(pt_dist)

// Shared Evidence
CREATE (ev_jupiter:Evidence:Success {id: "EV_JUPITER", text: "Jupiter's orbit follows predicted elliptical path.", confidence: 1.0})
CREATE (ev_mercury:Evidence:Anomaly:FailureTypA {id: "EV_MERCURY", text: "Mercury's perihelion precesses by 43 arcseconds/century more than predicted.", confidence: 1.0})

// ==========================================
// 2. NEWTONIAN MECHANICS (VERSION 1)
// (High Unification, High Coherence, Early Successes)
// ==========================================
CREATE (tn_newton_v1:TheoryNet {id: "TN_NEWTON_V1", name: "Classical Mechanics", version: "v1"})
CREATE (core_newton_v1:TheoryCore {id: "CORE_N_V1", name: "Newtonian Core"})-[:BELONGS_TO]->(tn_newton_v1)

CREATE (ax_gravity:BasicAxiom:Law {id: "AX_GRAVITY", text: "F = G(m1m2)/r^2"})-[:BELONGS_TO]->(core_newton_v1)
CREATE (ax_motion:BasicAxiom:Law {id: "AX_MOTION", text: "F = ma"})-[:BELONGS_TO]->(core_newton_v1)
CREATE (tc_abs_space:TheoreticalConstruct {id: "TC_ABS_SPACE", name: "Absolute Space and Time"})-[:BELONGS_TO]->(core_newton_v1)

CREATE (dl_kepler:DerivedEmpiricalLaw {id: "DL_KEPLER", text: "Planets orbit in ellipses."})-[:BELONGS_TO]->(tn_newton_v1)

// Derivation Tree (DAG property)
CREATE (ax_gravity)-[:SUPPORTS {weight: 1.0}]->(dl_kepler)
CREATE (ax_motion)-[:SUPPORTS {weight: 1.0}]->(dl_kepler)

// Empirical Applications
CREATE (app_jup_v1:EmpiricalApplication {id: "APP_JUP_V1", target: "Jupiter"})-[:BELONGS_TO]->(tn_newton_v1)
CREATE (dl_kepler)-[:EXPLAINS {weight: 0.95}]->(app_jup_v1)
CREATE (app_jup_v1)-[:MATCHES_EVIDENCE]->(ev_jupiter)

// ==========================================
// 3. NEWTONIAN MECHANICS (VERSION 2) - THEORY DYNAMICS
// (Degeneration Index & Immunizing Stratagems)
// ==========================================
// A new version is created to deal with the Mercury anomaly
CREATE (tn_newton_v2:TheoryNet {id: "TN_NEWTON_V2", name: "Classical Mechanics", version: "v2"})
CREATE (core_newton_v2:TheoryCore {id: "CORE_N_V2", name: "Newtonian Core (Revised)"})-[:BELONGS_TO]->(tn_newton_v2)

// Inherit the axioms
CREATE (core_newton_v1)-[:EVOLVES_TO]->(core_newton_v2)
CREATE (tn_newton_v1)-[:EVOLVES_TO]->(tn_newton_v2)

// The Ad-Hoc Modification (Immunizing Stratagem)
CREATE (hyp_vulcan:Claim {id: "HYP_VULCAN", text: "An unseen planet 'Vulcan' exerts gravitational pull on Mercury.", ad_hoc: true})-[:BELONGS_TO]->(tn_newton_v2)

// Attempted resolution of the anomaly
CREATE (hyp_vulcan)-[:RESOLVES_ANOMALY {success: false}]->(ev_mercury)

// But Vulcan is never found (FailureTypA)
CREATE (ev_no_vulcan:Evidence:FailureTypA {id: "EV_NO_VULCAN", text: "Telescopic searches reveal no intramercurial planet.", confidence: 1.0})
CREATE (ev_no_vulcan)-[:ATTACKS {weight: -1.0}]->(hyp_vulcan)

// ==========================================
// 4. GENERAL RELATIVITY (VERSION 1) - METATHEORETICAL
// (Reduction Capacity, Paradigm Shift, Higher-Level Warrant)
// ==========================================
CREATE (tn_relativity:TheoryNet {id: "TN_RELATIVITY_V1", name: "General Relativity", version: "v1"})
CREATE (core_rel:TheoryCore {id: "CORE_REL_V1", name: "Einsteinian Core"})-[:BELONGS_TO]->(tn_relativity)

CREATE (ax_equiv:BasicAxiom:Law {id: "AX_EQUIV", text: "Equivalence Principle (Inertial mass = Gravitational mass)"})-[:BELONGS_TO]->(core_rel)
CREATE (tc_spacetime:TheoreticalConstruct {id: "TC_SPACETIME", name: "Curved Spacetime Manifold"})-[:BELONGS_TO]->(core_rel)

// The new explanation natively handles the anomaly without ad-hoc hypotheses
CREATE (dl_geodesic:DerivedEmpiricalLaw {id: "DL_GEODESIC", text: "Objects follow geodesics in curved spacetime."})-[:BELONGS_TO]->(tn_relativity)
CREATE (ax_equiv)-[:SUPPORTS {weight: 1.0}]->(dl_geodesic)
CREATE (tc_spacetime)-[:SUPPORTS {weight: 1.0}]->(dl_geodesic)

CREATE (app_merc_rel:EmpiricalApplication {id: "APP_MERC_REL", target: "Mercury Precession"})-[:BELONGS_TO]->(tn_relativity)
CREATE (dl_geodesic)-[:EXPLAINS {weight: 0.99}]->(app_merc_rel)
CREATE (app_merc_rel)-[:MATCHES_EVIDENCE]->(ev_mercury)

// Metatheoretical: Reduction Capacity / Subsumption
// Relativity reduces to Newtonian mechanics at low velocities
CREATE (tn_relativity)-[:SUBSUMES {condition: "v << c, weak gravity field"}]->(tn_newton_v1)
CREATE (tn_relativity)-[:REDUCES_TO {limit: "c -> infinity"}]->(tn_newton_v1)

// Paradigm Guidance / Conflict
CREATE (core_rel)-[:ATTACKS {weight: -0.9}]->(tc_abs_space) // Spacetime attacks absolute space
CREATE (app_merc_rel)-[:ATTACKS {weight: -0.9}]->(hyp_vulcan) // The new paradigm actively refutes the old immunization

// ==========================================
// 5. ELECTROSTATICS (ANALOGICAL SUPPORT)
// (Metatheoretical lateral reinforcement)
// ==========================================
CREATE (tn_electro:TheoryNet {id: "TN_ELECTRO", name: "Classical Electromagnetism", version: "v1"})
CREATE (ax_coulomb:BasicAxiom:Law {id: "AX_COULOMB", text: "F = k(q1q2)/r^2"})-[:BELONGS_TO]->(tn_electro)

// Cross-domain structural isomorphism
CREATE (ax_coulomb)-[:ANALOGOUS_TO {mapping: "inverse-square law, centralized force"}]->(ax_gravity)
