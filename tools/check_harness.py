from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math
import re
import sys


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class CheckResult:
    level: str
    name: str
    detail: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def line_count(path: Path) -> int:
    return len(read_text(path).splitlines())


def add(results: list[CheckResult], level: str, name: str, detail: str) -> None:
    results.append(CheckResult(level=level, name=name, detail=detail))


def check_exists(results: list[CheckResult], rel_path: str) -> None:
    path = ROOT / rel_path
    if path.exists():
        add(results, "PASS", f"存在性: {rel_path}", "文件或目录存在。")
    else:
        add(results, "FAIL", f"存在性: {rel_path}", "缺失，当前 harness 不完整。")


def check_contains(
    results: list[CheckResult],
    rel_path: str,
    needles: list[str],
    label: str,
) -> None:
    path = ROOT / rel_path
    if not path.exists():
        add(results, "FAIL", label, f"{rel_path} 不存在，无法检查引用。")
        return

    content = read_text(path)
    missing = [needle for needle in needles if needle not in content]
    if missing:
        add(results, "FAIL", label, f"缺少关键引用: {', '.join(missing)}")
    else:
        add(results, "PASS", label, "关键引用完整。")


def check_not_contains(
    results: list[CheckResult],
    rel_paths: list[str],
    banned: list[str],
    label: str,
) -> None:
    hits: list[str] = []
    for rel_path in rel_paths:
        path = ROOT / rel_path
        if not path.exists():
            continue
        content = read_text(path)
        matched = [phrase for phrase in banned if phrase in content]
        if matched:
            hits.append(f"{rel_path}: {', '.join(matched)}")

    if hits:
        add(results, "FAIL", label, f"发现旧命名或旧实验残留: {'; '.join(hits)}")
    else:
        add(results, "PASS", label, "未发现旧命名或旧实验残留。")


def check_line_budget(results: list[CheckResult], rel_path: str, soft_limit: int) -> None:
    path = ROOT / rel_path
    if not path.exists():
        add(results, "FAIL", f"体量: {rel_path}", "文件不存在，无法判断是否膨胀。")
        return

    count = line_count(path)
    if count <= soft_limit:
        add(results, "PASS", f"体量: {rel_path}", f"{count} 行，仍在轻量范围内。")
    elif count <= soft_limit + 30:
        add(results, "WARN", f"体量: {rel_path}", f"{count} 行，开始接近膨胀边界。")
    else:
        add(results, "FAIL", f"体量: {rel_path}", f"{count} 行，建议收缩顶层内容。")


def check_regression_case(results: list[CheckResult], rel_path: str) -> None:
    required_sections = [
        "## 用户请求",
        "## 期望路由",
        "## 最低合格输出",
        "## 常见跑偏",
    ]
    check_contains(results, rel_path, required_sections, f"回归样例: {rel_path}")


def check_phrase_overlap(
    results: list[CheckResult],
    rel_paths: list[str],
    phrase: str,
    label: str,
    warn_threshold: int,
) -> None:
    hit_paths = []
    for rel_path in rel_paths:
        path = ROOT / rel_path
        if path.exists() and phrase in read_text(path):
            hit_paths.append(rel_path)

    if len(hit_paths) > warn_threshold:
        add(
            results,
            "WARN",
            label,
            f"短语“{phrase}”同时出现在 {len(hit_paths)} 个文件中: {', '.join(hit_paths)}",
        )
    else:
        add(results, "PASS", label, "未发现明显重复职责扩散。")


def iter_memory_md_files() -> list[Path]:
    return sorted((ROOT / ".project-memory").rglob("*.md"))


def approx_token_count(text: str) -> int:
    """Conservative mixed-language token estimate without external deps."""
    ascii_chars = len(re.findall(r"[\x00-\x7F]", text))
    cjk_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
    other_chars = max(0, len(text) - ascii_chars - cjk_chars)
    estimate = ascii_chars / 3.2 + cjk_chars * 1.15 + other_chars / 2.2
    return math.ceil(estimate)


def total_tokens(paths: list[Path]) -> int:
    return sum(approx_token_count(read_text(path)) for path in paths if path.exists())


def format_paths(paths: list[Path]) -> str:
    return ", ".join(str(path.relative_to(ROOT)).replace("\\", "/") for path in paths)


