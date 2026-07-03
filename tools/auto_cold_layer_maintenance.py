from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import argparse
import json
import math
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
PROJECT_MEMORY = ROOT / ".project-memory"
OUTPUT_DIR = ROOT / "outputs" / "harness-maintenance"

HOT_FILES = {
    "AGENTS.md",
    "PROJECT-WORKFLOW.md",
    ".project-memory/README.md",
    ".project-memory/tool-delivery-routing.md",
    ".project-memory/automation-entrypoints.md",
    ".project-memory/plugin-mcp-governance.md",
    ".project-memory/capability-fallback-matrix.md",
    ".project-memory/text-selector-questioning-protocol.md",
}

REFERENCE_ROOTS = [
    ROOT / "AGENTS.md",
    ROOT / "PROJECT-WORKFLOW.md",
    *sorted(PROJECT_MEMORY.rglob("*.md")),
]


@dataclass
class FileStat:
    rel_path: str
    lines: int
    chars: int
    tokens: int
    inbound_refs: int
    heading_count: int


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def approx_token_count(text: str) -> int:
    ascii_chars = len(re.findall(r"[\x00-\x7F]", text))
    cjk_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    other_chars = max(0, len(text) - ascii_chars - cjk_chars)
    estimate = ascii_chars / 3.2 + cjk_chars * 1.15 + other_chars / 2.2
    return math.ceil(estimate)


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def collect_inbound_refs(paths: list[Path]) -> Counter[str]:
    refs: Counter[str] = Counter()
    rel_names = {rel_path(path): path.name for path in paths}
    for source in REFERENCE_ROOTS:
        if not source.exists():
            continue
        content = read_text(source)
        for rel_name, basename in rel_names.items():
            if basename in content or rel_name in content:
                refs[rel_name] += 1
    return refs


def extract_headings(text: str) -> list[str]:
    return [line.strip().lower() for line in text.splitlines() if line.strip().startswith("#")]


def normalized_lines(text: str) -> set[str]:
    lines = set()
    for line in text.splitlines():
        stripped = re.sub(r"\s+", " ", line.strip().lower())
        if len(stripped) < 8:
            continue
        if stripped.startswith("```") or stripped.startswith("#"):
            continue
        lines.add(stripped)
    return lines


def collect_stats() -> tuple[list[FileStat], dict[str, list[str]], list[tuple[str, str, int]]]:
    cold_paths = [
        path for path in sorted(PROJECT_MEMORY.rglob("*.md"))
        if rel_path(path) not in HOT_FILES
    ]
    inbound_refs = collect_inbound_refs(cold_paths)
    heading_map: dict[str, list[str]] = defaultdict(list)
    line_sets: dict[str, set[str]] = {}
    stats: list[FileStat] = []

    for path in cold_paths:
        text = read_text(path)
        rel = rel_path(path)
        headings = extract_headings(text)
        for heading in headings:
            heading_map[heading].append(rel)
        line_sets[rel] = normalized_lines(text)
        stats.append(
            FileStat(
                rel_path=rel,
                lines=len(text.splitlines()),
                chars=len(text),
                tokens=approx_token_count(text),
                inbound_refs=inbound_refs[rel],
                heading_count=len(headings),
            )
        )

    overlap_pairs: list[tuple[str, str, int]] = []
    rels = [stat.rel_path for stat in stats]
    for idx, left in enumerate(rels):
        for right in rels[idx + 1 :]:
            overlap = len(line_sets[left] & line_sets[right])
            if overlap >= 3:
                overlap_pairs.append((left, right, overlap))

    overlap_pairs.sort(key=lambda item: item[2], reverse=True)
    return stats, heading_map, overlap_pairs


def score_candidate(stat: FileStat, total_cold_files: int) -> float:
    size_score = stat.tokens / 180
    line_score = stat.lines / 25
    low_ref_bonus = 1.8 if stat.inbound_refs <= 1 else 0.5 if stat.inbound_refs == 2 else 0
    count_pressure = 2.2 if total_cold_files >= 22 else 1.0
    return round(size_score + line_score + low_ref_bonus + count_pressure, 2)


def pick_actions(stats: list[FileStat], overlap_pairs: list[tuple[str, str, int]]) -> list[str]:
    actions: list[str] = []
    if overlap_pairs:
        left, right, overlap = overlap_pairs[0]
        actions.append(f"优先检查 `{left}` 与 `{right}`，它们存在 {overlap} 条重复行，适合先做合并或去重。")

    biggest = sorted(stats, key=lambda item: item.tokens, reverse=True)[:3]
    for stat in biggest:
        if stat.inbound_refs <= 2:
            actions.append(f"检查 `{stat.rel_path}` 是否可下沉、拆薄或并入相邻文件；当前约 {stat.tokens} tokens，引用数 {stat.inbound_refs}。")

    if not actions:
        actions.append("当前冷层没有明显重复热点，优先维持现状，仅保留预算监控。")
    return actions[:3]


