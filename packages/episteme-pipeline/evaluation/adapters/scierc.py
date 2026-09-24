import json
from typing import Any
from episteme_pipeline.contracts.domain import L2Entity, L2Triple

def load_scierc_subset(path: str, limit: int = 5) -> dict[str, Any]:
    """
    Load and map a subset of the SciERC dataset to Grund GLP domain objects.
    
    SciERC format typically includes:
    - sentences: list of lists of tokens
    - ner: list of lists of [start, end, label]
    - relations: list of lists of [start1, end1, start2, end2, relation_label]
    """
    entities = []
    triples = []
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for i, line in enumerate(lines[:limit]):
            data = json.loads(line)
            doc_id = data.get("doc_key", f"doc_{i}")
            sentences = data.get("sentences", [])
            ner = data.get("ner", [])
            relations = data.get("relations", [])
            
            # Flatten tokens for easier index mapping
            tokens = [token for sentence in sentences for token in sentence]
            
            # Map entities
            entity_map = {} # (start, end) -> L2Entity
            for ner_list in ner:
                for span in ner_list:
                    start, end, label = span
                    text = " ".join(tokens[start:end+1])
                    ent_id = f"{doc_id}_ent_{start}_{end}"
                    entity = L2Entity(
                        id=ent_id,
                        name=text,
                        label=label,
                        description="",
                        is_mature=True,
                        document_id=doc_id
                    )
                    entities.append(entity)
                    entity_map[(start, end)] = entity
            
            # Map relations
            for rel_list in relations:
                for rel in rel_list:
                    start1, end1, start2, end2, rel_type = rel
                    head_ent = entity_map.get((start1, end1))
                    tail_ent = entity_map.get((start2, end2))
                    
                    if head_ent and tail_ent:
                        triple = L2Triple(
                            subject_id=head_ent.id,
                            predicate=rel_type,
                            object_id=tail_ent.id,
                            confidence=1.0,
                            document_id=doc_id
                        )
                        triples.append(triple)
                        
    except Exception as e:
        print(f"Error loading SciERC from {path}: {e}")

    return {
        "metadata": {"dataset_type": "scierc", "limit": limit},
        "l2_entities": entities,
        "l2_triples": triples,
        "l3_atoms": [],
        "l3_relations": []
    }
