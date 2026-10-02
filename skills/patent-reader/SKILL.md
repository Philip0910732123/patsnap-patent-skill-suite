---
name: patent-reader
description: "专利通俗解读（智慧芽 MCP 增强）：公开号/PDF 成通俗笔记、图谱与 Obsidian 入库；MCP 可用时自动富化同族/引证/法律状态。"
user-invocable: false
---

# 专利通俗解读

## 用途

把公开号 / PDF / 全文读成通俗笔记、图谱，并可写入 Obsidian。独权拆成稳定特征行（`claim_features.json`），说明书段落可机读（`description_paragraphs.json`），给对照表当输入。

## 何时用

用户说读专利、给出公开号或 PDF 且目标是「读懂」，或 `/patent-read`、`/读专利`。对照表派工缺 `claim_features.json` 或 `description_paragraphs.json` 时由对照表点名进入。对照表只要这两份文件，不写笔记、不入库。

## 输入

公开号、专利 PDF、或粘贴的权利要求/说明书。对照表派工时默认把从属权也拆进 `claim_features.json`，并保留 `description_paragraphs.json`。

## 步骤

1. **`Read`** `prompts/patent_plain_reader.md`。对照表派工只做到该文件「对照表派工」段，不写笔记
2. 用户要读懂、且为实用新型或外观：**`Read`** `prompts/type_hooks.md` + `prompts/fill_*`
3. 笔记 / 自检：`obsidian_ofm_companion.md`、`patent_reader_self_check.md`

<<<<<<< HEAD
## 智慧芽 MCP 富化（可选增强）

MCP 可用时，在第 1 步取证后、写笔记前，用以下 MCP 工具富化专利维度：

| 维度 | MCP 工具 | 用途 |
|------|----------|------|
| 著录详情 | `core-patents.bibliography` | 补全申请人、发明人、IPC、申请日等 |
| 法律状态 | `core-patents.get_patent_legal_status` | 当前有效/失效/审查中状态 |
| 同族 | `core-patents.family` | 全球同族布局，地域覆盖范围 |
| 前向引证 | `core-patents.forward_citation` | 被引次数和引用方，衡量影响力 |

MCP 不可用时跳过本节，不影响解读主链路。

工具在 **`tools/`**（本包 `extract/` · `analyze/` · `vault/`）。  
中间产物：用户工作区 **`outputs/patent_reader/`**。PDF：`tools/extract/fetch_patent_pdf.py`；入库：`tools/vault/write_patent_obsidian_note.py`。
=======
工具在本包 **`tools/`**（`extract/` · `analyze/` · `vault/`）。PDF：`tools/extract/fetch_patent_pdf.py`；入库：`tools/vault/write_patent_obsidian_note.py`。特征行校验：`tools/analyze/validate_claim_features.py`。
>>>>>>> upstream/main

## 护栏

- 笔记、PDF 与特征行只用本包 `tools/`。

## 产出物

工作区 **`outputs/patent_reader/`**：通俗笔记、图谱中间产物、`claim_features.json`、`description_paragraphs.json`（含 `source_url`）。有库则另写入 Obsidian。对话给出笔记路径。
