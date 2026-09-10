# 专利全景分析（执行流程）

## 适用时机

用户需要对某个**技术赛道**做宏观专利竞争格局分析，而非单件专利检索或查新。

典型触发：
- 全景分析、技术赛道、竞争格局、专利 landscape
- "帮我看看 XX 领域的专利分布"
- "XX 技术的专利趋势怎么样"
- `/patent-landscape`、`/全景分析`

## 前置确认

开始前向用户确认：

| 确认项 | 默认值 | 说明 |
|--------|--------|------|
| 技术主题 | 用户提供 | 必须有明确的技术关键词或描述 |
| 时间范围 | 近 10 年 | 用户可指定区间 |
| 地域范围 | 全球 | 用户可指定中国/美国/欧洲等 |
| 分析深度 | 标准四维 | 趋势+构成+申请人排名+技术地图；深度=加生命周期+合作网络+被引排名 |
| 重点申请人 | 无 | 用户可指定关注特定公司 |

## 工作流

### 第 1 步：检索建池

```
tool_load(server="patent-landscape", tool_name="search_patents_v3")
```

按技术主题检索，获取专利集和总数。**记录 `matched_total`**。

- `limit` 默认 20 条作为 sample
- 检索条件包含：关键词/分类号/时间范围/地域
- **不要**把 20 条 sample 当总数；`matched_total` 才是查询范围总数

如果用户关注特定申请人，可叠加申请人过滤。

### 第 2 步：趋势分析

```
tool_load(server="patent-landscape", tool_name="trend")
```

获取申请年份趋势数据，生成趋势表：
- 年份 vs 申请量
- 标注峰值年份和增长拐点
- 趋势类型判断：上升/平稳/下降/新兴

### 第 3 步：技术构成

```
tool_load(server="patent-landscape", tool_name="technology_constitute")
```

获取技术分支构成，生成构成表：
- 技术分支 vs 专利数 vs 占比
- 标注主要技术方向和新兴方向

### 第 4 步：申请人排名

```
tool_load(server="patent-landscape", tool_name="applicant_rank")
```

获取申请人排名，生成排名表：
- 申请人 vs 专利数 vs 占比
- 标注头部集中度（CR3/CR5/CR10）
- 用户指定关注的公司高亮标注

### 第 5 步：技术地图（标准四维最后一维）

```
tool_load(server="patent-landscape", tool_name="domain_map")
```

获取技术领域分布地图，描述技术领域交叉分布情况。

### 第 6 步（深度扩展，用户指定时执行）

| 维度 | MCP 工具 | 产出 |
|------|----------|------|
| 技术生命周期 | `technology_life_cycle` | 判断技术处于萌芽/成长/成熟/衰退期 |
| 合作网络 | `cooperation_applicant_analysis` | 产学研合作矩阵 |
| 申请人技术布局 | `applicant_technology_analysis` | 头部申请人技术分支分布 |
| 申请人趋势 | `applicant_trend` | 头部申请人年份趋势 |
| 被引排名 | `refered_rank` | 高被引专利排名 |
| 同族规模 | `famn_rank` | 同族规模排名（衡量全球布局强度） |
| 地域分布 | `rec_office` | 专利局/地域分布 |

### 第 7 步（可选）：文本挖掘

```
tool_load(server="patent-analysis", tool_name="mine_patent_text")
```

对专利集做关键词词云、技术问题-技术手段-技术效果三要素挖掘。

### 第 8 步：生成报告

将以上维度的数据整合为 Markdown 报告，结构：

```markdown
# XX 技术专利全景分析

## 一、检索概况
- 技术主题、检索条件、专利总数（matched_total）
- 数据来源：智慧芽 MCP patent-landscape 服务

## 二、申请趋势
| 年份 | 申请量 | 趋势 |
（趋势表）

## 三、技术构成
| 技术分支 | 专利数 | 占比 |
（构成表）

## 四、申请人排名
| 排名 | 申请人 | 专利数 | 占比 |
（排名表，头部集中度）

## 五、技术地图
（领域分布描述）

## 六、深度分析（如有）
### 6.1 技术生命周期
### 6.2 合作网络
### 6.3 被引排名

## 七、结论与建议
- 赛道成熟度判断
- 竞争格局特征
- 技术热点与空白点
```

报告落到 **`outputs/patent-landscape/LANDSCAPE-YYYYMMDD-HHMMSS.md`**。

## 完整性门禁

- **禁止**把 sample 条数当总数——`matched_total` 是总数
- 每个维度数据须标注 MCP 工具来源
- MCP 不可用时直接告知用户，不降级
- **不替代 FTO**——不做侵权风险判断
- **不替代查新**——不做单点新颖性判断

## 交付

1. 报告 Markdown 路径
2. 一句话赛道判断（成熟度+竞争格局）
3. 提醒用户专利法律状态可能已变更
