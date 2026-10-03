# 专利著录检索

用于按发明人、申请人/单位、分类号、名称、摘要/简要说明、申请号或公开号等字段检索专利。个人公开清单只是其中一种用法，不是本包的全部定义。

用户给**一张图**或**一段权利要求**时，先 `Read` `prompts/derived_query.md`，把材料收成名称/摘要关键字后再检索；不要把图上传到公布站，也不要声称以图搜图或权要语义检索。

与交底 Step 5 技术主题查新不同：本流程走多条件字段检索；**不要**用交底语义查新的结果代替本包。

## 必要输入

至少一项：发明人、申请人、分类号、名称、摘要/简要说明、申请号或公开号。缺省字段不填。多条件按 AND 逻辑。

单图 / 权要入口另须：读懂材料后至少填名称或摘要。**单图必须带类型**（design / utility_model / invention），禁止 `all`；用户没说类型时看图推断。抽词口径见 `prompts/derived_query.md`。权要按权利要求主题选类型，可用 `all`。

个人清单场景另须：

- 发明人/设计人姓名；
- 已知申请人或任职单位别名（可多个）。缺少申请人时可先返回候选集，但须标注同名归属尚未核实。

## 检索渠道

### A. 智慧芽 MCP（优先）

在 Eureka 或已配置智慧芽 MCP 的环境中，**优先使用 MCP 工具**：

```
# 1. 加载检索工具 schema
tool_load(server="core-patents", tool_name="search_patents")

# 2. 按发明人 + 申请人检索
tool_invoke(tool="mcp_core-patents__search_patents", arguments={
    "inventor": "张三",
    "applicant": "某公司",
    "country": "CN",
    "limit": 20
})

# 3. 按名称 + 摘要 + 分类号检索
tool_invoke(tool="mcp_core-patents__search_patents", arguments={
    "title": "数据处理",
    "abstract": "吸附 and 再生",
    "ipc": "B01J20",
    "limit": 20
})

# 4. 获取单件著录详情
tool_load(server="core-patents", tool_name="bibliography")
tool_invoke(tool="mcp_core-patents__bibliography", arguments={
    "patent_id": "<从检索结果获取>"
})

# 5. 获取法律状态（可选）
tool_load(server="patent-status", tool_name="legal_data")
tool_invoke(tool="mcp_patent-status__legal_data", arguments={
    "patent_id": "<patent_id>"
})
```

**优势**：
- 结构化 JSON 返回，无需解析 HTML
- 不受 WAF/验证码/DOM 改版影响
- 覆盖全球专利（不限于中国公布公告）
- 自带发明人/申请人/分类号/摘要等著录字段
- 可扩展同族、引证、法律状态分析

**分页**：MCP 返回含 `matched_total`（查询范围总数）和 `returned_count`（当前页条数）。用户要求更多时翻页或增大 `limit`。**不要**把 `returned_count` 当总数。

**完整性门禁**：
- `matched_total` 是查询范围总数，不是整个数据库总数
- 普通多条件检索**禁止**声称「全部」
- 只有翻完所有页且无遗漏时才可说「已查全部」
- MCP 工具返回错误时如实报告，不降级到零结果

### B. CNIPA 公布公告站（降级回退）

无 MCP 环境时（如纯 Claude Code / Cursor 未配置智慧芽 MCP），降级到原 Playwright 爬取方案：

```bash
python skills/patent-search/tools/cnipa_search.py \
  --inventor "姓名" \
  --applicant "申请主体一" \
  --applicant "申请主体二" \
  --type all
```

其他字段示例：`--title`、`--abstract`、`--class`、`--application-number`、`--publication-number`。

降级条件：MCP 工具不可用、未配置智慧芽 MCP 服务器、或用户明确要求用 CNIPA。

CNIPA 模式的分页、完整性门禁、同名归属逻辑见原版 `config.yaml` 和 `emit_search_report.py`。

## 结果落盘

结果默认落到 **`outputs/patent-search/SEARCH-YYYYMMDD-HHMMSS.md`**（gitignore）。

- MCP 模式：Agent 将 MCP 返回的 JSON 格式化为 Markdown 表格后落盘
- CNIPA 模式：`tools/emit_search_report.py` 自动落盘

改版式只动 `tools/emit_search_report.py`。

对话里告诉用户 Markdown 路径和中文摘要，不要只倒 JSON 键。

## 链接格式

| 来源 | URL 形式 | 说明 |
|------|---------|------|
| 智慧芽 MCP | `https://analytics.zhihuiya.com/patent-view/abst?patentId={uuid}` | 从 MCP 返回的 `id` 字段构造 |
| CNIPA | `http://epub.cnipa.gov.cn/patent/CN…` | 从 JSON 的 `link` 字段照抄 |
| Google Patents（补充） | `https://patents.google.com/patent/CN…/en` | 仅无 MCP link 时使用 |

**禁止编造** URL。写入前确认链接与著录项一致。

## 同名归属（个人清单用法）

- MCP 模式：智慧芽著录数据天然带发明人/申请人字段，同名归属核实更准确
- CNIPA 模式：
  - `verified_inventor_metadata` → "已由官方发明人著录核实"
  - `inventor_query_and_applicant` → "发明人查询与申请人共同匹配"
  - `inventor_query_only_unverified_namesake` → "仅姓名查询命中，同名归属待核实"

<<<<<<< HEAD
## 不做

- Google Patents 学术检索与跨库去重（但可通过 `patsnap-search.patsnap_search` 做语义检索，覆盖专利+文献）
- PSS 登录站
- 按附图视觉相似检索
- 单图/权要只生成检索式
- **禁止**被交底 Step 5 当查新引擎调用（交底查新走 `patsnap-search.patsnap_search` 语义检索）
=======
机读前缀：`EPUB_SEARCH_MD:` / `EPUB_SEARCH_JSON:`（stdout）、`EPUB_SEARCH_NOTE:` / `EPUB_SEARCH_INCOMPLETE:`（stderr）。面向用户给 Markdown 路径和中文摘要，不要只倒 JSON 键。

## 按特征精排（可选旁路）

用户点名或对照表派工时，`Read` `prompts/covers_rank.md`。用命中摘要对 Fk 打 `covers_feature`，经 `emit_covers_report.py` 另写 `SEARCH-*.covers.md` / `.covers.json`。**禁止**改写本次 `SEARCH-*.md` 列表。无点名不要生成 covers。
>>>>>>> upstream/main
