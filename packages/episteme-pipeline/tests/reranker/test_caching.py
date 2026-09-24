"""
Test script to demonstrate the model caching functionality in the reranker.
"""

import time
from episteme_pipeline.phases.phase3_global_relations.rerankers import SentenceTransformerCrossEncoderReranker


def test_model_caching():
    """Test that the model caching works correctly."""
    print("Testing model caching functionality...")
    
    # Create first reranker with caching enabled
    start_time = time.time()
    reranker1 = SentenceTransformerCrossEncoderReranker(
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
        cache_model=True
    )
    first_load_time = time.time() - start_time
    print(f"First model load time: {first_load_time:.2f} seconds")
    
    # Create second reranker with caching enabled - should use cached model
    start_time = time.time()
    reranker2 = SentenceTransformerCrossEncoderReranker(
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
        cache_model=True
    )
    second_load_time = time.time() - start_time
    print(f"Second model load time (cached): {second_load_time:.2f} seconds")
    
    # Check if the second load was significantly faster
    if second_load_time < first_load_time * 0.5:
        print("✓ Model caching is working - second load was significantly faster")
    else:
        print("⚠ Model caching may not be working - second load wasn't much faster")
    
    # Verify that both rerankers use the same model instance
    if reranker1.model is reranker2.model:
        print("✓ Both rerankers are using the same model instance")
    else:
        print("⚠ Rerankers are using different model instances")


if __name__ == "__main__":
    test_model_caching()
