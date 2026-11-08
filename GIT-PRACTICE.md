# Git 练习手册

12 个任务，按难度递进。**建议按顺序做**，因为后面的任务会用到前面的习惯。

每个任务都设计了「可验证的结果」——做完能自己确认对错，不靠猜。

> 约定：所有命令都在仓库根目录执行。每完成一个任务，`git push` 之前先看一眼 `git status`。

---

## 第 0 级：热身（先建立肌肉记忆）

### 1. 看清你手上有什么

```bash
git status                  # 工作区与暂存区状态
git log --oneline --graph   # 提交历史，图形化
git diff                    # 未暂存的改动
git diff --staged           # 已暂存、待提交的改动
```

**练习**：改一行 `README.md`，分别执行 `git diff` 和 `git diff --staged`，观察差异。然后再 `git add README.md`，重跑这两条命令。

**要点**：`git diff` 只显示「还没 add 的」；加了 `--staged` 才是「将要提交的」。

---

### 2. 提交一次真实的改动

**练习**：把 `todolist` 的版本号从 `0.1.0` 改成 `0.1.1`，然后：

```bash
git add todolist/__init__.py
git commit -m "bump version to 0.1.1"
```

**验证**：`git log -1 --stat` 应该只看到这一个文件被改动。

**要点**：`git add` 选的是「这次提交包含什么」，不是「把所有东西都提交」。

---

### 3. 撤回一次还没提交的改动

**练习**：随便改坏 `README.md`（比如删掉标题），然后：

```bash
git restore README.md
git status      # 应该显示 clean
```

**要点**：`git restore` 会**不可逆地丢弃**工作区改动。用之前确认你真的不要了。

---

## 第 1 级：分支与合并

### 4. 新建分支，改完合回主干

给你的 `Task` 加一个 `priority` 字段（比如 `1=高, 2=中, 3=低`，默认 2）。

```bash
git switch -c feature/priority     # 新建并切换
# 改 todolist/store.py、cli.py、tests/test_store.py
python -m unittest discover -s tests -v
git add -A
git commit -m "add priority field to Task"
git switch main
git merge feature/priority
git push
git branch -d feature/priority
```

**验证**：`git log --oneline --graph` 能看到分支合并的痕迹。

**要点**：分支成本极低，失败就丢。别在 `main` 上直接写实验性代码。

---

### 5. 制造一次冲突，然后亲手解决

这是最重要的一个练习。两个人同时改同一个文件的同一区域时，冲突必然发生。

```bash
git switch -c conflict/a
# 把 store.py 里 add() 的空标题提示改成：raise ValueError("标题不可以是空白")
git commit -am "sharpen blank-title error message"

git switch main
# 把同一行改成：raise ValueError("任务标题不能为空，请重新输入")
git commit -am "clarify blank-title error message"

git merge conflict/a          # 冲突！
```

冲突时，文件里会出现：

```
<<<<<<< HEAD
        raise ValueError("任务标题不能为空，请重新输入")
=======
        raise ValueError("标题不可以是空白")
>>>>>>> conflict/a
```

**你要做的**：手动编辑，只保留**你真正想要的最终版本**（删掉 `<<<<<<<`、`=======`、`>>>>>>>` 这三行标记），然后：

```bash
git add todolist/store.py
git commit                    # 冲突解决完的提交，Git 会预填信息
python -m unittest discover -s tests -v
```

**验证**：测试必须全绿。如果红灯，说明你删坏了代码。

**要点**：冲突不是错误，是 Git 在说「这两处我判断不了，你决定」。解决冲突 = 编辑文件 + `git add` + `git commit`。

---

### 6. 用 `git diff` 对比两个分支

```bash
git diff main..feature/priority
git diff main..feature/priority -- todolist/store.py   # 只看某个文件
```

**练习**：开一个新分支，给 `list` 子命令加一个 `--sort` 参数，然后用上面的命令 review 自己的改动，**在合并前**发现问题。

---

## 第 2 级：历史整理

