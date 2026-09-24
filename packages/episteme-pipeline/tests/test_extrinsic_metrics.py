"""Tests for extrinsic evaluation metrics."""

from episteme_pipeline.evaluation.extrinsic import calculate_mrr, calculate_hits_at_k, calculate_ndcg


class TestMRR:
    def test_mrr_perfect_ranking(self):
        rankings = [["a", "b", "c"]]
        gold_standards = [{"a"}]
        assert calculate_mrr(rankings, gold_standards) == 1.0

    def test_mrr_second_position(self):
        rankings = [["b", "a", "c"]]
        gold_standards = [{"a"}]
        assert calculate_mrr(rankings, gold_standards) == 0.5

    def test_mrr_no_relevant(self):
        rankings = [["b", "c", "d"]]
        gold_standards = [{"a"}]
        assert calculate_mrr(rankings, gold_standards) == 0.0

    def test_mrr_empty_input(self):
        assert calculate_mrr([], []) == 0.0


class TestHitsAtK:
    def test_hits_at_k_hit(self):
        rankings = [["a", "b", "c"]]
        gold_standards = [{"b"}]
        assert calculate_hits_at_k(rankings, gold_standards, k=2) == 1.0

    def test_hits_at_k_miss(self):
        rankings = [["a", "b", "c"]]
        gold_standards = [{"c"}]
        assert calculate_hits_at_k(rankings, gold_standards, k=2) == 0.0


class TestNDCG:
    def test_ndcg_perfect(self):
        rankings = [["a", "b", "c"]]
        gold_standards = [{"a": 1.0, "b": 0.5}]
        assert calculate_ndcg(rankings, gold_standards, k=3) == 1.0

    def test_ndcg_empty(self):
        assert calculate_ndcg([], []) == 0.0

    def test_ndcg_partial(self):
        rankings = [["c", "a", "b"]]
        gold_standards = [{"a": 1.0, "b": 0.5}]
        ndcg = calculate_ndcg(rankings, gold_standards, k=3)
        assert 0.0 < ndcg < 1.0


class TestMetricsBounded:
    def test_metrics_bounded(self):
        rankings = [["a", "b", "c"], ["d", "e", "f"]]
        gold_sets = [{"a", "c"}, {"g"}]
        gold_dicts = [{"a": 1.0, "c": 0.5}, {"g": 1.0}]
        
        mrr = calculate_mrr(rankings, gold_sets)
        assert 0.0 <= mrr <= 1.0
        
        hits = calculate_hits_at_k(rankings, gold_sets, k=2)
        assert 0.0 <= hits <= 1.0
        
        ndcg = calculate_ndcg(rankings, gold_dicts, k=2)
        assert 0.0 <= ndcg <= 1.0
