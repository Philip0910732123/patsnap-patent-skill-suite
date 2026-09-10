---
name: patent-landscape
description: "专利全景分析（智慧芽 MCP）：技术赛道检索→趋势/构成/申请人排名/技术地图/生命周期/合作网络多维度分析，生成赛道竞争格局报告。无 MCP 时不支持。"
user-invocable: false
---

# 专利全景分析

基于智慧芽 MCP 工具链，对指定技术主题做多维度专利全景分析。

**须显式触发**：全景分析、技术赛道、竞争格局、专利 landscape、`/patent-landscape`、`/全景分析`。

**先 `Read` `prompts/patent_landscape.md`。**

## 检索渠道

### 仅智慧芽 MCP（无降级）

全景分析依赖智慧芽 `patent-landscape` MCP 服务的多维统计接口，**无 CNIPA 降级路径**。MCP 不可用时告知用户"需配置智慧芽 MCP"。

### MCP 工具清单

| 步骤 | MCP 工具 | 用途 |
|------|----------|------|
| 检索 | `patent-landscape.search_patents_v3` | 按技术主题检索专利集 |
| 统计 | `patent-landscape.search_patents_statistics` | 检索结果总数/分布 |
| 趋势 | `patent-landscape.trend` | 申请年份趋势 |
| 构成 | `patent-landscape.technology_constitute` | 技术分支构成 |
| 申请人 | `patent-landscape.applicant_rank` | 申请人排名 |
| 申请人趋势 | `patent-landscape.applicant_trend` | 重点申请人申请趋势 |
| 技术地图 | `patent-landscape.domain_map` | 技术领域分布地图 |
| 生命周期 | `patent-landscape.technology_life_cycle` | 技术生命周期阶段 |
| 合作网络 | `patent-landscape.cooperation_applicant_analysis` | 产学研合作分析 |
| 申请人技术 | `patent-landscape.applicant_technology_analysis` | 申请人技术布局 |
| 地域分布 | `patent-landscape.rec_office` | 专利局/地域分布 |
| 同族排名 | `patent-landscape.famn_rank` | 同族规模排名 |
| 被引排名 | `patent-landscape.refered_rank` | 被引排名 |
| 聚合 | `patent-landscape.detail_aggregation` | 多维交叉聚合 |
| 文本挖掘 | `patent-analysis.mine_patent_text` | 关键词词云/技术效果 |
| 可视化 | `patent-visual.trends` / `applicant_ranking` / `word_cloud` | 图表生成 |

调用方式：
```
tool_load(server="patent-landscape", tool_name="search_patents_v3") → 读取 schema → tool_invoke
```

## 默认行为

- **检索范围**：默认全球专利，用户要求只看中国时加国别过滤
- **时间范围**：默认近 10 年，用户可指定区间
- **分析维度**：默认跑趋势+构成+申请人排名+技术地图四维；用户指定时扩展到生命周期/合作网络/被引排名
- **结果量控制**：检索时 `limit` 默认 20 条/sample；全景统计按 MCP 返回的聚合数据，不需要拉全量专利列表
- **不要**一上来翻完所有分页——先看统计聚合，再按用户兴趣深挖特定维度

## 结果落盘

结果默认落到 **`outputs/patent-landscape/LANDSCAPE-YYYYMMDD-HHMMSS.md`**（gitignore）。

Agent 将 MCP 返回的 JSON 格式化为 Markdown 报告（含表格）后落盘。对话里告诉用户 Markdown 路径。

## 完整性门禁

- `matched_total` 是查询范围总数；`returned_count` 是当前页条数。**不要把 returned_count 当总数**
- MCP 工具不可用时直接告知用户，**不要**降级到 CNIPA 爬虫（全景分析无法靠爬虫实现）
- 每个维度的数据来源须标注对应的 MCP 工具名

## 不做

- **不替代 FTO**：全景分析看竞争格局，不做侵权风险判断（FTO 走 `patent-fto` 子技能）
- **不替代查新**：全景分析是赛道级宏观分析，不做单点新颖性判断（查新走交底 Step 5 或 `novelty-search-lite`）
- **不跨包调用**其他子技能的 `tools/`
