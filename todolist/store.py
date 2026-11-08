"""任务的存取逻辑：与命令行界面解耦，便于单元测试。"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_PATH = Path(os.environ.get("TODOLIST_FILE", "tasks.json"))


@dataclass
class Task:
    """一条待办事项。"""

    id: int
    title: str
    done: bool = False
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )


class TaskStore:
    """把任务保存在一个 JSON 文件里。

    刻意保持简单：没有数据库、没有并发控制。练习仓库的重点是 Git 操作，
    存储层只需要「能读能写、可断言」。
    """

    def __init__(self, path: Path | str = DEFAULT_PATH) -> None:
        self.path = Path(path)
        self._tasks: list[Task] = []
        self.load()

    # ---------- 持久化 ----------

    def load(self) -> None:
        if not self.path.exists():
            self._tasks = []
            return

        raw = json.loads(self.path.read_text(encoding="utf-8"))
        self._tasks = [Task(**item) for item in raw]

    def save(self) -> None:
        payload = [asdict(task) for task in self._tasks]
        self.path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    # ---------- 业务操作 ----------

    def _next_id(self) -> int:
        return max((task.id for task in self._tasks), default=0) + 1

    def add(self, title: str) -> Task:
        title = title.strip()
        if not title:
            raise ValueError("任务标题不能为空")

        task = Task(id=self._next_id(), title=title)
        self._tasks.append(task)
        self.save()
        return task

    def list(self, include_done: bool = True) -> list[Task]:
        if include_done:
            return list(self._tasks)
        return [task for task in self._tasks if not task.done]

    def done(self, task_id: int) -> Task:
        task = self.get(task_id)
        task.done = True
        self.save()
        return task

    def remove(self, task_id: int) -> Task:
        task = self.get(task_id)
        self._tasks.remove(task)
        self.save()
        return task

    def get(self, task_id: int) -> Task:
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"找不到 id 为 {task_id} 的任务")

    def clear_done(self) -> int:
        """删除所有已完成任务，返回删除数量。"""
        before = len(self._tasks)
        self._tasks = [task for task in self._tasks if not task.done]
        self.save()
        return before - len(self._tasks)
