import json
import xml.etree.ElementTree as ET
from typing import Any
from episteme_pipeline.contracts.domain import TheoryAtom, TheoryRelation

def load_arg_microtexts_subset(path: str, limit: int = 5) -> dict[str, Any]:
    """
    Load and map a subset of the Arg-Microtexts dataset to Grund GLP domain objects.
    This expects a specific JSON representation or a directory of XML files.
    Here we implement a simplified JSON adapter for the subset.
    """
    atoms = []
    relations = []
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        for i, doc in enumerate(data[:limit]):
            doc_id = doc.get("id", f"doc_{i}")
            components = doc.get("components", [])
            rels = doc.get("relations", [])
            
            for comp in components:
                atom = TheoryAtom(
                    id=comp["id"],
                    text=comp["text"],
                    component_type=comp.get("type", "CLAIM"),
                    confidence=1.0,
                    document_id=doc_id
                )
                atoms.append(atom)
                
            for rel in rels:
                relation = TheoryRelation(
                    source_id=rel["source_id"],
                    target_id=rel["target_id"],
                    relation_type=rel.get("type", "SUPPORTS"),
                    confidence=1.0,
                    document_id=doc_id
                )
                relations.append(relation)
                
    except Exception as e:
        print(f"Error loading Arg-Microtexts from {path}: {e}")

    return {
        "metadata": {"dataset_type": "arg_microtexts", "limit": limit},
        "l2_entities": [],
        "l2_triples": [],
        "l3_atoms": atoms,
        "l3_relations": relations
    }
