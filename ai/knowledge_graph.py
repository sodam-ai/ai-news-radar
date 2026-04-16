"""AI 뉴스 지식 그래프 — 태그 공동 출현 기반 엔티티 관계 시각화.

LLM 없이 동작: 같은 기사에 함께 등장한 태그 쌍을 엣지로 구성.
"""
from collections import Counter, defaultdict
from typing import Any

# 너무 일반적이어서 그래프 노이즈가 되는 태그
_STOPWORDS = {
    # 영어 일반어
    "ai", "llm", "gpt", "model", "models", "tool", "tools",
    "update", "updates", "release", "releases", "new", "latest",
    "open", "source", "free", "based", "use", "using", "app", "apps",
    "api", "apis", "feature", "features", "company", "platform",
    "technology", "tech", "system", "systems", "data", "users",
    "user", "service", "services", "product", "products", "news",
    # 한국어 일반어
    "인공지능", "모델", "기술", "도구", "출시", "업데이트", "최신",
    "서비스", "플랫폼", "기업", "회사", "사용자", "기능", "제품",
    "공개", "발표", "지원", "제공", "활용", "개발", "시스템", "데이터",
    # 주식/재무 노이즈 (AI 그래프 범위 밖)
    "지분율", "주식", "공시", "주주총회", "재무제표", "배당금", "주주",
    "자본금", "거래량", "시가총액",
}

_MIN_TAG_LEN = 2
_MAX_TAG_LEN = 40


def _clean_tag(tag: str) -> str:
    return tag.strip().lower()


def _is_valid_tag(tag: str) -> bool:
    t = _clean_tag(tag)
    return (
        _MIN_TAG_LEN <= len(t) <= _MAX_TAG_LEN
        and t not in _STOPWORDS
        and not t.isdigit()
    )


def build_graph(
    articles: list[dict],
    top_n: int = 60,
    min_edge_weight: int = 2,
) -> dict[str, Any]:
    """태그 공동 출현 기반 지식 그래프 데이터 생성.

    Returns:
        {
          "nodes": [{"id", "label", "count", "category", "sentiment_pos_pct", "importance_avg"}],
          "edges": [{"source", "target", "weight"}],
          "total_articles": int,
        }
    """
    tag_count: Counter = Counter()
    tag_articles: dict[str, list[dict]] = defaultdict(list)
    cooccur: Counter = Counter()

    for article in articles:
        raw_tags = article.get("tags", [])
        if isinstance(raw_tags, str):
            import json
            try:
                raw_tags = json.loads(raw_tags)
            except Exception:
                raw_tags = []

        valid = [_clean_tag(t) for t in raw_tags if _is_valid_tag(t)]
        valid = list(dict.fromkeys(valid))  # 중복 제거 (순서 보존)

        for tag in valid:
            tag_count[tag] += 1
            tag_articles[tag].append(article)

        for i in range(len(valid)):
            for j in range(i + 1, len(valid)):
                pair = tuple(sorted([valid[i], valid[j]]))
                cooccur[pair] += 1

    # 상위 N개 노드만 사용
    top_tags = {tag for tag, _ in tag_count.most_common(top_n)}

    nodes = []
    for tag in top_tags:
        related = tag_articles[tag]
        pos_cnt = sum(1 for a in related if a.get("sentiment") == "positive")
        pos_pct = round(pos_cnt / max(len(related), 1) * 100)
        avg_imp = round(sum(a.get("importance", 0) for a in related) / max(len(related), 1), 1)
        # 가장 많이 연결된 카테고리
        cat_counter: Counter = Counter(a.get("category", "ai_other") for a in related)
        main_cat = cat_counter.most_common(1)[0][0] if cat_counter else "ai_other"

        nodes.append({
            "id": tag,
            "label": tag,
            "count": tag_count[tag],
            "category": main_cat,
            "sentiment_pos_pct": pos_pct,
            "importance_avg": avg_imp,
        })

    edges = []
    for (src, tgt), weight in cooccur.items():
        if src in top_tags and tgt in top_tags and weight >= min_edge_weight:
            edges.append({"source": src, "target": tgt, "weight": weight})

    return {
        "nodes": nodes,
        "edges": edges,
        "total_articles": len(articles),
    }


