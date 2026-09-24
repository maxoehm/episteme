// ==============================================================================
// Grund GLP - Example Dataset: Paradigm Shifts in Psychology
// Demonstrates: Epistemic Safety, Conservatism, and LPG-ECHO dynamics.
// 
// Instructions: Copy and paste this entire script into your Neo4j Browser.
// ==============================================================================

// Optional: Uncomment the line below to clear the database before loading
// MATCH (n) DETACH DELETE n;

// ==========================================
// 1. SHARED EMPIRICAL GROUNDING (Observation Laws)
// ==========================================
CREATE (e1:EmpiricalSentence {id: "E1", text: "Subject exhibits elevated heart rate and avoidance behavior when exposed to spiders.", confidence: 1.0})
CREATE (e2:EmpiricalSentence {id: "E2", text: "fMRI scans show severe hyperactivation in the amygdala during spider exposure.", confidence: 1.0})
CREATE (e3:EmpiricalSentence {id: "E3", text: "Venomous spiders posed a lethal threat to early hominid ancestors.", confidence: 1.0})

// ==========================================
// 2. THEORY B: The "Bad" Theory (Classical Freudian Psychoanalysis)
// ==========================================
CREATE (tb:Theory {id: "T_FREUD", name: "Freudian Psychoanalysis", description: "Spider phobia as displaced psychosexual conflict."})

CREATE (pb1:Premise {id: "PB1", text: "The spider is a symbolic displacement of a phallic threat or repressed psychosexual childhood trauma."})-[:BELONGS_TO]->(tb)
CREATE (pb2:Premise {id: "PB2", text: "The Ego represses trauma into the unconscious to prevent psychological fragmentation."})-[:BELONGS_TO]->(tb)
CREATE (cb:Claim {id: "CB", text: "The phobia is a neurotic defense mechanism to avoid confronting repressed childhood conflicts."})-[:BELONGS_TO]->(tb)

// Long, tenuous reasoning chain (Low Epistemic Safety, Low Conservatism)
CREATE (e1)-[:SUPPORTS {weight: 0.2}]->(pb1)
CREATE (pb1)-[:SUPPORTS {weight: 0.3}]->(pb2)
CREATE (pb2)-[:SUPPORTS {weight: 0.4}]->(cb)

// ==========================================
// 3. THEORY C: The "In-Between" Theory (Classical Behaviorism)
// ==========================================
CREATE (tc:Theory {id: "T_BEHAVIOR", name: "Classical Behaviorism", description: "Spider phobia as a purely conditioned reflex."})

CREATE (pc1:Premise {id: "PC1", text: "The subject experienced a direct, painful conditioning event involving a spider in the past."})-[:BELONGS_TO]->(tc)
CREATE (cc:Claim {id: "CC", text: "Phobias are strictly learned associative reflexes (Pavlovian conditioning)."})-[:BELONGS_TO]->(tc)

// Moderate reasoning chain, but ignores E2 and E3
CREATE (e1)-[:SUPPORTS {weight: 0.7}]->(pc1)
CREATE (pc1)-[:SUPPORTS {weight: 0.8}]->(cc)

// ==========================================
// 4. THEORY A: The "Good" Theory (Evolutionary Neuroscience)
// ==========================================
CREATE (ta:Theory {id: "T_NEURO", name: "Evolutionary Neuroscience", description: "Spider phobia as hyper-sensitized, evolutionary threat-detection."})

CREATE (pa1:Premise {id: "PA1", text: "The amygdala is the brain's primary threat-detection and fear-processing center."})-[:BELONGS_TO]->(ta)
CREATE (pa2:Premise {id: "PA2", text: "Innate fear of historic evolutionary threats provides a survival advantage."})-[:BELONGS_TO]->(ta)
CREATE (ca:Claim {id: "CA", text: "Phobias are hyper-sensitized, evolutionary threat-detection circuits localized in the amygdala."})-[:BELONGS_TO]->(ta)

// Short, highly safe paths grounded in objective MRT and evolutionary data
CREATE (e2)-[:SUPPORTS {weight: 0.95}]->(pa1)
CREATE (e3)-[:SUPPORTS {weight: 0.90}]->(pa2)
CREATE (pa1)-[:SUPPORTS {weight: 0.95}]->(ca)
CREATE (pa2)-[:SUPPORTS {weight: 0.90}]->(ca)
// Neuroscience also explains the behavioral symptom directly
CREATE (e1)-[:SUPPORTS {weight: 0.85}]->(ca)

// ==========================================
// 5. PARADIGM CONFLICTS (For LPG-ECHO Algorithm)
// ==========================================
// Neuroscience heavily attacks the ungrounded Freudian claim
CREATE (ca)-[:ATTACKS {weight: -0.9}]->(cb)

// Behaviorism and Freud are mutually incompatible explanations
CREATE (cc)-[:ATTACKS {weight: -0.6}]->(cb)
CREATE (cb)-[:ATTACKS {weight: -0.6}]->(cc)

// Neuroscience partially conflicts with pure Behaviorism (because fear isn't *purely* learned)
CREATE (ca)-[:ATTACKS {weight: -0.4}]->(cc)
