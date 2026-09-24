---
<<<<<<< HEAD
name: patsnap-patent-skill-suite
description: "中国专利全流程技能套件（智慧芽 MCP 增强）：挖掘专利点与编写交底书（发明/实用/外观），把已有交底改写成申请文件四件套，也可按材料交底申请一起做，著录检索支持智慧芽 MCP 语义检索与同族/引证分析，通俗解读专利，对照审查口径出政策简报，辅助审查答复。| China patents skill suite (PatSnap MCP enhanced): mine patent points and draft disclosures, rewrite an existing disclosure into application documents, search patents via PatSnap MCP with semantic search and family/citation analysis, explain patents, brief examination-policy changes, and assist office-action responses."
version: "1.0.0"
=======
name: patent-disclosure-skill
description: "中国专利技能：挖掘专利点与编写交底书（发明/实用/外观），把已有交底改写成申请文件四件套，也可按材料交底申请一起做，按著录字段检索公布公告，通俗解读专利，基于已读库打开专利地图，对照审查口径出政策简报，辅助审查答复。| China patents skill: mine patent points and draft disclosures, rewrite an existing disclosure into application documents, or chain disclosure-then-application from inventor materials in one pass (ask when facts are missing; at most three issue-list rounds), search CNIPA bibliographic records, explain patents, open a local patent map from interpreted notes, brief examination-policy changes, and assist office-action responses."
version: "4.13.0"
>>>>>>> upstream/main
user-invocable: true
argument-hint: "[可选：项目路径 / 交底书 / 申请底稿 / 交底申请一起做 / 专利检索 / 专利号或 PDF / 专利地图 / 专利围栏 / 政策简报 / 审查答复]"
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, Bash
---

# 中国专利技能

按用户意图 **`Read`** 对应入口的 `SKILL.md`，再按该流程执行。**先查「路由判定表」定去向，再看「通则」。**

<<<<<<< HEAD
| 能力 | 做什么 | 何时进入 | 入口 |
|------|--------|----------|------|
| **交底** | 挖专利点 → 查新 → 成稿 → 迭代 | 专利挖掘、交底书、查新、实用新型、外观设计；`/patent-disclosure`、`/交底书` | `skills/patent-disclosure/SKILL.md` |
| **申请文件** | 已有交底 → 权要 / 说明书 / 摘要 / 附图 | **须显式**且**指定交底目录**：申请文件、申请底稿、申报材料、`/申请底稿`、`/patent-apply`。仅缺材料则终止；内容争议写入问题清单；交付末尾须摘要清单；改已有产出则另存 | `skills/patent-application/SKILL.md` |
| **案卷** | 按发明人/工程师给的材料一趟写出交底书和申请文件；清单缺口最多来回三轮，缺事实问人、不编 | **须显式**：交底申请一起做、从零出交底和申请、一条龙、帮写交底再出申请、按清单改、会稿、案卷、`/patent-docket`。只写交底或已有交底只出四件套 → 不要进本案。状态 `outputs/docket/` | `skills/patent-docket/SKILL.md` |
| **检索** | 智慧芽 MCP 语义检索 + 著录字段检索 + 同族/引证分析 | 按著录字段查专利、个人公开清单、语义检索；`/patent-search`。无 MCP 时降级 CNIPA 公布公告站。普通多条件**不要**默认翻完全部分页 | `skills/patent-search/SKILL.md` |
| **解读** | 公开号 / PDF / 全文 → 通俗笔记 + 图谱 | 读专利、公开号或 PDF 且目标为理解；`/patent-read`、`/读专利` | `skills/patent-reader/SKILL.md` |
| **审查答复** | 审查意见问答与草稿；库薄时引导入库/蒸馏 | **须显式**：审查意见、OA、案例入库、实务书、`/oa` | `skills/patent-oa/SKILL.md` |
| **政策简报** | 对照国知局口径，说明对交底写法/本稿的影响；改技能仅为旁路 | **须显式**：政策简报、政策雷达、`/政策简报`、`/patent-brief`、`/patent-exam-policy`。「技能进化 / `/patent-evolve`」同一入口，仍先出简报 | `skills/patent-exam-policy/SKILL.md` |
| **全景分析** | 技术赛道检索→趋势/构成/申请人排名/技术地图/生命周期多维度分析 | **须显式**：全景分析、技术赛道、竞争格局、专利 landscape、`/patent-landscape`。仅 MCP 模式，无降级 | `skills/patent-landscape/SKILL.md` |
| **FTO** | 产品/技术方案→风险专利识别+权要对比+风险等级+规避方向 | **须显式**：FTO、自由实施、侵权风险、风险专利、`/patent-fto`、`/fto`。仅 MCP 模式，无降级 | `skills/patent-fto/SKILL.md` |
=======
## 能力总览
>>>>>>> upstream/main

