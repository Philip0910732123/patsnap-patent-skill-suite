# 联网检索查新（Step 5）

> 本文件用于按技术主题查找现有技术。著录检索（发明人/申请人清单等）**不在本包**；整仓时另走检索技能，**禁止**把检索技能当成本包查新引擎。

## 必做时机

生成交底书全文**之前或生成过程中**必须执行；检索结论写入第一章 **1.1 现有技术** 及与本案的**区别论述**。

## 检索渠道（优先智慧芽 MCP 语义检索，再降级 CNIPA / WebSearch）

### A. 智慧芽 MCP 语义检索（优先）

在 Eureka 或已配置智慧芽 MCP 的环境中，**优先使用 `patsnap-search.patsnap_search`** 做语义检索，覆盖专利与文献：

```
# 1. 加载语义检索工具 schema
tool_load(server="patsnap-search", tool_name="patsnap_search")

# 2. 语义检索（自然语言查询，覆盖专利+文献）
tool_invoke(tool="mcp_patsnap-search__patsnap_search", arguments={
    "query": "知识库检索增强 大语言模型",
    "type": "patent",  # patent|literature|all
    "limit": 20
})

# 3. 获取单条详情（可选，深入理解某篇专利/文献）
tool_load(server="patsnap-search", tool_name="patsnap_fetch")
tool_invoke(tool="mcp_patsnap-search__patsnap_fetch", arguments={
    "id": "<从检索结果获取>"
})
```

**优势**：
- 语义检索，无需手动拆词、无需两轮分类号收口
- 覆盖全球专利 + 科技文献（不限于中国公布公告）
- 结构化 JSON 返回，含标题、摘要、公开号、申请人、分类号等
- 不受 WAF/验证码/DOM 改版影响
- 支持自然语言查询，无需构造复杂布尔式

**检索策略**：
1. **第一轮（语义召回）**：用技术方案核心描述做自然语言查询，`limit: 20`，`type: patent`
2. **筛选**：从结果中筛出与本案**技术手段对得上**的条目（吸附/接枝/再生，或外观的造型要点），目标 4～8 条
3. **不足 4 条**：换更贴近本案手段的查询串重试，或改 `type: all` 加入文献
4. **仍不足**：1.1 如实写「检索范围内近邻较少」，**禁止编造条目凑数**
5. **获取详情**：对高相关条目用 `patsnap_fetch` 获取完整摘要和权利要求，确保 1.1 概括准确

**专利类型过滤**：
- 发明：查询时加 `country: CN`，结果中按公开号 `CN…A` / `CN…B` 过滤
- 实用新型：公开号 `CN…U`，或查询时加关键词「实用新型」
- 外观设计：公开号 `CN…S`，或查询时加关键词「外观设计」

**abstract 字段（规定必用）**：

若检索结果中某项含非空的摘要/abstract，对该条专利须同时遵守：

- **必用**：查新笔记、交底书 **1.1** 中对该专利的技术方案概括、应用场景与局限性分析，**必须先基于对该 abstract 的完整阅读与理解**后再撰写；**禁止**仅凭标题、公开号臆造方案要点。
- **充分理解**：写入 1.1 前，Agent 须在推理过程内明确：摘要所涉技术领域、解决什么问题、核心手段/模块、主要效果或流程；若摘要与标题存在差异，**以摘要为准**。
- **正文呈现**：交底书 1.1 中**不得**大段逐字粘贴官方摘要；应消化后用自己的话压缩为「方案概括 + 应用 + 缺点/局限」。
- **缺失时**：若某条无摘要，用 `patsnap_fetch` 获取详情补全理解后再写 1.1，**不得**留空含糊带过。

### B. CNIPA 公布公告站（降级回退）

无 MCP 环境时降级到原 Playwright 爬取方案（一词一页）：

```bash
python skills/patent-disclosure/tools/browser.py --probe
python skills/patent-disclosure/tools/crawl/cnipa_epub_search.py --type invention 词甲 词乙 词丙
```

CNIPA 模式的两轮查新（关键词召回 → IPC/LOC 分类号收口）逻辑见原版 `cnipa_epub_search.py` 和 `EPUB_CLASS_HINT` 机制。降级条件：MCP 工具不可用、未配置智慧芽 MCP 服务器、或用户明确要求用 CNIPA。

**stderr ≠ 失败**：退出码 0 且 stdout 有 `EPUB_HITS_JSON:` 即为成功。PowerShell `NativeCommandError` 不等于失败，**禁止**因此降级。

### C. Google 学术与 Google Patents（补充）

在 A 和 B 结果不足时启用：

1. **中文文献与学术**：Google 学术搜索，用中文关键词、技术方案核心术语，可组合 2–3 组查询
2. **专利公开文献（补充）**：Google Patents，按类型过滤（发明 `type=PATENT` + `country:CN`；外观 `type=DESIGN`）
3. 每条使用稳定著录页 URL

## 分析要求

对检索到的、与方案**高度相关**的现有专利或公开文献逐项概括：

- 专利号 / 文献标识
- 技术方案要点（若含 abstract，要点须与摘要理解一致）
- 应用场景
- **局限性**
- **公开源 URL（必填）**：每一条必须附带至少一个可公开访问、与著录项一致的链接

### 链接来源与格式

| 类型 | URL 形式 | 说明 |
|------|---------|------|
| 智慧芽 MCP 命中 | `https://analytics.zhihuiya.com/patent-view/abst?patentId={uuid}` | 从 MCP 返回的 `id` 字段构造 |
| CNIPA 命中 | JSON 的 `link`，如 `http://epub.cnipa.gov.cn/patent/CN…` | 照抄 `link`，勿改域名 |
| Google Patents 补条 | `https://patents.google.com/patent/CN…/en` | 仅无 MCP/CNIPA link 时使用 |
| 学术论文 | Scholar 条目页、DOI：`https://doi.org/10.xxxx/...` | 以 DOI 解析后页面与文献一致为准 |
| arXiv 预印本 | `https://arxiv.org/abs/xxxx.xxxxx` | `abs` 页为规范条目页 |

**禁止编造或猜测 URL**。写入前应确认页面可访问且对应同一文献/专利。

文末给出：**检索总结**与**本发明与现有技术的本质区别**，与 1.1 结尾及 1.2 缺点呼应。

## 记录习惯

保留专利号、标题、消化摘要后的一两句方案概括；每条另起一行给出「来源 URL」。避免大段抄袭权利要求或整段粘贴官方摘要。

### 1.1「检索说明」写法

写入交底书 1.1 开头的「检索说明」时，面向代理人/审查员表述，**不要**暴露 Agent 查新流程或工具实现。

- **须写**：实际使用的公开数据库或渠道名称（如「智慧芽专利数据库」「国家知识产权局专利公布公告系统」）、本案主要检索词；若做了分类号收口，可写 IPC 或外观 LOC
- **禁止写入 1.1 正文**：脚本/文件名、MCP 工具名、Playwright、WebSearch、Agent、技能仓库名等内部或流程元信息

**示例**：

> 检索说明：在**智慧芽专利数据库**及 **Google Patents** 中，以「批任务调度」「异构集群调度」「任务队列重排」「负载感知调度」等为检索词进行语义检索；部分条目的公开文本与著录项以 Google Patents 页面复核。
