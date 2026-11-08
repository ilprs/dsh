# Git 练习场

一个**能跑起来**的迷你待办清单，专门用来练 Git。文档看一百遍不如亲手制造一次冲突——这里的代码小到能在脑中装下，又完整到足以演练真实工作流。

## 快速开始

只需要 Python 3.10+，**没有任何第三方依赖**。

```bash
git clone https://github.com/ilprs/dsh.git
cd dsh

python -m todolist add "练习 git commit"
python -m todolist list
python -m todolist done 1
python -m todolist list --all
python -m todolist clear
```

数据默认写在当前目录的 `tasks.json`，可用 `--file` 指定别的位置。

## 跑测试

```bash
python -m unittest discover -s tests -v
```

10 个用例覆盖增删改查、空标题校验、持久化与损坏文件处理。CI 会在 Python 3.10 和 3.12 上各跑一遍。

## 目录结构

```
.
├── todolist/
│   ├── __init__.py     # 版本号
│   ├── __main__.py     # python -m todolist 入口
│   ├── cli.py          # 命令行解析与输出
│   └── store.py        # 任务存取（JSON 持久化）
├── tests/
│   └── test_store.py   # 单元测试
├── .github/workflows/
│   └── ci.yml          # GitHub Actions
├── GIT-PRACTICE.md     # 分难度练习手册 ← 从这里开始
├── .gitattributes      # 换行符与二进制约定
├── .gitignore
├── .env.example
└── LICENSE
```

## 为什么选这个项目练 Git

它同时具备三个条件：**能跑**（有真实行为可改）、**可测**（改动能被验证，不是凭感觉）、**够小**（冲突范围可控，改一处不会牵动全身）。所以你可以放心地制造冲突、搞乱历史、再自己修回来——这正是练习要的。

## 练习手册

难度递进的 12 个任务，从「改一行提交」到「rebase 压平历史」「revert 已推送的错误」，全部在这份文件里：

**[GIT-PRACTICE.md](GIT-PRACTICE.md)**

## 约定

- 提交信息用祈使句，说清「做了什么」：`add priority field to Task`，而不是 `改了代码`。
- 仓库内统一 LF 换行，由 `.gitattributes` 处理，Windows 上的 CRLF 警告属正常。
- 不提交密钥：`.env` 已被忽略，配置模板看 `.env.example`。

## 许可证

[MIT](LICENSE) © 2026 ilprs
