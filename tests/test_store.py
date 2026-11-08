"""单元测试：只用标准库 unittest，避免练习仓库引入安装步骤。"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from todolist.store import TaskStore


class TaskStoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "tasks.json"
        self.store = TaskStore(self.path)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_add_assigns_increasing_ids(self) -> None:
        first = self.store.add("买牛奶")
        second = self.store.add("写周报")
        self.assertEqual(first.id, 1)
        self.assertEqual(second.id, 2)

    def test_add_rejects_blank_title(self) -> None:
        with self.assertRaises(ValueError):
            self.store.add("   ")

    def test_add_strips_whitespace(self) -> None:
        task = self.store.add("  交房租  ")
        self.assertEqual(task.title, "交房租")

    def test_persists_across_instances(self) -> None:
        self.store.add("健身")
        reopened = TaskStore(self.path)
        self.assertEqual([t.title for t in reopened.list()], ["健身"])

    def test_done_marks_task(self) -> None:
        task = self.store.add("读书")
        self.store.done(task.id)
        self.assertTrue(TaskStore(self.path).get(task.id).done)

    def test_list_can_hide_done(self) -> None:
        done_task = self.store.add("已完成")
        self.store.add("未完成")
        self.store.done(done_task.id)

        self.assertEqual(len(self.store.list()), 2)
        self.assertEqual(len(self.store.list(include_done=False)), 1)

    def test_remove_deletes_task(self) -> None:
        task = self.store.add("临时任务")
        self.store.remove(task.id)
        self.assertEqual(self.store.list(), [])

    def test_missing_id_raises(self) -> None:
        with self.assertRaises(KeyError):
            self.store.get(999)

    def test_clear_done_returns_count(self) -> None:
        a = self.store.add("a")
        self.store.add("b")
        self.store.done(a.id)
        self.assertEqual(self.store.clear_done(), 1)
        self.assertEqual([t.title for t in self.store.list()], ["b"])

    def test_corrupt_file_surfaces_error(self) -> None:
        self.path.write_text("{not json", encoding="utf-8")
        with self.assertRaises(Exception):
            TaskStore(self.path)


if __name__ == "__main__":
    unittest.main()
