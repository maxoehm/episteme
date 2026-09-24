from pydantic import BaseModel, Field


L2_NODE_TYPES: list[str] = [
    "Concept",
    "Person",
    "Work",
    "Theory",
    "Institution"
]

L2_RELATION_TYPES: list[str] = [
    "RELATED_TO",
    "INSTANCE_OF",
    "PART_OF",
    "SUBCLASS_OF",
    "SUPPORTS",
    "REFUTES",
    "IMPLIES",
    "CONTRADICTS"
]

L2_NODE_DEFINITIONS: dict[str, str] = {
    "Concept": "Abstract idea, category, mental construct, or theoretical term (e.g. 'Justified True Belief', 'Working Memory').",
    "Person": "Individual thinker, scientist, philosopher, author, or historical figure (e.g. 'Edmund Gettier', 'Immanuel Kant').",
    "Work": "Publication, paper, treatise, book, or essay (e.g. 'Is Justified True Belief Knowledge?', 'Critique of Pure Reason').",
    "Theory": "Cohesive conceptual framework, formal model, doctrine, or system (e.g. 'Classical Theory of Knowledge', 'Behaviorism').",
    "Institution": "Academic school, university, research group, movement, or organization (e.g. 'Vienna Circle', 'Harvard University').",
}

L2_RELATION_DEFINITIONS: dict[str, str] = {
    "RELATED_TO": "General associative semantic connection between entities.",
    "INSTANCE_OF": "Entity is a concrete realization or token of a conceptual type.",
    "PART_OF": "Mereological containment or constituent sub-component.",
    "SUBCLASS_OF": "Taxonomic specialization or categorical subsumption.",
    "SUPPORTS": "Entity evidence or premise positively contributes to another.",
    "REFUTES": "Entity evidence or counterargument denies or falsifies another.",
    "IMPLIES": "Logical, causal, or inferential entailment from source to target.",
    "CONTRADICTS": "Direct propositional inconsistency or mutual exclusivity.",
}

L3_COMPONENT_TYPES: list[str] = [
    "ObservationUnit",
    "EmpiricalStatement",
    "TheoreticalHypothesis",
    "CoreExpansion"
]
L3_RELATION_TYPES: list[str] = [
    "ATTACKS",
    "SUPPORTS_ARG",
    "UNDERCUTS",
    "SPECIALIZES",
    "CONSTRAINS",
    "REDUCES_TO",
    "ENTAILS",
    "DEDUCES",
    "COHERES_WITH",
    "INHIBITS"
]

L3_COMPONENT_DEFINITIONS: dict[str, str] = {
    "ObservationUnit": "Singular or localized statements containing exclusively observational terms. Act as raw data nodes.",
    "EmpiricalStatement": "Statements containing only logical and empirical concepts.",
    "TheoreticalHypothesis": "Statements containing theoretical concepts or whose quantifiers have theoretical scope. These represent core laws or abstract hypotheses.",
    "CoreExpansion": "Special auxiliary laws and constraints that form a shifting superstructure around the stable theory core."
}

L3_RELATION_DEFINITIONS: dict[str, str] = {
    "ATTACKS": "Argument component attacks another (critical relationship).",
    "SUPPORTS_ARG": "Argument component provides support for another.",
    "UNDERCUTS": "Argument component undermines the inference of another.",
    "SPECIALIZES": "Directed vertical edges forming a hierarchy where a specialized node inherits and restricts properties from its parent.",
    "CONSTRAINS": "Lateral/horizontal edges crossing overlapping applications to ensure intrinsic properties remain constant.",
    "REDUCES_TO": "Intertheoretical links connecting entirely separate theories, including strict reduction from older to newer theories.",
    "ENTAILS": "Intertheoretical links connecting entirely separate theories, including strict reduction from older to newer theories.",
    "DEDUCES": "Logical entailments between nodes such as Explanation Patterns (Erklärungsschema) and Falsification Patterns (Falsifikationsschema).",
    "COHERES_WITH": "Positive (excitatory) connections between hypotheses that explain evidence, or co-hypotheses that jointly explain a fact.",
    "INHIBITS": "Negative (inhibitory) weights representing incoherence between logically contradictory or competing hypotheses."
}

RELATION_POLARITIES: dict[str, int] = {
    "RELATED_TO": 0,
    "INSTANCE_OF": 0,
    "PART_OF": 0,
    "SUBCLASS_OF": 0,
    "SUPPORTS": 1,
    "REFUTES": -1,
    "IMPLIES": 1,
    "CONTRADICTS": -1,
    "ATTACKS": -1,
    "SUPPORTS_ARG": 1,
    "UNDERCUTS": -1,
    "SPECIALIZES": 0,
    "CONSTRAINS": 0,
    "REDUCES_TO": 1,
    "ENTAILS": 1,
    "DEDUCES": 1,
    "COHERES_WITH": 1,
    "INHIBITS": -1
}


COMPONENT_PARTITIONS: dict[str, str] = {
    "ObservationUnit": "B",
    "EmpiricalStatement": "B",
    "TheoreticalHypothesis": "A",
    "CoreExpansion": "A"
}


class SchemaConfig(BaseModel):
    """
    Decoupled schema configuration — all node/edge types the pipeline uses.

    Pass a custom instance to PipelineConfig to override the defaults for a
    different domain. Prompt templates receive these lists as {entity_types}
    and {relation_types} at runtime.
    """

    version: str = "v1"
    node_types: list[str] = Field(default_factory=lambda: list(L2_NODE_TYPES))
    relation_types: list[str] = Field(default_factory=lambda: list(L2_RELATION_TYPES))
    node_definitions: dict[str, str] = Field(default_factory=lambda: dict(L2_NODE_DEFINITIONS))
    relation_definitions: dict[str, str] = Field(default_factory=lambda: dict(L2_RELATION_DEFINITIONS))
    component_types: list[str] = Field(default_factory=lambda: list(L3_COMPONENT_TYPES))
    argument_relation_types: list[str] = Field(default_factory=lambda: list(L3_RELATION_TYPES))
    component_definitions: dict[str, str] = Field(default_factory=lambda: dict(L3_COMPONENT_DEFINITIONS))
    argument_relation_definitions: dict[str, str] = Field(default_factory=lambda: dict(L3_RELATION_DEFINITIONS))
    relation_polarities: dict[str, int] = Field(default_factory=lambda: dict(RELATION_POLARITIES))
    component_partitions: dict[str, str] = Field(default_factory=lambda: dict(COMPONENT_PARTITIONS))

    def node_types_str(self) -> str:
        return ", ".join(self.node_types)

    def relation_types_str(self) -> str:
        return ", ".join(self.relation_types)

    def component_types_str(self) -> str:
        import json
        payload = {k: self.component_definitions.get(k, "No description provided.") for k in self.component_types}
        return json.dumps(payload, indent=2, ensure_ascii=False)

    def argument_relation_types_str(self) -> str:
        import json
        payload = {k: self.argument_relation_definitions.get(k, "No description provided.") for k in self.argument_relation_types}
        return json.dumps(payload, indent=2, ensure_ascii=False)


DEFAULT_SCHEMA = SchemaConfig()
