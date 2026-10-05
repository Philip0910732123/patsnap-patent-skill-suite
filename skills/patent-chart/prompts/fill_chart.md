# 填格

只在已有原文窗口里写。窗口来自：对照专利的 `description_paragraphs.json`、产品页 URL（intake 的 `right[].url`）、产品/标准用户文件、covers 旁路摘录、intake 粘贴正文。有产品链接先抓页面再填格；禁止只凭产品名称编结构。

对照结果的主文件是 **Excel**。写法对齐 Solve Charts / Patlytics / Andy：四列、跨列同色、书面对应说明、可点出处、总览可进入明细。禁止只填「结构对应」那种玩具格。

## 强度（写入 `strength`，导出显示「很强 / 中等 / 偏弱 / 未见」）

| 值 | 何时 | 导出 |
|----|------|------|
| 强 | 原文几乎覆盖该限定，且有链接或段号 | 很强 |
| 中 | 手段对应但术语或限定不完全对齐 | 中等 |
| 弱 | 仅可能同义或片段相关 | 偏弱 |
| 无 | 未见；单元格留空 | 未见 |

术语不对齐不得标「强」。无摘录不得标「强」。

## 跨列同色

同一概念共用一个 `id`（H1、H2…）。权要一边的字面和对照一边的字面**可以不同**（如下行资源 vs CORESET），颜色仍相同。Excel 图例用语加粗并着高亮色。

写在 payload 顶层 `highlights`，某一格还可追加自己的 `highlights`。

```json
{"id": "H1", "label": "冷却腔", "claim": "冷却腔", "evidence": "冷却空腔"}
```

## 对应说明（`analysis`）

必须分三块书面语，禁止口语（如「对上了」「没写到」「下钻」）和单句标签。导出时按项换行，写成一段也可以：

1. **对应**：权要哪一限定对应摘录哪一句
2. **差别**：术语不同、更宽/更窄、或未记载的点
3. **依据**：段号或文件名。禁止「应当无效」「构成侵权」「不具备新颖性」

另填：

- `covered`：已对应的短语列表
- `missing`：未记载的短语列表
- `cite`：给人看的出处，如 `对比文件1 · 说明书 [0021]`
- `quote`：写入**完整段落**（给明细页核对）。对照表导出时按对应短语截取窗口并着色；同一对照对象截取结果相同则显示「同 Fk · [段号]」，悬停批注可看摘录、不跳转。
- `source_url` / `desc_para`：可点开或可核段号

## 场景页（导出自动生成）

同一套 `cells`。场景页由导出脚本按 `scene` 生成，不另写一份表。

| `scene` | Excel 加页 | 内容 |
|---------|------------|------|
| `invalidity` | 路径备忘 | 哪份对照覆盖哪条 Fk、未覆盖、最强、可点出处 |
| `fto` | 风险清单 | 覆盖强弱 → 风险 高/中/低/未见；高标「须人审」 |
| `infringement` | 证据缺口 | 弱/未见排前；`missing` 写成待补证据 |
| `oa` | 驳回映射 | 驳回点 × Fk × D；弱/未见排前。不写入意见陈述正文 |
| `sep` / `patentability` | （不加） | 只用四页矩阵 |

## 写入 payload 后导出

字段：`scene`、`left`、`features`、`columns`、`cells`、`highlights`；审查答复另加 `rejections`（`item`、`statute`、`feature_ids`、`column_ids`、`examiner_view`）。

```bash
python skills/patent-chart/tools/emit_chart.py \
  --json outputs/patent-chart/{案件}/{会话}/_payload.json \
  --into outputs/patent-chart/{案件}/{会话}
```

看 `CHART_XLSX:`（给人传）以及 `CHART_JSON:`（再导出）。场景页由脚本按 `scene` 追加。对话只给 xlsx 路径。