| 能力 | 做什么 | 入口 |
|------|--------|------|
| **交底** | 挖专利点 → 查新 → 成稿 → 迭代（发明 / 实用新型 / 外观）；首篇定稿后可做保护型 1+N 专利布局 | `skills/patent-disclosure/SKILL.md` |
| **申请文件** | 已有交底 → 权要 / 说明书 / 摘要 / 附图 | `skills/patent-application/SKILL.md` |
| **案卷** | 按发明人/工程师给的材料一趟写出交底书和申请文件 | `skills/patent-docket/SKILL.md` |
| **检索** | 公布站高级查询（发明人/申请人/分类号/名称/摘要等）；单图或权要可先抽关键字再查 | `skills/patent-search/SKILL.md` |
| **解读** | 公开号 / PDF / 全文 → 通俗笔记 + 图谱 | `skills/patent-reader/SKILL.md` |
| **专利地图** | 已解读入库的案例摊成五种图（语义地形） | `skills/patent-map/SKILL.md` |
| **审查答复** | 审查意见问答与草稿；库薄时引导入库/蒸馏 | `skills/patent-oa/SKILL.md` |
| **政策简报** | 对照国知局口径，说明对交底写法/本稿的影响；改技能仅为旁路 | `skills/patent-exam-policy/SKILL.md` |

<<<<<<< HEAD
- 填表、线稿、CAD、公式、Word 出图在交底包 `prompts/` 与 `tools/`；解读填表用解读包 `prompts/fill_*`；Markdown 转 Word 的 `md_to_docx.py` **各包自带副本**。
- **禁止跨包调用**其他子技能的 `tools/`。需要同一能力就用本包副本。
- 专利号或 PDF 且意图为「读懂」→ **优先解读**，不跑交底 Step 1–8。
- **禁止**因写交底或读专利自动进入政策简报、审查答复、申请文件或案卷。申请文件必须用户点名并给出交底目录；缺 schema / 线稿 / 交底书则停，引导先补交底。内容争议不阻塞主文件。
- **案卷**必须用户点名（交底申请一起做 / 从零出交底和申请 / 一条龙 / 帮写交底再出申请 / 按清单改 / 会稿 / `/patent-docket`）。点名后 `Read` `skills/patent-docket/SKILL.md`；由案卷再 `Read` 交底或申请入口。调度申请视为已点名申请文件，仍须有交底目录。只写交底、或已有交底只出四件套 → 不要进案卷。
- 交底 Step 5 查新优先用智慧芽 MCP `patsnap-search.patsnap_search` 做语义检索（覆盖专利+文献）；无 MCP 时降级到交底包 `cnipa_epub_search.py`（一词一页）。按发明人/申请人等做著录检索时用检索包（`core-patents.search_patents` MCP 或 CNITA 降级），两者不要混用。
- **全景分析**（`/patent-landscape`）和 **FTO**（`/patent-fto`）须用户显式触发，不因写交底/读专利/检索而自动进入。两者仅支持 MCP 模式（无 CNIPA 降级），MCP 不可用时直接告知用户。全景分析用 `patent-landscape` MCP 服务；FTO 用 `patsnap-ip-searching` + `novelty-search-lite` + `core-patents` MCP 服务。
- 解读（patent-reader）在 MCP 可用时于第 1.5 步自动富化同族/引证/法律状态；MCP 不可用时跳过，不影响主链路。
=======
## 路由判定表

「**须点名**」= 只有用户明确说出该行触发词才进入，**禁止**由写交底或读专利自动进入。

