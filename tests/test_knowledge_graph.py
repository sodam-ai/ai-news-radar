"""ai/knowledge_graph.py — 태그 공동 출현 그래프 엣지 케이스."""
from __future__ import annotations

from ai.knowledge_graph import (
    build_graph,
    get_related_articles,
    get_top_connected_tags,
)


def _art(tags, importance=3, sentiment="neutral", category="ai_tool"):
    return {
        "id": "x",
        "tags": tags,
        "importance": importance,
        "sentiment": sentiment,
        "category": category,
    }


class TestBuildGraph:
    def test_empty_input(self):
        g = build_graph([])
        assert g["nodes"] == []
        assert g["edges"] == []
        assert g["total_articles"] == 0

    def test_single_article_single_tag(self):
        g = build_graph([_art(["claude"])])
        assert len(g["nodes"]) == 1
        assert g["nodes"][0]["id"] == "claude"
        assert g["edges"] == []

    def test_cooccurrence_edge(self):
        articles = [
            _art(["claude", "anthropic"]),
            _art(["claude", "anthropic"]),
        ]
        g = build_graph(articles, min_edge_weight=2)
        assert len(g["edges"]) == 1
        edge = g["edges"][0]
        assert set([edge["source"], edge["target"]]) == {"claude", "anthropic"}
        assert edge["weight"] == 2

    def test_min_edge_weight_filters_weak_edges(self):
        articles = [_art(["a", "b"])]
        g = build_graph(articles, min_edge_weight=2)
        assert g["edges"] == []

    def test_duplicate_tags_in_article_count_once(self):
        g = build_graph([_art(["claude", "claude", "CLAUDE"])])
        claude_nodes = [n for n in g["nodes"] if n["id"] == "claude"]
        assert len(claude_nodes) == 1
        assert claude_nodes[0]["count"] == 1

    def test_stopwords_filtered(self):
        g = build_graph([_art(["ai", "llm", "tool", "anthropic"])])
        node_ids = {n["id"] for n in g["nodes"]}
        assert "ai" not in node_ids
        assert "llm" not in node_ids
        assert "tool" not in node_ids
        assert "anthropic" in node_ids

    def test_numeric_tag_filtered(self):
        g = build_graph([_art(["2026", "gpt5"])])
        node_ids = {n["id"] for n in g["nodes"]}
        assert "2026" not in node_ids

    def test_short_tag_filtered(self):
        g = build_graph([_art(["a", "anthropic"])])
        node_ids = {n["id"] for n in g["nodes"]}
        assert "a" not in node_ids

    def test_long_tag_filtered(self):
        g = build_graph([_art(["x" * 50, "anthropic"])])
        node_ids = {n["id"] for n in g["nodes"]}
        assert ("x" * 50) not in node_ids

    def test_top_n_limit(self):
        articles = [_art([f"tag{i}"]) for i in range(100)]
        g = build_graph(articles, top_n=10)
        assert len(g["nodes"]) <= 10

    def test_sentiment_and_importance_aggregation(self):
        articles = [
            _art(["anthropic"], importance=5, sentiment="positive"),
            _art(["anthropic"], importance=3, sentiment="positive"),
            _art(["anthropic"], importance=1, sentiment="neutral"),
        ]
        g = build_graph(articles, min_edge_weight=1)
        node = next(n for n in g["nodes"] if n["id"] == "anthropic")
        assert node["count"] == 3
        assert node["sentiment_pos_pct"] == 67
        assert node["importance_avg"] == 3.0

    def test_tags_as_json_string(self):
        article = {
            "id": "x",
            "tags": '["claude", "anthropic"]',
            "importance": 3,
            "sentiment": "neutral",
            "category": "ai_tool",
        }
        g = build_graph([article])
        assert len(g["nodes"]) == 2

    def test_malformed_json_tags_safe(self):
        article = {
            "id": "x",
            "tags": "not valid json",
            "importance": 3,
            "sentiment": "neutral",
            "category": "ai_tool",
        }
        g = build_graph([article])
        assert g["nodes"] == []


class TestGetTopConnectedTags:
    def test_basic(self):
        articles = [
            _art(["anthropic", "claude"]),
            _art(["anthropic", "claude"]),
            _art(["anthropic", "gemini"]),
            _art(["anthropic", "gemini"]),
        ]
        g = build_graph(articles, min_edge_weight=2)
        top = get_top_connected_tags(g, n=3)
        assert len(top) > 0
        assert top[0]["id"] == "anthropic"

    def test_empty_graph(self):
        g = {"nodes": [], "edges": [], "total_articles": 0}
        assert get_top_connected_tags(g) == []


class TestGetRelatedArticles:
    def test_basic(self):
        articles = [
            {"id": "a1", "tags": ["claude"], "importance": 5, "category": "ai_tool", "sentiment": "positive"},
            {"id": "a2", "tags": ["claude", "anthropic"], "importance": 3, "category": "ai_tool", "sentiment": "neutral"},
            {"id": "a3", "tags": ["gemini"], "importance": 4, "category": "ai_tool", "sentiment": "positive"},
        ]
        related = get_related_articles("claude", articles)
        assert len(related) == 2
        assert related[0]["id"] == "a1"

    def test_case_insensitive(self):
        articles = [{"id": "a", "tags": ["Claude"], "importance": 1, "category": "ai_tool", "sentiment": "neutral"}]
        assert len(get_related_articles("CLAUDE", articles)) == 1

    def test_no_match_returns_empty(self):
        articles = [{"id": "a", "tags": ["x"], "importance": 1, "category": "ai_tool", "sentiment": "neutral"}]
        assert get_related_articles("nonexistent", articles) == []
