"""Generator for canned demonstration run manifests and artifact envelopes.

Transforms domain paradigms into self-contained artifact envelopes and manifests
packaged directly within episteme_studio.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def generate_fixtures(base_dir: Path | None = None) -> None:
    """Generate demonstration manifests and artifact envelopes.

    Parameters
    ----------
    base_dir : Path or None, optional
        Target fixtures directory. If None, defaults to current module parent.
    """
    if base_dir is None:
        base_dir = Path(__file__).parent

    runs_dir = base_dir / "runs"
    artifacts_dir = base_dir / "artifacts"
    runs_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    _generate_physics_run(runs_dir, artifacts_dir)
    _generate_psychology_run(runs_dir, artifacts_dir)


def _write_envelope(
    target_dir: Path,
    artifact_id: str,
    kind: str,
    payload: dict[str, Any],
    run_id: str,
    phase_name: str,
) -> None:
    envelope = {
        "artifact_id": artifact_id,
        "identity_key": artifact_id,
        "kind": kind,
        "run_id": run_id,
        "phase_name": phase_name,
        "payload": payload,
        "provenance": {
            "source_path": f"datasets/{run_id}.cypher",
            "notes": {"generated": "demo_fixture"},
        },
        "created_at": "2026-09-01T10:00:00Z",
    }
    file_path = target_dir / f"{artifact_id}.json"
    file_path.write_text(json.dumps(envelope, indent=2), encoding="utf-8")


def _generate_physics_run(runs_dir: Path, artifacts_dir: Path) -> None:
    run_id = "run-demo-physics"
    run_art_dir = artifacts_dir / run_id
    run_art_dir.mkdir(parents=True, exist_ok=True)

    # 1. Document & Chunks (L1)
    _write_envelope(
        run_art_dir,
        "doc_physics",
        "document",
        {
            "id": "doc_physics",
            "title": "Physics Paradigm Shift: Classical Mechanics to General Relativity",
            "filename": "physics_comprehensive_paradigms.cypher",
            "author": "Isaac Newton / Albert Einstein / Urbain Le Verrier",
        },
        run_id,
        "Phase 1: Data Foundation",
    )

    chunks = [
        ("chunk_phys_1", "Empirical power & T-theoreticity: Inertial mass, spatial distance, and astrometric measurements."),
        ("chunk_phys_2", "Newtonian mechanics (v1): Gravitational law F=G(m1m2)/r^2, motion F=ma, and Keplerian orbital derivations."),
        ("chunk_phys_3", "Theory dynamics & anomaly: Mercury perihelion 43 arcsec/century anomaly and Le Verrier's Vulcan hypothesis."),
        ("chunk_phys_4", "General relativity (v1): Equivalence principle, curved spacetime manifold, and geodesic orbital explanations."),
        ("chunk_phys_5", "Metatheoretical reduction and electrostatics: Coulomb inverse-square law isomorphism and Newtonian reduction."),
    ]
    for cid, text in chunks:
        _write_envelope(
            run_art_dir,
            cid,
            "chunk",
            {
                "id": cid,
                "text": text,
                "chunk_index": int(cid.split("_")[-1]),
                "confidence": 1.0,
            },
            run_id,
            "Phase 1: Data Foundation",
        )

    # 2. Entities (L2)
    entities = [
        ("PT_MASS", "PrimitiveTerm", "Inertial Mass", "Fundamental physical quantity describing inertial resistance."),
        ("PT_DIST", "PrimitiveTerm", "Spatial Distance", "Geometric interval between spatial coordinates."),
        ("EI_TELE", "EmpiricalIndicator", "Telescope Astrometry", "High-precision telescopic tracking of planetary positions."),
        ("TC_ORBIT", "TheoreticalConstruct", "Planetary Orbital Path", "Theoretical construct modeling planetary trajectories."),
        ("TC_ABS_SPACE", "TheoreticalConstruct", "Absolute Space and Time", "Newtonian Euclidean absolute coordinate framework."),
        ("TC_SPACETIME", "TheoreticalConstruct", "Curved Spacetime Manifold", "4-dimensional pseudo-Riemannian metric manifold."),
        ("TN_NEWTON_V1", "TheoryNet", "Classical Mechanics (v1)", "Unifying framework of Newton's laws and universal gravitation."),
        ("CORE_N_V1", "TheoryCore", "Newtonian Core", "Hard core of classical mechanics: laws of motion and gravitation."),
        ("TN_NEWTON_V2", "TheoryNet", "Classical Mechanics (v2)", "Revised Newtonian framework incorporating Vulcan perturbation."),
        ("CORE_N_V2", "TheoryCore", "Newtonian Core (Revised)", "Revised hard core of Newtonian mechanics."),
        ("TN_RELATIVITY_V1", "TheoryNet", "General Relativity (v1)", "Einsteinian geometric theory of gravitation."),
        ("CORE_REL_V1", "TheoryCore", "Einsteinian Core", "Hard core of General Relativity: Equivalence Principle & field equations."),
        ("TN_ELECTRO", "TheoryNet", "Classical Electromagnetism", "Maxwellian electromagnetic field theory."),
        ("APP_JUP_V1", "EmpiricalApplication", "Jupiter Orbit Application", "Application predicting Jupiter's orbital kinematics."),
        ("APP_MERC_REL", "EmpiricalApplication", "Mercury Precession Application", "Application explaining Mercury's 43 arcsec precession."),
    ]
    for eid, etype, name, desc in entities:
        _write_envelope(
            run_art_dir,
            f"entity_{eid}",
            "linked_entity",
            {
                "entity_id": eid,
                "entity_type": etype,
                "canonical_name": name,
                "description": desc,
                "confidence": 0.95,
                "source_chunk_ids": ["chunk_phys_1"],
            },
            run_id,
            "Phase 2: Entity & Local Relation Discovery",
        )

    # 3. Triples / Relations (L2)
    l2_relations = [
        ("rel_ei_tc", "EI_TELE", "MEASURES", "TC_ORBIT"),
        ("rel_tc_pt", "TC_ORBIT", "DETERMINED_BY", "PT_DIST"),
        ("rel_core_tn1", "CORE_N_V1", "BELONGS_TO", "TN_NEWTON_V1"),
        ("rel_core_tn2", "CORE_N_V2", "BELONGS_TO", "TN_NEWTON_V2"),
        ("rel_core_evolves", "CORE_N_V1", "EVOLVES_TO", "CORE_N_V2"),
        ("rel_tn_evolves", "TN_NEWTON_V1", "EVOLVES_TO", "TN_NEWTON_V2"),
        ("rel_core_rel", "CORE_REL_V1", "BELONGS_TO", "TN_RELATIVITY_V1"),
        ("rel_app_jup", "APP_JUP_V1", "BELONGS_TO", "TN_NEWTON_V1"),
        ("rel_app_merc", "APP_MERC_REL", "BELONGS_TO", "TN_RELATIVITY_V1"),
        ("rel_rel_subsumes", "TN_RELATIVITY_V1", "SUBSUMES", "TN_NEWTON_V1"),
        ("rel_rel_reduces", "TN_RELATIVITY_V1", "REDUCES_TO", "TN_NEWTON_V1"),
    ]
    for rid, src, pred, tgt in l2_relations:
        _write_envelope(
            run_art_dir,
            rid,
            "global_relation",
            {
                "relation_id": rid,
                "subject_entity_id": src,
                "predicate": pred,
                "object_entity_id": tgt,
                "confidence": 0.95,
                "scope": "global",
            },
            run_id,
            "Phase 3: Global Relation Extraction",
        )

    # 4. Theory Atoms (L3)
    atoms = [
        ("EV_JUPITER", "Evidence", "Jupiter's orbit follows predicted elliptical path.", "Success", 1.0, 1.0),
        ("EV_MERCURY", "Evidence", "Mercury's perihelion precesses by 43 arcseconds/century more than predicted.", "Anomaly", 1.0, 1.0),
        ("EV_NO_VULCAN", "Evidence", "Telescopic searches reveal no intramercurial planet.", "Failure", 1.0, 1.0),
        ("AX_GRAVITY", "BasicAxiom", "F = G(m1m2)/r^2", "A", 0.98, 1.0),
        ("AX_MOTION", "BasicAxiom", "F = ma", "A", 0.98, 1.0),
        ("DL_KEPLER", "DerivedEmpiricalLaw", "Planets orbit in ellipses.", "B", 0.95, 0.95),
        ("HYP_VULCAN", "Claim", "An unseen planet 'Vulcan' exerts gravitational pull on Mercury.", "A", 0.4, 0.3),
        ("AX_EQUIV", "BasicAxiom", "Equivalence Principle (Inertial mass = Gravitational mass)", "A", 0.99, 1.0),
        ("DL_GEODESIC", "DerivedEmpiricalLaw", "Objects follow geodesics in curved spacetime.", "B", 0.98, 0.99),
        ("AX_COULOMB", "BasicAxiom", "F = k(q1q2)/r^2", "A", 0.95, 1.0),
    ]
    for aid, atype, text, part, conf, plaus in atoms:
        _write_envelope(
            run_art_dir,
            f"atom_{aid}",
            "theory_atom",
            {
                "component_id": aid,
                "component_type": atype,
                "text": text,
                "epistemic_status": part,
                "confidence": conf,
                "plausibility": plaus,
                "source_chunk_id": "chunk_phys_2",
            },
            run_id,
            "Phase 4: Argument Mining",
        )

    # 5. Theory Relations (L3)
    theory_relations = [
        ("trel_grav_kep", "AX_GRAVITY", "SUPPORTS", "DL_KEPLER", 1.0),
        ("trel_mot_kep", "AX_MOTION", "SUPPORTS", "DL_KEPLER", 1.0),
        ("trel_kep_jup", "DL_KEPLER", "EXPLAINS", "APP_JUP_V1", 0.95),
        ("trel_jup_ev", "APP_JUP_V1", "MATCHES_EVIDENCE", "EV_JUPITER", 1.0),
        ("trel_vulc_merc", "HYP_VULCAN", "RESOLVES_ANOMALY", "EV_MERCURY", 0.4),
        ("trel_novulc_att", "EV_NO_VULCAN", "ATTACKS", "HYP_VULCAN", -1.0),
        ("trel_eq_geo", "AX_EQUIV", "SUPPORTS", "DL_GEODESIC", 1.0),
        ("trel_geo_merc", "DL_GEODESIC", "EXPLAINS", "APP_MERC_REL", 0.99),
        ("trel_merc_ev", "APP_MERC_REL", "MATCHES_EVIDENCE", "EV_MERCURY", 1.0),
        ("trel_rel_space_att", "CORE_REL_V1", "ATTACKS", "TC_ABS_SPACE", -0.9),
        ("trel_rel_vulc_att", "APP_MERC_REL", "ATTACKS", "HYP_VULCAN", -0.9),
        ("trel_coul_grav_analog", "AX_COULOMB", "ANALOGOUS_TO", "AX_GRAVITY", 0.85),
    ]
    for trid, src, rtype, tgt, weight in theory_relations:
        _write_envelope(
            run_art_dir,
            trid,
            "theory_relation",
            {
                "relation_id": trid,
                "source_component_id": src,
                "relation_type": rtype,
                "target_component_id": tgt,
                "weight": weight,
                "confidence": abs(weight),
                "scope": "global",
            },
            run_id,
            "Phase 5: Inter-Document Argument Web",
        )

    # Run Manifest
    manifest = {
        "run_id": run_id,
        "pipeline_version": "0.1.0",
        "schema_version": "v1",
        "status": "completed",
        "created_at": "2026-09-01T10:00:00Z",
        "started_at": "2026-09-01T10:00:05Z",
        "completed_at": "2026-09-01T10:04:25Z",
        "duration_seconds": 260.0,
        "primary_input": "physics_comprehensive_paradigms.cypher",
        "input_sources": ["datasets/physics_comprehensive_paradigms.cypher"],
        "tags": ["demo", "physics", "paradigm-shift", "general-relativity"],
        "models": {
            "llm_model": "anthropic/claude-3-5-sonnet",
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "reranker_model": "Alibaba-NLP/gte-reranker-modernbert-base",
            "thinking_level": "high",
        },
        "phase_records": [
            {"ordinal": 1, "phase_name": "Phase 1: Data Foundation", "status": "completed", "reused": False, "artifact_count": 6},
            {"ordinal": 2, "phase_name": "Phase 2: Entity & Local Relation Discovery", "status": "completed", "reused": False, "artifact_count": 15},
            {"ordinal": 3, "phase_name": "Phase 3: Global Relation Extraction", "status": "completed", "reused": False, "artifact_count": 11},
            {"ordinal": 4, "phase_name": "Phase 3b: Latent Graph Consolidation", "status": "completed", "reused": False, "artifact_count": 5},
            {"ordinal": 5, "phase_name": "Phase 4: Entity Maturation", "status": "completed", "reused": False, "artifact_count": 15},
            {"ordinal": 6, "phase_name": "Phase 4: Argument Mining", "status": "completed", "reused": False, "artifact_count": 10},
            {"ordinal": 7, "phase_name": "Phase 5: Inter-Document Argument Web", "status": "completed", "reused": False, "artifact_count": 12},
            {"ordinal": 8, "phase_name": "Phase 6: TheoryNet Projection", "status": "completed", "reused": False, "artifact_count": 8},
        ],
        "artifact_counts_by_kind": {
            "document": 1,
            "chunk": 5,
            "entity": 15,
            "global_relation": 11,
            "theory_atom": 10,
            "theory_relation": 12,
        },
        "config_snapshot": {
            "default_embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "models": {
                "llm_model": "anthropic/claude-3-5-sonnet",
                "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
                "reranker_model": "Alibaba-NLP/gte-reranker-modernbert-base",
            },
            "graph_schema": {
                "version": "v1",
                "node_types": ["PrimitiveTerm", "EmpiricalIndicator", "TheoreticalConstruct", "TheoryNet", "TheoryCore", "EmpiricalApplication"],
                "relation_types": ["MEASURES", "DETERMINED_BY", "BELONGS_TO", "EVOLVES_TO", "SUBSUMES", "REDUCES_TO"],
                "component_types": ["BasicAxiom", "DerivedEmpiricalLaw", "Evidence", "Claim"],
                "argument_relation_types": ["SUPPORTS", "EXPLAINS", "MATCHES_EVIDENCE", "RESOLVES_ANOMALY", "ATTACKS", "ANALOGOUS_TO"],
                "relation_polarities": {
                    "SUPPORTS": 1,
                    "EXPLAINS": 1,
                    "MATCHES_EVIDENCE": 1,
                    "RESOLVES_ANOMALY": 1,
                    "ANALOGOUS_TO": 1,
                    "ATTACKS": -1,
                },
                "component_partitions": {
                    "BasicAxiom": "A",
                    "Claim": "A",
                    "DerivedEmpiricalLaw": "B",
                    "Evidence": "B",
                },
            },
        },
        "fingerprints": {},
    }
    (runs_dir / f"{run_id}.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def _generate_psychology_run(runs_dir: Path, artifacts_dir: Path) -> None:
    run_id = "run-demo-psychology"
    run_art_dir = artifacts_dir / run_id
    run_art_dir.mkdir(parents=True, exist_ok=True)

    # 1. Document & Chunks (L1)
    _write_envelope(
        run_art_dir,
        "doc_psychology",
        "document",
        {
            "id": "doc_psychology",
            "title": "Paradigm Shifts in Psychology: Phobia Etiology Models",
            "filename": "psychology_paradigms.cypher",
            "author": "Sigmund Freud / B.F. Skinner / Joseph LeDoux",
        },
        run_id,
        "Phase 1: Data Foundation",
    )

    chunks = [
        ("chunk_psych_1", "Shared empirical grounding: Elevated heart rate, fMRI amygdala hyperactivation, and ancestral venomous threats."),
        ("chunk_psych_2", "Freudian psychoanalysis: Phobia as symbolic displacement of repressed psychosexual trauma."),
        ("chunk_psych_3", "Classical behaviorism: Phobia as direct conditioned reflex from painful traumatic events."),
        ("chunk_psych_4", "Evolutionary neuroscience: Phobia as hyper-sensitized evolutionary threat-detection circuit in the amygdala."),
        ("chunk_psych_5", "Paradigm conflict: Epistemic safety, conservatism, and mutual attacks between neuroscientific and clinical models."),
    ]
    for cid, text in chunks:
        _write_envelope(
            run_art_dir,
            cid,
            "chunk",
            {
                "id": cid,
                "text": text,
                "chunk_index": int(cid.split("_")[-1]),
                "confidence": 1.0,
            },
            run_id,
            "Phase 1: Data Foundation",
        )

    # 2. Entities (L2)
    entities = [
        ("T_FREUD", "Theory", "Freudian Psychoanalysis", "Spider phobia as displaced psychosexual conflict."),
        ("T_BEHAVIOR", "Theory", "Classical Behaviorism", "Spider phobia as a purely conditioned associative reflex."),
        ("T_NEURO", "Theory", "Evolutionary Neuroscience", "Spider phobia as hyper-sensitized, evolutionary threat-detection."),
    ]
    for eid, etype, name, desc in entities:
        _write_envelope(
            run_art_dir,
            f"entity_{eid}",
            "linked_entity",
            {
                "entity_id": eid,
                "entity_type": etype,
                "canonical_name": name,
                "description": desc,
                "confidence": 0.95,
                "source_chunk_ids": ["chunk_psych_1"],
            },
            run_id,
            "Phase 2: Entity & Local Relation Discovery",
        )

    # 3. Theory Atoms (L3)
    atoms = [
        ("E1", "EmpiricalSentence", "Subject exhibits elevated heart rate and avoidance behavior when exposed to spiders.", "B", 1.0, 1.0),
        ("E2", "EmpiricalSentence", "fMRI scans show severe hyperactivation in the amygdala during spider exposure.", "B", 1.0, 1.0),
        ("E3", "EmpiricalSentence", "Venomous spiders posed a lethal threat to early hominid ancestors.", "B", 1.0, 1.0),
        ("PB1", "Premise", "The spider is a symbolic displacement of a phallic threat or repressed psychosexual childhood trauma.", "A", 0.5, 0.3),
        ("PB2", "Premise", "The Ego represses trauma into the unconscious to prevent psychological fragmentation.", "A", 0.6, 0.4),
        ("CB", "Claim", "The phobia is a neurotic defense mechanism to avoid confronting repressed childhood conflicts.", "A", 0.4, 0.35),
        ("PC1", "Premise", "The subject experienced a direct, painful conditioning event involving a spider in the past.", "A", 0.7, 0.6),
        ("CC", "Claim", "Phobias are strictly learned associative reflexes (Pavlovian conditioning).", "A", 0.65, 0.6),
        ("PA1", "Premise", "The amygdala is the brain's primary threat-detection and fear-processing center.", "A", 0.95, 0.95),
        ("PA2", "Premise", "Innate fear of historic evolutionary threats provides a survival advantage.", "A", 0.9, 0.9),
        ("CA", "Claim", "Phobias are hyper-sensitized, evolutionary threat-detection circuits localized in the amygdala.", "A", 0.95, 0.95),
    ]
    for aid, atype, text, part, conf, plaus in atoms:
        _write_envelope(
            run_art_dir,
            f"atom_{aid}",
            "theory_atom",
            {
                "component_id": aid,
                "component_type": atype,
                "text": text,
                "epistemic_status": part,
                "confidence": conf,
                "plausibility": plaus,
                "source_chunk_id": "chunk_psych_1",
            },
            run_id,
            "Phase 4: Argument Mining",
        )

    # 4. Theory Relations (L3)
    relations = [
        # Freud chain
        ("trel_pb1_tf", "PB1", "BELONGS_TO", "T_FREUD", 1.0),
        ("trel_pb2_tf", "PB2", "BELONGS_TO", "T_FREUD", 1.0),
        ("trel_cb_tf", "CB", "BELONGS_TO", "T_FREUD", 1.0),
        ("trel_e1_pb1", "E1", "SUPPORTS", "PB1", 0.2),
        ("trel_pb1_pb2", "PB1", "SUPPORTS", "PB2", 0.3),
        ("trel_pb2_cb", "PB2", "SUPPORTS", "CB", 0.4),
        # Behaviorism chain
        ("trel_pc1_tc", "PC1", "BELONGS_TO", "T_BEHAVIOR", 1.0),
        ("trel_cc_tc", "CC", "BELONGS_TO", "T_BEHAVIOR", 1.0),
        ("trel_e1_pc1", "E1", "SUPPORTS", "PC1", 0.7),
        ("trel_pc1_cc", "PC1", "SUPPORTS", "CC", 0.8),
        # Neuroscience chain
        ("trel_pa1_ta", "PA1", "BELONGS_TO", "T_NEURO", 1.0),
        ("trel_pa2_ta", "PA2", "BELONGS_TO", "T_NEURO", 1.0),
        ("trel_ca_ta", "CA", "BELONGS_TO", "T_NEURO", 1.0),
        ("trel_e2_pa1", "E2", "SUPPORTS", "PA1", 0.95),
        ("trel_e3_pa2", "E3", "SUPPORTS", "PA2", 0.90),
        ("trel_pa1_ca", "PA1", "SUPPORTS", "CA", 0.95),
        ("trel_pa2_ca", "PA2", "SUPPORTS", "CA", 0.90),
        ("trel_e1_ca", "E1", "SUPPORTS", "CA", 0.85),
        # Paradigm conflicts
        ("trel_ca_att_cb", "CA", "ATTACKS", "CB", -0.9),
        ("trel_cc_att_cb", "CC", "ATTACKS", "CB", -0.6),
        ("trel_cb_att_cc", "CB", "ATTACKS", "CC", -0.6),
        ("trel_ca_att_cc", "CA", "ATTACKS", "CC", -0.4),
    ]
    for trid, src, rtype, tgt, weight in relations:
        _write_envelope(
            run_art_dir,
            trid,
            "theory_relation",
            {
                "relation_id": trid,
                "source_component_id": src,
                "relation_type": rtype,
                "target_component_id": tgt,
                "weight": weight,
                "confidence": abs(weight),
                "scope": "global",
            },
            run_id,
            "Phase 5: Inter-Document Argument Web",
        )

    # Run Manifest
    manifest = {
        "run_id": run_id,
        "pipeline_version": "0.1.0",
        "schema_version": "v1",
        "status": "completed",
        "created_at": "2026-09-01T11:00:00Z",
        "started_at": "2026-09-01T11:00:05Z",
        "completed_at": "2026-09-01T11:03:45Z",
        "duration_seconds": 220.0,
        "primary_input": "psychology_paradigms.cypher",
        "input_sources": ["datasets/psychology_paradigms.cypher"],
        "tags": ["demo", "psychology", "paradigm-conflict", "epistemic-safety"],
        "models": {
            "llm_model": "openai/gpt-4o",
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "reranker_model": "Alibaba-NLP/gte-reranker-modernbert-base",
            "thinking_level": "medium",
        },
        "phase_records": [
            {"ordinal": 1, "phase_name": "Phase 1: Data Foundation", "status": "completed", "reused": False, "artifact_count": 6},
            {"ordinal": 2, "phase_name": "Phase 2: Entity & Local Relation Discovery", "status": "completed", "reused": False, "artifact_count": 3},
            {"ordinal": 3, "phase_name": "Phase 3: Global Relation Extraction", "status": "completed", "reused": False, "artifact_count": 0},
            {"ordinal": 4, "phase_name": "Phase 3b: Latent Graph Consolidation", "status": "completed", "reused": False, "artifact_count": 2},
            {"ordinal": 5, "phase_name": "Phase 4: Entity Maturation", "status": "completed", "reused": False, "artifact_count": 3},
            {"ordinal": 6, "phase_name": "Phase 4: Argument Mining", "status": "completed", "reused": False, "artifact_count": 11},
            {"ordinal": 7, "phase_name": "Phase 5: Inter-Document Argument Web", "status": "completed", "reused": False, "artifact_count": 22},
            {"ordinal": 8, "phase_name": "Phase 6: TheoryNet Projection", "status": "completed", "reused": False, "artifact_count": 5},
        ],
        "artifact_counts_by_kind": {
            "document": 1,
            "chunk": 5,
            "entity": 3,
            "theory_atom": 11,
            "theory_relation": 22,
        },
        "config_snapshot": {
            "default_embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "models": {
                "llm_model": "openai/gpt-4o",
                "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
                "reranker_model": "Alibaba-NLP/gte-reranker-modernbert-base",
            },
            "graph_schema": {
                "version": "v1",
                "node_types": ["Theory"],
                "relation_types": ["BELONGS_TO"],
                "component_types": ["EmpiricalSentence", "Premise", "Claim"],
                "argument_relation_types": ["SUPPORTS", "ATTACKS", "BELONGS_TO"],
                "relation_polarities": {
                    "SUPPORTS": 1,
                    "BELONGS_TO": 1,
                    "ATTACKS": -1,
                },
                "component_partitions": {
                    "Premise": "A",
                    "Claim": "A",
                    "EmpiricalSentence": "B",
                },
            },
        },
        "fingerprints": {},
    }
    (runs_dir / f"{run_id}.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


if __name__ == "__main__":
    generate_fixtures()
    print("Demo fixtures successfully generated in episteme_studio/fixtures/")