| 用户这样说 | 前置门禁（不满足就停下说明） | 进入 | 明确不要做 |
|------------|------------------------------|------|------------|
| 专利挖掘、交底书、查新、实用新型、外观设计；`/patent-disclosure`、`/交底书` | 无 | 交底包 | 查新只用交底包轻量检索（一词一页、公布模式每页 10 条），不调检索包 |
| 专利布局、专利围栏、族树、保护型1+N、做围栏 | 首篇交底已定稿（用户点名可强开）；须分解 → 突围 → 矩阵 → 立项说明，立项校验写入 `专利布局.md` | **交底包旁路** `prompts/fence/` | 不进专利地图；未确认立项说明**不得**分件写多篇交底 |
| 申请文件、申请底稿、申报材料；`/申请底稿`、`/patent-apply` — **须点名** | **须指定交底目录**；缺 schema / 线稿 / 交底书则停，引导先补交底 | 申请文件包 | 仅缺材料则终止；内容争议写入问题清单、**不**阻塞主文件；「交付后请确认」须摘要该清单；改已有产出则另存 |
| 交底申请一起做、从零出交底和申请、一条龙、帮写交底再出申请、按清单改、会稿、案卷；`/patent-docket` — **须点名** | 状态写 `outputs/docket/`；清单缺口最多来回三轮，缺事实问人、不编 | 案卷包（再由它 `Read` 交底或申请入口） | 只写交底、或已有交底只出四件套 → **不要**进案卷；案卷自身不写交底/申请正文 |
| 按著录字段查公布公告、个人公开清单、以图或权要生成检索式；`/patent-search` | 无 | 检索包 | 普通多条件**不要**默认翻完全部分页；结果不得冒充交底查新 |
| 读专利、给出公开号或 PDF 且目标是「读懂」；`/patent-read`、`/读专利` | 无 | 解读包（**优先**） | 不跑交底 Step 1–8 |
| 专利地图、案例地图；`/专利地图`、`/patent-map` — **须点名** | 需已有解读入库的 vault | 专利地图包 | 不因读专利自动进入 |
| 审查意见、OA、案例入库、实务书；`/oa` — **须点名** | 库薄时先引导入库/蒸馏 | 审查答复包 | — |
| 政策简报、政策雷达；`/政策简报`、`/patent-brief`、`/patent-exam-policy`；「技能进化 / `/patent-evolve`」同一入口 — **须点名** | 无 | 政策简报包 | 仍**先出简报**；改技能只是旁路，无点名不改交底包以外的目录 |

## 通则

- **工具归属**：填表、线稿、CAD、公式、Word 出图在交底包 `prompts/` 与 `tools/`；解读填表用解读包 `prompts/fill_*`；过 WAF 的 `browser.py`、Markdown 转 Word 的 `md_to_docx.py` **各包自带副本**。
- **禁止跨包调用**其他子技能的 `tools/`。需要同一能力就用本包副本。
- **调度视同点名**：由案卷调度申请文件视为已点名申请文件，**仍须**有交底目录。
- **交付末块**：各子技能交付回复末块标题统一为 **交付后请确认**；跨包口令以上表为准，交底**不得**在此节把申请、案卷、专利地图列为下一步。检索与专利地图可不设此节。

## 能力自述（用户问「你能做什么 / 还能做什么」时）

按**能力总览**复述 8 项，每项一句并给出触发说法；说明**申请文件 / 案卷 / 专利地图 / 审查答复 / 政策简报须点名**才会进入。不要只报交底，也**不要**改用交底的「交付后请确认」代替本节（该节仍受上述限制）。
>>>>>>> upstream/main

## 目录

```
SKILL.md                         # 本文件：子技能路由入口
skills/patent-disclosure/        # 交底（含填表/线稿/CAD/公式/docx；围栏旁路）
skills/patent-application/       # 申请文件四件套（须显式；须指定交底目录）
skills/patent-docket/            # 案卷：交底到申请一趟串起来（须显式）
skills/patent-search/            # 著录检索
skills/patent-reader/            # 解读
skills/patent-map/               # 专利地图（须显式；读 vault，本机页面）
skills/patent-oa/                # 审查答复
skills/patent-exam-policy/        # 政策简报（技能进化为旁路）
skills/patent-landscape/           # 全景分析（须显式；仅 MCP）
skills/patent-fto/                 # FTO 自由实施分析（须显式；仅 MCP）
```

