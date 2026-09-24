import json
from typing import Any

def load_scifact_subset(path: str, limit: int = 5) -> list[dict[str, Any]]:
    """
    Load a subset of the SciFact dataset for extrinsic retrieval evaluation.
    Returns a list of queries and their gold document/entity IDs.
    """
    queries = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines[:limit]:
            data = json.loads(line)
            query = data.get("claim", "")
            # Collect all evidence document IDs
            gold_ids = []
            for doc_id, evidences in data.get("evidence", {}).items():
                gold_ids.append(str(doc_id))
                
            queries.append({
                "query": query,
                "gold_ids": set(gold_ids)
            })
    except Exception as e:
        print(f"Error loading SciFact from {path}: {e}")
        
    return queries
