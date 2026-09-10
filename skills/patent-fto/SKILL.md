---
name: patent-fto
description: "自由实施分析（FTO）（智慧芽 MCP）：基于产品/技术方案检索风险专利，权要逐项对比，输出风险等级与规避建议。支持发明和外观设计 FTO。无 MCP 时不支持。"
user-invocable: false
---

# 自由实施分析（FTO）

基于智慧芽 MCP 工具链，对产品或技术方案做自由实施风险分析。

**须显式触发**：FTO、自由实施、侵权风险、风险专利、`/patent-fto`、`/fto`。

**先 `Read` `prompts/patent_fto.md`。**

## 检索渠道

### 仅智慧芽 MCP（无降级）

FTO 分析依赖智慧芽 `patsnap-ip-searching` 和 `novelty-search-lite` MCP 服务，**无 CNIPA 降级路径**。MCP 不可用时告知用户"需配置智慧芽 MCP"。

### MCP 工具清单

| 步骤 | MCP 工具 | 用途 |
|------|----------|------|
| FTO 分析 | `patsnap-ip-searching.fto_review` | 发明 FTO：产品/技术描述 → 风险专利识别 + 权要对比 |
| 外观 FTO | `patsnap-ip-searching.design_fto` | 外观设计 FTO：产品图片 → 相似外观专利检索 |
| 图片上传 | `patsnap-ip-searching.upload_image` | 外观 FTO 前置：上传产品图片 |
| 任务状态 | `patsnap-ip-searching.get_task` | 查询 FTO 任务执行状态 |
| 新颖性检索 | `novelty-search-lite.novelty_lite_search` | 技术方案 novelty 检索 |
| 特征提取 | `novelty-search-lite.novelty_feature_extract` | 从技术方案提取关键技术特征 |
| 特征对比 | `novelty-search-lite.novelty_feature_comparison` | 技术特征 vs 候选专利逐项对比 |
| 关键词提取 | `novelty-search-lite.novelty_keywords_extract` | 提取检索关键词 |
| 布尔检索 | `novelty-search-lite.novelty_lite_boolean_search` | 布尔逻辑检索专利 |
| 语义检索 | `novelty-search-lite.novelty_lite_semantic_search` | 语义向量检索专利 |
| 文献检索 | `novelty-search-lite.novelty_lite_paper_search` | 检索科技文献 |
| 报告生成 | `novelty-search-lite.novelty_lite_report_generate` | 生成查新报告 |
| 综述 | `novelty-search-lite.novelty_summary` | 汇总查新结论 |
| 建议评审 | `novelty-search-lite.novelty_review_with_suggestions` | AI 评审 + 修改建议 |
| 权要详情 | `core-patents.claims` | 获取风险专利权利要求全文 |
| 权要翻译 | `core-patents.claim_translated` | 获取权利要求中文翻译 |
| 法律状态 | `core-patents.get_patent_legal_status` | 核查风险专利法律状态 |
| 同族 | `core-patents.family` | 风险专利同族信息 |

调用方式：
```
tool_load(server="patsnap-ip-searching", tool_name="fto_review") → 读取 schema → tool_invoke
```

## FTO 类型

| 类型 | 输入 | 主工具 | 流程 |
|------|------|--------|------|
| 发明 FTO | 产品/技术方案文字描述 | `fto_review` | 描述 → 检索 → 权要对比 → 风险等级 |
| 外观 FTO | 产品图片 | `design_fto` | 图片 → 相似检索 → 风险分析 |

## 默认行为

- **风险等级**：高（权要全面覆盖）/ 中（部分覆盖）/ 低（仅边缘相关）
- **法律状态过滤**：默认只关注有效专利（授权+有效），失效专利标注但不算高风险
- **地域范围**：默认中国；用户可指定多国
- **结果量控制**：风险专利默认返回 top 10；用户可要求更多
- **权要对比**：逐项对比技术特征与权利要求，标注覆盖情况

## 结果落盘

结果默认落到 **`outputs/patent-fto/FTO-YYYYMMDD-HHMMSS.md`**（gitignore）。

Agent 将 MCP 返回的 JSON 格式化为 Markdown 报告（含权要对比表）后落盘。对话里告诉用户 Markdown 路径。

## 完整性门禁

- **法律状态必查**：每件风险专利必须核查法律状态；有效才计高风险
- **权要必读**：不能只看摘要就判风险；必须读 claims 全文做技术特征对比
- **同族必查**：风险专利须查同族，评估地域风险范围
- MCP 不可用时直接告知用户，**不降级**
- **FTO 不等于查新**：查新看新颖性/创造性，FTO 看侵权风险；两者目的不同

## 不做

- **不替代全景分析**：FTO 是单点风险判断，不做赛道级宏观分析（全景走 `patent-landscape`）
- **不做无效宣告建议**：只做风险识别和规避方向提示，不做无效策略（那是专利代理师的工作）
- **不跨包调用**其他子技能的 `tools/`
- **免责声明必须**：报告末尾必须附"本报告基于智慧芽 MCP 检索结果，不构成法律意见，建议咨询专业专利律师"
