# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Hello-Agents 是 Datawhale 社区的开源教程项目，主题为"从零开始构建智能体"。项目包含系统性教程文档（`docs/`）和配套示例代码（`code/`），涵盖从 LLM 基础到多智能体系统的完整知识体系。

## 目录结构

```
├── docs/                    # 教程 Markdown 文档（16 章）
├── code/                    # 各章节配套代码，按 chapter{N} 组织
│   ├── chapter1-3/          # 基础概念与算法实现
│   ├── chapter4/            # 经典范式（ReAct, Plan-and-Solve, Reflection）
│   ├── chapter5/            # 低代码平台配置
│   ├── chapter6/            # 主流框架实践（AgentScope, LangGraph, AutoGen）
│   ├── chapter7/            # 自研 HelloAgents 框架
│   ├── chapter8-9/          # 记忆系统与上下文工程
│   ├── chapter10/           # MCP/A2A/ANP 通信协议
│   ├── chapter11/           # LLM 训练（SFT → GRPO）
│   ├── chapter12/           # 评估框架（BFCL, GAIA, 数据生成）
│   ├── chapter13/           # 综合案例：旅行助手（FastAPI 后端）
│   ├── chapter14/           # 综合案例：深度研究智能体（FastAPI 后端）
│   └── chapter15/           # 综合案例：赛博小镇
├── Co-creation-projects/    # 社区贡献的独立 Agent 项目
├── Additional-Chapter/      # 附加安装指南
└── Extra-Chapter/           # 社区精选补充内容
```

## 开发环境

本项目使用 **uv** 作为 Python 包管理器。

```bash
# 安装依赖
uv sync

# 运行根目录入口（目前仅占位）
uv run main.py

# 运行特定章节代码
uv run code/chapter4/ReAct.py
uv run code/chapter7/test_react_agent.py
```

### 环境变量

章节代码依赖 `.env` 文件配置 LLM API 连接信息，关键字段：
- `LLM_MODEL_ID` — 模型标识
- `LLM_API_KEY` — API 密钥
- `LLM_BASE_URL` — 服务端点
- `LLM_TIMEOUT` — 超时秒数（默认 60）

在项目根目录创建 `.env` 文件即可。

## 核心架构模式

### LLM 客户端抽象（chapter4/llm_client.py）

`HelloAgentsLLM` 类封装了 OpenAI 兼容的 LLM 调用，是各章节 Agent 实现的统一入口。所有 Agent 范式都围绕这个客户端构建。

### Agent 范式模式（chapter4, chapter7）

- **ReAct Agent**: Thought → Action → Observation 循环，通过正则解析 LLM 输出
- **Plan-and-Solve**: 先生成计划再执行的两阶段模式
- **Reflection**: 生成 → 反思 → 改进的迭代模式

### 综合案例后端架构（chapter13, chapter14, chapter15）

章节 13/14 采用 FastAPI + uvicorn 的后端架构，典型分层：
```
backend/
├── run.py          # uvicorn 启动入口
├── src|app/
│   ├── api/        # 路由定义
│   ├── agents/     # Agent 核心逻辑
│   ├── services/   # 外部服务封装（搜索、地图、LLM）
│   ├── models/     # 数据模型/Pydantic schemas
│   └── config.py   # 配置管理
```

启动方式：`uvicorn run:app --reload` 或直接 `python run.py`

## 常用命令

```bash
# 运行单个章节代码
uv run code/chapter4/ReAct.py

# 格式检查（如有）
ruff check .

# 格式化
ruff format .
```

## 贡献注意事项

- 文档修改请同步更新 `docs/` 下对应章节
- 代码修改请确保能通过 `uv run` 执行
- 新增章节代码放在 `code/chapter{N}/` 目录下
