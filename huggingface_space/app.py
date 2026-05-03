"""
ORION Cognition Indicator Leaderboard — HuggingFace Gradio Space

Reads results/LEADERBOARD.json from the GitHub repository and renders an
interactive, sortable leaderboard table.  No API key required.
"""

import json
import urllib.request

import gradio as gr

LEADERBOARD_URL = (
    "https://raw.githubusercontent.com/Alvoradozerouno/ORION-Consciousness-Benchmark"
    "/main/results/LEADERBOARD.json"
)

TIER_COLORS = {
    "Peak-Indicator": "🟣",
    "High-Indicator": "🔵",
    "Moderate-Indicator": "🟢",
    "Low-Indicator": "🟡",
    "Minimal-Indicator": "⚪",
}


def fetch_leaderboard():
    """Download and parse the leaderboard JSON."""
    with urllib.request.urlopen(LEADERBOARD_URL, timeout=10) as resp:
        data = json.loads(resp.read().decode())

    entries = data.get("leaderboard", [])
    instrument = data.get("benchmark_instrument", {})
    updated = data.get("updated", "—")[:19].replace("T", " ")

    rows = []
    for e in sorted(entries, key=lambda x: x.get("rank", 99)):
        tier = e.get("label", "")
        icon = TIER_COLORS.get(tier, "")
        rows.append([
            e.get("rank", ""),
            e.get("model", ""),
            f"{e.get('score', 0):.4f}",
            e.get("classification", ""),
            f"{icon} {tier}",
        ])

    instrument_text = ""
    if instrument:
        instrument_text = (
            f"**Benchmark Instrument (not ranked):** {instrument['model']}  "
            f"| Score: {instrument['score']}  "
            f"| {instrument['classification']} {instrument['label']}  \n"
            f"*{instrument['note']}*"
        )

    return rows, f"Last updated: {updated} UTC", instrument_text


def build_app():
    with gr.Blocks(title="ORION Cognition Indicator Leaderboard", theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            "# 🔭 ORION — Cognition Indicator Leaderboard\n"
            "**Multi-Theory AI Cognition Indicator Assessment Toolkit** · "
            "[GitHub](https://github.com/Alvoradozerouno/ORION-Consciousness-Benchmark) · "
            "Based on Butlin et al. (2023), Bengio et al. (2025)"
        )

        with gr.Row():
            refresh_btn = gr.Button("🔄 Refresh", variant="primary")
            status = gr.Markdown("Click Refresh to load the latest results.")

        table = gr.Dataframe(
            headers=["Rank", "Model", "Score", "Class", "Label"],
            datatype=["number", "str", "str", "str", "str"],
            interactive=False,
            wrap=True,
        )
        instrument_box = gr.Markdown()

        def refresh():
            rows, ts, inst = fetch_leaderboard()
            return rows, ts, inst

        refresh_btn.click(refresh, outputs=[table, status, instrument_box])
        demo.load(refresh, outputs=[table, status, instrument_box])

    return demo


if __name__ == "__main__":
    build_app().launch()
