---
name: patent-search
description: "专利著录检索（智慧芽 MCP 增强）：发明人、申请人、分类号、名称、摘要；支持语义检索和同族/引证分析。也可从单图或权利要求生成关键字后查询。无 MCP 环境时降级到 CNIPA 公布公告站爬取。"
user-invocable: false
---

# 著录检索

通用专利著录检索，不是「个人清单技能」。个人公开清单只是一种用法。

**先 `Read` `prompts/patent_search.md`。** 用户给单图或权要时再 `Read` `prompts/derived_query.md`。

## 检索渠道（双通道）

### A. 智慧芽 MCP（优先）

在 Eureka 或已配置智慧芽 MCP 的环境中，**优先使用 MCP 工具**，无需 Playwright 或浏览器：

1. **专利检索**：`tool_load` 加载 `core-patents.search_patents`，按发明人/申请人/分类号/名称/摘要等字段检索
2. **著录详情**：`tool_load` 加载 `core-patents.bibliography`，获取单件专利完整著录数据
3. **法律状态**：`tool_load` 加载 `core-patents.get_patent_legal_status` 或 `patent-status.legal_data`
4. **同族信息**：`tool_load` 加载 `core-patents.family`
5. **前向引证**：`tool_load` 加载 `core-patents.forward_citation`

调用方式：
```
tool_load(server="core-patents", tool_name="search_patents") → 读取 schema → tool_invoke
```

**优势**：结构化 JSON 返回，无需解析 HTML，不受 WAF/验证码影响，覆盖全球专利（不限于中国公布公告）。

### B. CNIPA 公布公告站（降级回退）

无 MCP 环境时（如纯 Claude Code / Cursor），降级到原 Playwright 爬取方案：
```bash
python skills/patent-search/tools/cnipa_search.py --inventor "姓名" --applicant "单位"
```

降级条件：MCP 工具不可用、未配置智慧芽 MCP 服务器、或用户明确要求用 CNIPA。

## 默认少翻页

- MCP 模式：通过 `tool_invoke` 的 `limit` / `page_size` 参数控制返回条数，默认 20 条；用户要求更多时增大 `limit` 或翻页
- CNIPA 模式：阈值在 `config.yaml`：`max_pages`（默认 3）；`max_pages_hard`（默认 20）
- **不要**一上来查全部。只有用户明确要求穷举清单时才翻完
- **不要**用配置 `page_size` 估总条数
- 采到总数才能说「已查全部」；没采到只谈「还能否翻页」

## 命令示例

### MCP 模式（Eureka / 已配置 MCP）

Agent 直接调用 MCP 工具，无需 Python 脚本：

```
# 1. 加载检索工具 schema
tool_load(server="core-patents", tool_name="search_patents")

# 2. 按发明人检索
tool_invoke(tool="mcp_core-patents__search_patents", arguments={
    "inventor": "张三",
    "applicant": "某公司",
    "type": "all"  # invention|utility_model|design|all
})

# 3. 获取著录详情
tool_load(server="core-patents", tool_name="bibliography")
tool_invoke(tool="mcp_core-patents__bibliography", arguments={
    "patent_id": "<从检索结果获取>"
})

# 4. 获取法律状态（可选）
tool_load(server="patent-status", tool_name="legal_data")
tool_invoke(tool="mcp_patent-status__legal_data", arguments={
    "patent_id": "<patent_id>"
})
```

### CNIPA 模式（降级）

```bash
python skills/patent-search/tools/cnipa_search.py --inventor "姓名" --applicant "单位"
python skills/patent-search/tools/cnipa_search.py --title "数据处理" --abstract "吸附 and 再生" --class B01J20 --max-pages 2
python skills/patent-search/tools/cnipa_search.py --abstract "折叠 and 杯盖" --type design --derived-from image --type-inferred --derived-note "折叠杯盖"
python skills/patent-search/tools/cnipa_search.py --inventor "姓名" --complete
```

单图必须 `--type design|utility_model|invention`，不能 `all`。用户没说类型时看图推断并加 `--type-inferred`。权要按文本选类型，可用 `all`。

单独拷走本包时：`python tools/cnipa_search.py …`。

## 结果落盘

结果默认落到 **`outputs/patent-search/SEARCH-YYYYMMDD-HHMMSS.md`**（gitignore）。

- MCP 模式：Agent 将 MCP 返回的 JSON 格式化为 Markdown 表格后落盘
- CNIPA 模式：`tools/emit_search_report.py` 自动落盘

改版式只动 `tools/emit_search_report.py`。

机读前缀（CNIPA 模式）：`EPUB_SEARCH_MD:` / `EPUB_SEARCH_JSON:` / `EPUB_SEARCH_NOTE:` / `EPUB_SEARCH_INCOMPLETE:`。对话里告诉用户 Markdown 路径，不要只倒 JSON。

## 完整性门禁

- MCP 模式：`matched_total` 是查询范围总数；`returned_count` 是当前页条数。**不要把 returned_count 当总数**
- CNIPA 模式：退出码 `3` 表示分页不完整
- 普通多条件检索**禁止**声称「全部」
- WAF、验证码、DOM 改版属于检索失败，不等于零结果

## 同名归属（个人清单用法）

- `verified_inventor_metadata` → "已由官方发明人著录核实"
- `inventor_query_and_applicant` → "发明人查询与申请人共同匹配"
- `inventor_query_only_unverified_namesake` → "仅姓名查询命中，同名归属待核实"

MCP 模式下，智慧芽著录数据天然带发明人/申请人字段，同名归属核实更准确。

**不做**：Google Patents / 学术检索与跨库去重（但可通过 `patsnap-search.patsnap_search` 做语义检索，覆盖专利+文献）、PSS 登录站、按附图视觉相似检索。单图/权要只生成检索式。
**禁止**被交底 Step 5 当查新引擎调用（交底查新走 `patsnap-search.patsnap_search` 语义检索）。
