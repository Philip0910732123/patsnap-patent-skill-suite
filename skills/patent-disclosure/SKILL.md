---
name: patent-disclosure
description: "中国专利交底书：发明/实用新型/外观设计的专利点挖掘、轻量查新与成文。"
user-invocable: false
---

# 交底书编写

分步指令在 **`prompts/`**（本包内）。发明 / 实用新型 / 外观是**包内三个目录**，不是三个可触发技能。

| 步骤 | 文件 |
|------|------|
| Step 1 | `prompts/intake.md` |
| Step 2 | `prompts/project_scan.md` |
| Step 3–4 | `prompts/invention/` · `utility_model/` · `design/` 挖点 |
| 填表 / 线稿 | `prompts/fill_*`、`image_gen.md`、`*_lineart_*.md`；外观视图口径 `references/design_view_cnipa.md` |
| Step 5 | `prompts/prior_art_search.md`（轻量查新，一词一页） |
| Step 6 | `prompts/disclosure_preview.md` |
| Step 7 | 对应类型 `disclosure_builder.md` + `template_reference.md` |
| Step 8 | `prompts/disclosure_self_check.md` |
| 迭代 | `iteration_context.md` / `merger.md` / `correction_handler.md` |

查新工具：优先使用智慧芽 MCP `patsnap-search.patsnap_search` 做语义检索（覆盖专利+文献，无需拆词/两轮收口）；无 MCP 环境时降级到 `tools/crawl/cnipa_epub_search.py`（一词一页）。整仓安装时路径为 `skills/patent-disclosure/tools/crawl/cnipa_epub_search.py`。著录检索不在本包，**禁止**当查新引擎调用。  
交底交付后**不要**自动进入申请文件；用户点名并给出本目录后，再走 `skills/patent-application/SKILL.md`。  
MCP 模式：自然语言查询 → `patsnap_search` 语义召回 → 按 `limit: 20` 控制返回条数 → 筛选技术手段对得上的 4～8 条。CNIPA 模式：两段式——关键词 → `EPUB_CLASS_HINT` / IPC·LOC → `--class`；不足 4 条则同分类号回补第一轮。

线稿、CAD、公式、Word 出图用本包 `tools/`（`browser.py`、`mermaid_render.py`、`md_to_docx.py` 等）。
