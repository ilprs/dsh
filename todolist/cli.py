"""命令行入口：python -m todolist <子命令>。"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .store import TaskStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todolist",
        description="极简待办清单（练习 Git 用的示例项目）",
    )
    parser.add_argument(
        "--file",
        default="tasks.json",
        help="任务数据文件路径，默认 tasks.json",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="添加一条任务")
    p_add.add_argument("title", help="任务标题")

    p_list = sub.add_parser("list", help="列出任务")
    p_list.add_argument("--all", action="store_true", help="包含已完成的任务")

    p_done = sub.add_parser("done", help="标记任务为已完成")
    p_done.add_argument("id", type=int, help="任务编号")

    p_remove = sub.add_parser("remove", help="删除一条任务")
    p_remove.add_argument("id", type=int, help="任务编号")

    sub.add_parser("clear", help="清除所有已完成任务")

    sub.add_parser("stats", help="显示任务统计")

    return parser


def _ensure_utf8_stdout() -> None:
    """Windows 控制台默认 GBK，输出中文会乱码；这里统一切到 UTF-8。"""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass


def main(argv: list[str] | None = None) -> int:
    _ensure_utf8_stdout()
    args = build_parser().parse_args(argv)
    store = TaskStore(Path(args.file))

    try:
        if args.command == "add":
            task = store.add(args.title)
            print(f"已添加 #{task.id}: {task.title}")

        elif args.command == "list":
            tasks = store.list(include_done=args.all)
            if not tasks:
                print("没有任务。用 add 添加一条吧。")
                return 0
            for task in tasks:
                mark = "x" if task.done else " "
                print(f"[{mark}] #{task.id}  {task.title}")

        elif args.command == "done":
            task = store.done(args.id)
            print(f"已完成 #{task.id}: {task.title}")

        elif args.command == "remove":
            task = store.remove(args.id)
            print(f"已删除 #{task.id}: {task.title}")

        elif args.command == "clear":
            count = store.clear_done()
            print(f"清除了 {count} 条已完成任务")

        elif args.command == "stats":
            s = store.stats()
            print(f"总计 {s['total']} 条，已完成 {s['done']} 条，完成率 {s['rate']}%")

    except (KeyError, ValueError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
