# 自由实施分析（FTO）执行流程

## 适用时机

用户需要对产品或技术方案做**自由实施风险分析**，识别可能侵权的有效专利。

典型触发：
- FTO、自由实施、侵权风险、风险专利
- "我的产品有没有侵权风险"
- "这个技术方案能不能自由实施"
- `/patent-fto`、`/fto`

**与查新的区别**：查新看"我的方案够不够新颖"，FTO 看"我的产品会不会侵犯别人的专利"。

## 前置确认

开始前向用户确认：

| 确认项 | 默认值 | 说明 |
|--------|--------|------|
| 技术方案/产品描述 | 用户提供 | 必须有明确的技术描述或产品图片 |
| FTO 类型 | 自动判断 | 文字描述→发明 FTO；图片→外观 FTO |
| 地域范围 | 中国 | 用户可指定多国 |
| 法律状态过滤 | 仅有效专利 | 失效专利标注但不计高风险 |
| 关注申请人 | 无 | 用户可指定关注特定权利人 |

## 工作流

### 第 1 步：FTO 任务提交

#### 发明 FTO

```
tool_load(server="patsnap-ip-searching", tool_name="fto_review")
```

提交产品/技术方案文字描述，启动 FTO 分析任务。记录 `task_id`。

#### 外观 FTO

```
# 1. 上传产品图片
tool_load(server="patsnap-ip-searching", tool_name="upload_image")
tool_invoke(tool="mcp_patsnap-ip-searching__upload_image", arguments={
    "image": "<图片路径或 URL>"
})

# 2. 提交外观 FTO 任务
tool_load(server="patsnap-ip-searching", tool_name="design_fto")
tool_invoke(tool="mcp_patsnap-ip-searching__design_fto", arguments={
    "image_url": "<上传返回的 URL>"
})
```

### 第 2 步：等待任务完成

```
tool_load(server="patsnap-ip-searching", tool_name="get_task")
tool_invoke(tool="mcp_patsnap-ip-searching__get_task", arguments={
    "task_id": "<task_id>"
})
```

FTO 是异步任务，需要轮询直到 `status=completed`。

### 第 3 步：风险专利法律状态核查

对每件候选风险专利，**必须**核查法律状态：

```
tool_load(server="core-patents", tool_name="get_patent_legal_status")
tool_invoke(tool="mcp_core-patents__get_patent_legal_status", arguments={
    "patent_id": "<风险专利 ID>"
})
```

- 法律状态为"有效/授权" → 计入高风险
- 法律状态为"失效/撤销/放弃" → 标注但降级为低风险
- 无法查到法律状态 → 标注"法律状态未核实"

### 第 4 步：权要全文获取与对比

对每件**有效**风险专利，获取权利要求全文做逐项对比：

```
# 获取权要全文
tool_load(server="core-patents", tool_name="claims")
tool_invoke(tool="mcp_core-patents__claims", arguments={
    "patent_id": "<风险专利 ID>"
})

# 获取中文翻译（非中文专利）
tool_load(server="core-patents", tool_name="claim_translated")
tool_invoke(tool="mcp_core-patents__claim_translated", arguments={
    "patent_id": "<风险专利 ID>"
})
```

对比表格式：

| 我方技术特征 | 对方权要限定 | 覆盖情况 | 风险 |
|-------------|------------|----------|------|
| 特征 A | 权1：… | 完全覆盖 | 高 |
| 特征 B | 权3：… | 部分覆盖 | 中 |
| 特征 C | （无对应） | 未覆盖 | 低 |

### 第 5 步：同族查询（评估地域风险）

对高风险专利，查同族以评估地域风险范围：

```
tool_load(server="core-patents", tool_name="family")
tool_invoke(tool="mcp_core-patents__family", arguments={
    "patent_id": "<高风险专利 ID>"
})
```

### 第 6 步（可选）：深度查新补充

如果 FTO 结果有限，可用 novelty-search-lite 做补充检索：

```
tool_load(server="novelty-search-lite", tool_name="novelty_lite_search")
tool_load(server="novelty-search-lite", tool_name="novelty_feature_extract")
tool_load(server="novelty-search-lite", tool_name="novelty_feature_comparison")
```

### 第 7 步：生成 FTO 报告

```markdown
# 自由实施分析报告（FTO）

## 一、分析概况
- 技术方案描述
- FTO 类型（发明/外观）
- 地域范围
- 数据来源：智慧芽 MCP patsnap-ip-searching 服务

## 二、风险专利清单
| 排名 | 公开号 | 标题 | 申请人 | 法律状态 | 风险等级 |
（风险专利表，按风险等级降序）

## 三、高风险专利详析
### 3.1 专利 CNXXXXXX
- 法律状态：有效
- 权要对比表
- 同族地域分布
- 规避方向提示

## 四、中等风险专利
（简要说明覆盖差异）

## 五、低风险/失效专利
（仅列出，不展开）

## 六、结论与建议
- 整体风险等级判断
- 重点规避方向
- 建议进一步动作（如绕开设计、许可谈判等）

## 免责声明
本报告基于智慧芽 MCP 检索结果，不构成法律意见。
专利法律状态可能已变更，建议咨询专业专利律师。
数据截止：YYYY-MM-DD
```

报告落到 **`outputs/patent-fto/FTO-YYYYMMDD-HHMMSS.md`**。

## 完整性门禁

- **法律状态必查**：每件风险专利必须核查
- **权要必读**：不能只看摘要判风险
- **同族必查**：高风险专利必须查同族
- **免责声明必须**：报告末尾必须附免责声明
- **不替代查新**：FTO 看侵权，查新看新颖性

## 交付

1. FTO 报告 Markdown 路径
2. 一句话整体风险判断
3. 高风险专利数量和 top 3 规避方向
4. 免责声明
