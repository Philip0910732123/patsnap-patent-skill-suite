---
name: patent-reader
description: "专利通俗解读（智慧芽 MCP 增强）：公开号/PDF 成通俗笔记、图谱与 Obsidian 入库；MCP 可用时自动富化同族/引证/法律状态。"
user-invocable: false
---

# 专利通俗解读

1. **`Read`** `prompts/patent_plain_reader.md`
2. 实用新型或外观：**`Read`** `prompts/type_hooks.md` + `prompts/fill_*`
3. 笔记 / 自检：`obsidian_ofm_companion.md`、`patent_reader_self_check.md`

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

与交底互斥：解读不跑交底 Step 1–8。