### 7. 修改最近一次提交

**练习**：故意提交一条信息写错的 commit：

```bash
echo "# 临时" >> README.md
git commit -am "temp"          # 信息很烂
git commit --amend -m "docs: add temporary note section"
```

**要点**：`--amend` 只对**未推送**的提交安全。已经推送的提交不要 amend，否则别人拉取时会分裂。

---

### 8. 用 `rebase` 把零碎提交压平

假设你在分支上提交了 3 次「改一点、再改一点、又改一点」，想合成一个有意义的提交：

```bash
git switch -c feature/cleanup
# 做三次小改动，每次 commit
git log --oneline -3

git rebase -i HEAD~3
# 编辑器里把后两行的 pick 改成 squash（或 s），保存
# 然后编辑合并后的提交信息
```

**验证**：`git log --oneline` 只剩 1 条。

**要点**：`rebase` 改写历史，**只能对没推送的分支用**。已经共享的提交绝对不要 rebase。

---

### 9. 用 `revert` 撤回一个已推送的提交

这是「已经公开的错误」的正确处理方式。

```bash
# 先找一个已推送、想撤回的提交
git log --oneline -5

git revert <提交号>            # 会生成一个反向提交
git push
```

**关键区别**：`revert` 是**新增**一个提交来抵消，历史完整保留；`reset --hard` 是**抹除**历史，配合 `push --force` 会破坏别人的仓库。

**验证**：`git log` 里能看到两条记录——原来的和反向的。

---

### 10. 找回「丢失」的提交

**练习**：制造一次「事故」——在分支上提交了内容，然后 `git reset --hard HEAD~1`，看起来全没了。

```bash
git reflog                    # 会列出 HEAD 走过的每一步
# 找到 reset 之前的那个提交号
git switch -c rescue <提交号>
```

**验证**：提交内容回来了。

**要点**：只要 commit 过，`reflog` 就能救回来（默认保留 90 天）。Git 很少真的「丢」东西。

---

## 第 3 级：协作流程

### 11. 走一遍 Pull Request 流程

```bash
git switch -c feature/pr-demo
# 给 CLI 加一个 `stats` 子命令：输出总数 / 已完成数 / 完成率
git add -A
git commit -m "add stats subcommand"
git push -u origin feature/pr-demo
```

然后到 GitHub 页面上：
1. 点 **Compare & pull request**
2. 写清「做了什么、为什么、怎么验证」
3. 等 CI 变绿（这是 `ci.yml` 的作用）
4. 合并，删除远程分支

**验证**：合并后 `git switch main && git pull`，本地能看到合并结果。

---

### 12. 处理「远程有新提交」的情况

**练习**：在 GitHub 网页上直接改一行 `README.md` 并提交，然后本地也改同一个地方并提交，再 `git push`：

```bash
# 预期被拒绝
git push
# 先拉取并变基，把本地提交放到远程提交之后
git pull --rebase
# 若有冲突，按任务 5 的方法解决
git push
```

**要点**：`git pull` 默认是 merge（会产生一个合并提交）；`--rebase` 让历史保持线性。个人分支建议用 `--rebase`。

---

## 附：出问题时先跑这三条

```bash
git status                 # 我在哪个分支、有没有未提交的东西
git log --oneline -10      # 最近发生了什么
git reflog -15             # 我做过哪些「危险」操作
```

`reflog` 是你的安全网。绝大多数「我搞砸了」的情况，都能从这里找到回去的路。

## 附：常用参数速查

| 目的 | 命令 |
| --- | --- |
| 看某次提交改了什么 | `git show <提交号>` |
| 只暂存文件的一部分 | `git add -p` |
| 暂存当前改动去处理急事 | `git stash` / `git stash pop` |
| 看某一行是谁写的 | `git blame <文件>` |
| 查一个词何时引入 | `git log -S "关键词" --oneline` |
| 撤销某个文件的本地改动 | `git restore <文件>` |
| 取消暂存（保留改动） | `git restore --staged <文件>` |