def check_expansion_budget(results: list[CheckResult]) -> None:
    memory_files = iter_memory_md_files()
    if len(memory_files) <= 26:
        add(results, "PASS", "扩张预算", f".project-memory 当前共有 {len(memory_files)} 个 md 文件，仍在预算内。")
    elif len(memory_files) <= 30:
        add(results, "WARN", "扩张预算", f".project-memory 当前共有 {len(memory_files)} 个 md 文件，接近扩张边界。")
    else:
        add(results, "FAIL", "扩张预算", f".project-memory 当前共有 {len(memory_files)} 个 md 文件，建议暂停新增并优先收缩。")


def check_central_file_budgets(results: list[CheckResult]) -> None:
    budgets = {
        ".project-memory/README.md": 85,
        ".project-memory/tool-delivery-routing.md": 125,
        ".project-memory/automation-entrypoints.md": 75,
        ".project-memory/plugin-mcp-governance.md": 80,
        ".project-memory/text-selector-questioning-protocol.md": 70,
    }
    for rel_path, limit in budgets.items():
        check_line_budget(results, rel_path, limit)


def check_context_budget(
    results: list[CheckResult],
    rel_paths: list[str],
    label: str,
    warn_limit: int,
    fail_limit: int,
) -> None:
    paths = [ROOT / rel_path for rel_path in rel_paths]
    missing = [rel_path for rel_path, path in zip(rel_paths, paths) if not path.exists()]
    if missing:
        add(results, "FAIL", label, f"缺少文件，无法评估上下文预算: {', '.join(missing)}")
        return

    estimate = total_tokens(paths)
    detail = f"约 {estimate} tokens，样本: {format_paths(paths)}"
    if estimate <= warn_limit:
        add(results, "PASS", label, detail)
    elif estimate <= fail_limit:
        add(results, "WARN", label, f"{detail}；开始接近预算上限。")
    else:
        add(results, "FAIL", label, f"{detail}；已超过预算上限。")


def check_full_flatten_budget(results: list[CheckResult], warn_limit: int, fail_limit: int) -> None:
    paths = [ROOT / "AGENTS.md", ROOT / "PROJECT-WORKFLOW.md", *iter_memory_md_files()]
    missing = [path for path in paths if not path.exists()]
    if missing:
        missing_text = ", ".join(str(path.relative_to(ROOT)).replace("\\", "/") for path in missing)
        add(results, "FAIL", "全量平铺预算", f"缺少文件，无法评估全量平铺预算: {missing_text}")
        return

    estimate = total_tokens(paths)
    detail = f"约 {estimate} tokens，覆盖 AGENTS + PROJECT-WORKFLOW + .project-memory 全部 md"
    if estimate <= warn_limit:
        add(results, "PASS", "全量平铺预算", detail)
    elif estimate <= fail_limit:
        add(results, "WARN", "全量平铺预算", f"{detail}；如果误全量加载，会开始明显变重。")
    else:
        add(results, "FAIL", "全量平铺预算", f"{detail}；误全量加载风险过高，应继续收缩。")


