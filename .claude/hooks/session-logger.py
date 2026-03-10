#!/usr/bin/env python3
"""
Claude Code Stop Hook — 会话摘要记录器
每次 CC 完成响应，自动追加一条摘要到 .claude/session-log.md
参考 ECC 的 Stop-phase session summaries 模式
"""

import json
import sys
from datetime import datetime
from pathlib import Path


def count_tool_calls(transcript_path: str) -> tuple[int, list[str]]:
    """统计最后一轮 assistant 回复中的工具调用次数和工具名列表"""
    try:
        lines = Path(transcript_path).read_text(encoding="utf-8-sig", errors="replace").strip().splitlines()
        tools_used = []
        in_last_assistant = False

        for line in reversed(lines):
            try:
                entry = json.loads(line)
            except Exception:
                continue

            msg = entry.get("message", {})
            role = msg.get("role", "") or entry.get("role", "")

            if role == "assistant":
                in_last_assistant = True
                content = msg.get("content", []) or entry.get("content", [])
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "tool_use":
                            tool_name = block.get("name", "unknown")
                            if tool_name not in tools_used:
                                tools_used.append(tool_name)
            elif role == "user" and in_last_assistant:
                break

        return len(tools_used), tools_used

    except Exception:
        return 0, []


def main():
    try:
        hook_input = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except Exception:
        sys.exit(0)

    # 防止 stop_hook_active 死循环
    if hook_input.get("stop_hook_active", False):
        sys.exit(0)

    transcript_path = hook_input.get("transcript_path", "")
    cwd = hook_input.get("cwd", "")
    last_message = hook_input.get("last_assistant_message", "")

    if not cwd:
        sys.exit(0)

    # 统计工具调用
    tool_count, tools_used = count_tool_calls(transcript_path)

    # 构建摘要行
    now = datetime.now().strftime("%H:%M:%S")

    # 截取 last_assistant_message 前80字作为摘要
    summary = last_message.strip().replace("\n", " ")[:80]
    if len(last_message.strip()) > 80:
        summary += "..."

    if tool_count == 0:
        log_line = f"- `{now}` 💬 {summary}\n"
    else:
        tools_str = " / ".join(tools_used)
        log_line = f"- `{now}` 🔧 [{tools_str}] {summary}\n"

    # 用字符串操作提取项目名，避免 Windows 中文路径下 Path() 产生 surrogate 字符
    project_name = cwd.replace("\\", "/").rstrip("/").split("/")[-1]

    log_path = Path(cwd) / ".claude" / "session-log.md"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")

    try:
        if log_path.exists():
            content = log_path.read_text(encoding="utf-8-sig", errors="replace")
            if f"## {today}" not in content:
                new_content = content + f"\n## {today}\n" + log_line
            else:
                new_content = content + log_line
        else:
            new_content = f"# CC Session Log — {project_name}\n\n## {today}\n" + log_line

        log_path.write_text(new_content, encoding="utf-8-sig", errors="replace")
    except Exception as e:
        print(f"session-logger error: {e}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()