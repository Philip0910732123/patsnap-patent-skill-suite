---
name: patent-oa
description: "审查答复辅助：审查意见问答与草稿；库薄时引导案例入库与实务书蒸馏。须显式触发。"
user-invocable: false
---

# 审查答复辅助

须用户点名（审查意见 / OA / 入库 / 实务书）。草稿须复核后递交。  
**主场景**是问和答、出意见陈述草稿；用户确认采纳后才出陈述正文 Word（本包 `tools/emit_opinion_docx.py`，禁止调用交底包）。案例入库与实务书蒸馏是让检索变准的配套。每次答复完整回答的末块为 **`## 交付后请确认`**，按 `prompts/soft_nudge.md` 看库是否太薄（历史案或手册少于 3），再决定是否加「案例入库」「实务书蒸馏」。

1. **`Read`** `prompts/guardrails.md` → `intake.md`
2. 向量可选：`prompts/configure_embedding.md` + `tools/config.py`
3. **扫描件 PDF 处理**：审查意见通知书若为扫描件（`pdf_text.py` 提取为空或字符 < 80），须先使用 MCP OCR 工具（`document-processing` MCP 或 MinerU MCP）提取文本，再将提取后的 .txt 传给 `search_cases.py --pdf`。不要跳过 OCR 直接使用空文本。
4. 答复：`prompts/respond_office_action.md` + `tools/search_cases.py --pdf`
5. 用户确认采纳：`assets/opinion_statement.md` → `tools/emit_opinion_docx.py`
6. 入库（用户同意后）：`tools/ingest_case.py`；手册：`tools/ingest_playbook.py`

依赖：`pip install -r tools/requirements-oa.txt`。