def build_report(mode: str) -> tuple[str, dict[str, object]]:
    stats, heading_map, overlap_pairs = collect_stats()
    total_cold_files = len(stats)
    total_cold_tokens = sum(stat.tokens for stat in stats)
    repeated_headings = [
        {"heading": heading, "files": files}
        for heading, files in heading_map.items()
        if len(files) >= 2
    ]
    repeated_headings.sort(key=lambda item: len(item["files"]), reverse=True)

    ranked = sorted(
        [
            {
                "path": stat.rel_path,
                "lines": stat.lines,
                "tokens": stat.tokens,
                "inbound_refs": stat.inbound_refs,
                "score": score_candidate(stat, total_cold_files),
            }
            for stat in stats
        ],
        key=lambda item: (item["score"], item["tokens"]),
        reverse=True,
    )

    top_candidates = ranked[:5]
    top_overlaps = [
        {"left": left, "right": right, "overlap": overlap}
        for left, right, overlap in overlap_pairs[:5]
    ]
    actions = pick_actions(stats, overlap_pairs)

    status = "稳定"
    if total_cold_files >= 24 or total_cold_tokens >= 12000:
        status = "需要收缩"
    if total_cold_files >= 28 or total_cold_tokens >= 15000:
        status = "收缩优先级高"

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": mode,
        "status": status,
        "metrics": {
            "cold_file_count": total_cold_files,
            "cold_token_estimate": total_cold_tokens,
        },
        "top_candidates": top_candidates,
        "top_overlaps": top_overlaps,
        "repeated_headings": repeated_headings[:5],
        "recommended_actions": actions,
    }

    lines = [
        f"# Cold Layer Maintenance Report ({mode})",
        "",
        "## 总体判断",
        f"- 状态：{status}",
        f"- 冷层文件数：{total_cold_files}",
        f"- 冷层总估算 tokens：{total_cold_tokens}",
        "",
        "## 最值得先看的候选文件",
    ]
    for item in top_candidates:
        lines.append(
            f"- `{item['path']}`：约 {item['tokens']} tokens，{item['lines']} 行，引用数 {item['inbound_refs']}，收缩分数 {item['score']}"
        )

    lines.extend(["", "## 重复或近重复热点"])
    if top_overlaps:
        for item in top_overlaps:
            lines.append(f"- `{item['left']}` <-> `{item['right']}`：重复行 {item['overlap']}")
    else:
        lines.append("- 暂无明显高重复文件对。")

    lines.extend(["", "## 重复标题热点"])
    if repeated_headings:
        for item in repeated_headings[:5]:
            lines.append(f"- `{item['heading']}`：{', '.join(f'`{path}`' for path in item['files'])}")
    else:
        lines.append("- 暂无明显重复标题热点。")

    lines.extend(["", "## 自动建议动作"])
    for action in actions:
        lines.append(f"- {action}")

    lines.extend(
        [
            "",
            "## 使用方式",
            "- 周维护：先读这份报告，再只处理一个最高价值的小问题。",
            "- 月深检：按这里的候选顺序优先做合并、去重和下沉，不优先新增新文件。",
        ]
    )
    return "\n".join(lines) + "\n", payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate automatic cold-layer maintenance report.")
    parser.add_argument("--mode", choices=["weekly", "monthly"], default="weekly")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report_text, payload = build_report(args.mode)
    stamp = datetime.now().strftime("%Y-%m-%d")
    markdown_path = OUTPUT_DIR / f"{stamp}-{args.mode}-cold-layer-report.md"
    json_path = OUTPUT_DIR / f"{stamp}-{args.mode}-cold-layer-report.json"
    latest_markdown = OUTPUT_DIR / f"latest-{args.mode}-cold-layer-report.md"
    latest_json = OUTPUT_DIR / f"latest-{args.mode}-cold-layer-report.json"

    markdown_path.write_text(report_text, encoding="utf-8")
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    latest_markdown.write_text(report_text, encoding="utf-8")
    latest_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(f"Generated: {markdown_path}")
    print(f"Generated: {json_path}")
    print(f"Status: {payload['status']}")
    print(f"Cold files: {payload['metrics']['cold_file_count']}")
    print(f"Cold tokens: {payload['metrics']['cold_token_estimate']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