def build_plotly_figure(
    graph_data: dict,
    highlight_tag: str = "",
    color_by: str = "category",
) -> Any:
    """networkx spring_layout + Plotly Scatter로 인터랙티브 네트워크 그래프 생성."""
    import networkx as nx
    import plotly.graph_objects as go

    nodes = graph_data["nodes"]
    edges = graph_data["edges"]

    if not nodes:
        return None

    G = nx.Graph()
    for n in nodes:
        G.add_node(n["id"], **n)
    for e in edges:
        G.add_edge(e["source"], e["target"], weight=e["weight"])

    # 고립 노드 제거 (엣지 없는 노드)
    isolated = list(nx.isolates(G))
    G.remove_nodes_from(isolated)

    if len(G.nodes) == 0:
        return None

    pos = nx.spring_layout(G, seed=42, k=1.8 / (len(G.nodes) ** 0.5))

    # 카테고리 색상 팔레트
    CAT_COLORS = {
        "ai_tool": "#818cf8",
        "ai_research": "#c084fc",
        "ai_trend": "#fb923c",
        "ai_tutorial": "#34d399",
        "ai_business": "#f472b6",
        "ai_image_video": "#fb7185",
        "ai_coding": "#2dd4bf",
        "ai_ontology": "#a78bfa",
        "ai_other": "#94a3b8",
    }

    # 엣지 traces
    edge_x, edge_y = [], []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        mode="lines",
        line=dict(width=0.6, color="rgba(148,163,184,0.2)"),
        hoverinfo="none",
    )

    # 노드 traces
    node_x, node_y, node_text, node_color, node_size, node_hover = [], [], [], [], [], []
    for node_id in G.nodes():
        x, y = pos[node_id]
        nd = G.nodes[node_id]
        count = nd.get("count", 1)
        cat = nd.get("category", "ai_other")

        node_x.append(x)
        node_y.append(y)
        node_text.append(node_id)

        # 색상: highlight > category
        if highlight_tag and node_id == highlight_tag.lower():
            color = "#facc15"  # 강조 노란색
        elif color_by == "importance":
            imp = nd.get("importance_avg", 3)
            r = int(99 + (imp / 5) * 100)
            color = f"rgb({r}, 102, 241)"
        else:
            color = CAT_COLORS.get(cat, "#94a3b8")

        node_color.append(color)
        node_size.append(6 + min(count * 3, 28))  # 최소 6, 최대 34

        node_hover.append(
            f"<b>{node_id}</b><br>"
            f"기사 {count}개 · 중요도 {nd.get('importance_avg', 0)}<br>"
            f"긍정 {nd.get('sentiment_pos_pct', 0)}%<br>"
            f"카테고리: {cat}"
        )

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode="markers+text",
        text=node_text,
        textposition="top center",
        textfont=dict(size=9, color="rgba(236,236,239,0.85)"),
        marker=dict(
            size=node_size,
            color=node_color,
            line=dict(width=1, color="rgba(255,255,255,0.12)"),
        ),
        hovertext=node_hover,
        hoverinfo="text",
    )

    fig = go.Figure(
        data=[edge_trace, node_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode="closest",
            margin=dict(b=0, l=0, r=0, t=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=560,
        ),
    )
    return fig


def get_top_connected_tags(graph_data: dict, n: int = 10) -> list[dict]:
    """연결 수 기준 상위 태그 목록."""
    from collections import Counter
    degree: Counter = Counter()
    for e in graph_data["edges"]:
        degree[e["source"]] += e["weight"]
        degree[e["target"]] += e["weight"]
    top = degree.most_common(n)
    node_map = {nd["id"]: nd for nd in graph_data["nodes"]}
    return [
        {**node_map[tag], "degree": deg}
        for tag, deg in top
        if tag in node_map
    ]


def get_related_articles(tag: str, articles: list[dict], limit: int = 10) -> list[dict]:
    """특정 태그와 연결된 기사 반환."""
    tag_lower = tag.lower()
    matched = [
        a for a in articles
        if any(_clean_tag(t) == tag_lower for t in a.get("tags", []))
    ]
    return sorted(matched, key=lambda x: x.get("importance", 0), reverse=True)[:limit]