## 环境与约定

- **默认语言**：面向用户的检索清单、交底书、申请文件、案卷 TRACKER、解读和审查答复用简体中文；脚本机读前缀与 JSON 字段名保持稳定。
<<<<<<< HEAD
- **脚本判读（尤其 Windows）**：stderr 有字 **不等于** 失败。以 **退出码 0** 和机读前缀为准：`EPUB_HITS_JSON:` / `EPUB_SEARCH_MD:` / `EPUB_SEARCH_JSON:` / `EPUB_CLASS_HINT:`、`PROBE:` / `BROWSER:`、`MERMAID:` / `DOCX:`、`APPLICATION_GATE:` / `APPLICATION_CLAIMS:` / `APPLICATION_NUMERALS:`、`DOCKET_DIR:` / `DOCKET_YAML:` / `DOCKET_OK:` / `DOCKET_ERROR:`。PowerShell 可能把 stderr 标成 `NativeCommandError`；**禁止**因此重跑安装或把查新降级 WebSearch。**MCP 模式下无需脚本判读**——MCP 工具直接返回结构化 JSON。
- **专利类型**：未显式指定时交底**默认发明**。
- **脚本路径**：相对本技能仓库根（本文件所在目录）。整仓：`python skills/patent-disclosure/tools/…`。当前工作区不是本仓库时，把技能安装目录接到命令前面。单独拷走某一子包时，该包内用 `python tools/…`。不要写厂商环境变量。
- **用户产出**：写在当前工作区 `outputs/`（解读 `outputs/patent_reader/`，检索 `outputs/patent-search/`，政策 `outputs/exam-policy/`，审查答复 `outputs/oa/`，申请文件 `outputs/patent-application/`，案卷 `outputs/docket/`，全景分析 `outputs/patent-landscape/`，FTO `outputs/patent-fto/`），不要写到技能安装目录或 `tmp/`。调用脚本时 cwd 用工作区根；`-o` / `-w` 用上述相对路径。
=======
- **专利类型**：未显式指定时交底**默认发明**。
- **脚本路径**：相对本技能仓库根（本文件所在目录）。整仓：`python skills/patent-disclosure/tools/…`。当前工作区不是本仓库时，把技能安装目录接到命令前面。单独拷走某一子包时，该包内用 `python tools/…`。不要写厂商环境变量。
- **用户产出**：写在当前工作区 `outputs/`（解读 `outputs/patent_reader/`，检索 `outputs/patent-search/`，政策 `outputs/exam-policy/`，审查答复 `outputs/oa/`，申请文件 `outputs/patent-application/`，案卷 `outputs/docket/`，交底围栏 `outputs/{案件}/fence/`），不要写到技能安装目录或 `tmp/`。调用脚本时 cwd 用工作区根；`-o` / `-w` 用上述相对路径。
>>>>>>> upstream/main

## 执行前核对

```
□ 已 Read 对应 skills/*/SKILL.md，未把本文件当交底/申请底稿/案卷/检索/解读/专利地图正文
□ 交底查新未调用 patent-search
□ 著录检索未用交底一词一页结果冒充清单
<<<<<<< HEAD
□ 政策简报 / 审查答复 / 申请文件 / 案卷仅在显式触发时进入
□ 全景分析 / FTO 仅在显式触发时进入；MCP 不可用时不降级
=======
□ 政策简报 / 审查答复 / 申请文件 / 案卷 / 专利地图仅在显式触发时进入
>>>>>>> upstream/main
□ 申请文件已指定交底目录；门禁未过未开写
□ 案卷未写交底/申请正文；派工只 Read 对方 SKILL.md
□ 未跨包调用其他子技能的 tools/
□ 围栏未确认立项说明未批量写多篇；未把布局说明当成专利地图
□ 未把政策简报当成改技能；无点名未改交底包以外的目录
□ 交付回复末块标题为「交付后请确认」；交底该节未把申请、案卷、地图列为下一步
```