def summarize(results: list[CheckResult]) -> tuple[int, int]:
    fail_count = sum(1 for result in results if result.level == "FAIL")
    warn_count = sum(1 for result in results if result.level == "WARN")
    return fail_count, warn_count


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    results: list[CheckResult] = []

    required_paths = [
        "AGENTS.md",
        "PROJECT-WORKFLOW.md",
        ".project-memory",
        ".project-memory/README.md",
        ".project-memory/automation-entrypoints.md",
        ".project-memory/plugin-mcp-governance.md",
        ".project-memory/capability-registry.md",
        ".project-memory/capability-fallback-matrix.md",
        ".project-memory/weekly-maintenance-report-template.md",
        ".project-memory/rule-deletion-guidelines.md",
        ".project-memory/memory-write-thresholds.md",
        ".project-memory/memory-retention-and-expiry.md",
        ".project-memory/memory-audit-playbook.md",
        ".project-memory/document-condense-template.md",
        ".project-memory/expansion-budget-policy.md",
        ".project-memory/text-selector-questioning-protocol.md",
        ".project-memory/tool-delivery-routing.md",
        ".project-memory/validation-pre-delivery.md",
        ".project-memory/validation-harness-health.md",
        ".project-memory/knowledge-cache/index.md",
        "harness-regression/README.md",
        "harness-regression/cases",
        "harness-regression/drills/README.md",
        "harness-regression/drills/memory/README.md",
    ]
    for rel_path in required_paths:
        check_exists(results, rel_path)

    check_contains(
        results,
        "AGENTS.md",
        [
            ".project-memory/",
            "automation-entrypoints.md",
            "plugin-mcp-governance.md",
            "capability-registry.md",
            "capability-fallback-matrix.md",
            "validation-pre-delivery.md",
            "tool-delivery-routing.md",
            "text-selector-questioning-protocol.md",
        ],
        "顶层协议引用",
    )
    check_contains(
        results,
        "PROJECT-WORKFLOW.md",
        [
            "automation-entrypoints.md",
            "knowledge-cache\\index.md",
            "tool-delivery-routing.md",
            "plugin-mcp-governance.md",
            "capability-fallback-matrix.md",
            "text-selector-questioning-protocol.md",
        ],
        "工作流引用",
    )
    check_contains(
        results,
        ".project-memory/README.md",
        [
            "user-preferences.md",
            "project-state.md",
            "decision-log.md",
            "knowledge-cache/",
            "plugin-mcp-governance.md",
            "capability-registry.md",
            "capability-fallback-matrix.md",
            "weekly-maintenance-report-template.md",
            "rule-deletion-guidelines.md",
            "memory-write-thresholds.md",
            "memory-retention-and-expiry.md",
            "memory-audit-playbook.md",
            "document-condense-template.md",
            "expansion-budget-policy.md",
            "text-selector-questioning-protocol.md",
        ],
        "记忆层分工",
    )
    check_contains(
        results,
        ".project-memory/expansion-budget-policy.md",
        [
            "新增文件预算",
            "中枢文件预算",
            "新增前强制检查",
            "月度深检默认动作",
        ],
        "扩张预算策略",
    )
    check_contains(
        results,
        ".project-memory/weekly-maintenance-report-template.md",
        [
            "本周总体判断",
            "本轮检查范围",
            "已处理问题",
            "剩余风险",
            "下一轮最该看的文件",
        ],
        "周维护报告模板",
    )
    check_contains(
        results,
        ".project-memory/plugin-mcp-governance.md",
        [
            "什么时候必须优先走专用能力",
            "什么时候先不要上重工具",
            "回退原则",
            "capability-fallback-matrix.md",
        ],
        "插件治理边界",
    )
    check_contains(
        results,
        ".project-memory/tool-delivery-routing.md",
        [
            "论文 / 作业 / 长文写作",
            "汇报 / slides / 演讲型呈现",
            "文本点选追问",
        ],
        "工具路由结构",
    )
    check_contains(
        results,
        ".project-memory/capability-registry.md",
        [
            "高优先级能力",
            "正式文件交付",
            "最新信息与来源核对",
            "浏览器验证",
        ],
        "能力清单结构",
    )
    check_contains(
        results,
        ".project-memory/capability-fallback-matrix.md",
        [
            "文档交付",
            "表格交付",
            "Slides / 演讲交付",
            "最新事实与来源核对",
            "浏览器验证",
        ],
        "能力断链矩阵",
    )
    check_contains(
        results,
        ".project-memory/validation-harness-health.md",
        [
            "顶层是否变胖",
            "路由是否清晰",
            "memory 是否还干净",
            "spec 是否真的有用",
        ],
        "健康检查维度",
    )
    check_contains(
        results,
        ".project-memory/rule-deletion-guidelines.md",
        [
            "重复表达",
            "很少真正被读取",
            "只服务一次性纠偏",
            "造成选择摇摆",
        ],
        "删除准则结构",
    )
    check_contains(
        results,
        ".project-memory/memory-write-thresholds.md",
        [
            "默认写入门槛",
            "默认不写入",
            "四类信息的专门门槛",
            "写入前最后检查",
        ],
        "memory 写入阈值",
    )
    check_contains(
        results,
        ".project-memory/memory-retention-and-expiry.md",
        [
            "默认状态",
            "触发复查的信号",
            "默认处理顺序",
        ],
        "memory 保留与过期规则",
    )
    check_contains(
        results,
        ".project-memory/memory-audit-playbook.md",
        [
            "什么时候启动",
            "审计顺序",
            "审计问题",
            "默认修正顺序",
        ],
        "memory 审计入口",
    )
    check_contains(
        results,
        ".project-memory/document-condense-template.md",
        [
            "一句话主旨",
            "一页解构",
            "精炼版摘要",
            "提纲版",
        ],
        "文档精炼模板",
    )
    check_contains(
        results,
        ".project-memory/text-selector-questioning-protocol.md",
        [
            "默认原则",
            "选项格式",
            "不推荐的问法",
            "不触发场景",
            "默认收口",
        ],
        "文本选择器追问协议",
    )
    check_contains(
        results,
        "harness-regression/drills/README.md",
        [
            "Slides 回退",
            "最新事实核对回退",
            "表格交付回退",
            "正式文档交付回退",
            "PDF 审阅回退",
            "文本选择器追问回退",
            "文本选择器实战演练",
        ],
        "演练索引结构",
    )
    check_contains(
        results,
        "harness-regression/drills/memory/README.md",
        [
            "写入阈值",
            "边界分层",
            "过期复查",
        ],
        "memory 演练索引",
    )

    check_expansion_budget(results)
    check_central_file_budgets(results)
    check_context_budget(
        results,
        [
            "AGENTS.md",
            "PROJECT-WORKFLOW.md",
            ".project-memory/README.md",
            ".project-memory/tool-delivery-routing.md",
            ".project-memory/plugin-mcp-governance.md",
            ".project-memory/capability-fallback-matrix.md",
            ".project-memory/text-selector-questioning-protocol.md",
        ],
        "误广加载预算",
        warn_limit=12000,
        fail_limit=14000,
    )
    check_full_flatten_budget(results, warn_limit=22000, fail_limit=32000)
    check_phrase_overlap(
        results,
        [
            ".project-memory/README.md",
            ".project-memory/tool-delivery-routing.md",
            ".project-memory/plugin-mcp-governance.md",
            ".project-memory/automation-entrypoints.md",
        ],
        "主交付物",
        "重复职责扫描: 主交付物",
        2,
    )
    check_phrase_overlap(
        results,
        [
            ".project-memory/README.md",
            ".project-memory/rule-deletion-guidelines.md",
            ".project-memory/expansion-budget-policy.md",
            ".project-memory/validation-harness-health.md",
        ],
        "删除",
        "重复职责扫描: 删除/收缩",
        2,
    )
    check_not_contains(
        results,
        [
            "AGENTS.md",
            "PROJECT-WORKFLOW.md",
            ".project-memory/README.md",
            "harness-regression/cases/05-click-option-questioning.md",
            "harness-regression/drills/2026-07-03-click-option-questioning-drill.md",
            "harness-regression/drills/2026-07-03-click-option-live-rehearsal.md",
        ],
        ["click-option-questioning-protocol.md", "Click Option Questioning Protocol"],
        "旧命名残留检查",
    )

    check_line_budget(results, "AGENTS.md", 160)
    check_line_budget(results, "PROJECT-WORKFLOW.md", 130)

    regression_cases = [
        "harness-regression/cases/01-review-notes.md",
        "harness-regression/cases/02-essay-outline.md",
        "harness-regression/cases/03-presentation-delivery.md",
        "harness-regression/cases/04-document-condense.md",
        "harness-regression/cases/05-click-option-questioning.md",
    ]
    for rel_path in regression_cases:
        check_regression_case(results, rel_path)

    fail_count, warn_count = summarize(results)

    print("Harness Health Check")
    print(f"Root: {ROOT}")
    print()
    for result in results:
        print(f"[{result.level}] {result.name}")
        print(f"  {result.detail}")

    print()
    if fail_count == 0 and warn_count == 0:
        print("结论: PASS")
        print("当前 harness 结构完整，关键链接、预算与命名状态正常。")
        return 0

    if fail_count == 0:
        print("结论: PASS WITH WARNINGS")
        print(f"存在 {warn_count} 个警告，建议继续收缩或补齐。")
        return 0

    print("结论: FAIL")
    print(f"存在 {fail_count} 个失败项，建议先修复再继续扩展。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
