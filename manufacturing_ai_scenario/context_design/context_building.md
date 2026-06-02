# 製造業議事録からのコンテキスト構築

**作成**: 2026-05-09 / Sonnet 4.6
**信頼度**: [DRV]+[EST] — 構造導出。実データ検証は未実施

---

## 0. 何をやるか

議事録は「会議の記録」ではない。**各部門が蓄積してきた判断・知識・前提の断片**が自然言語で流れ出てくる場所。

これを部門ごとに:

```
議事録（自然言語）
  → タクソノミー（分類体系）
  → オントロジー（概念間の関係構造）
  → 述語論理・様相論理（形式化）
  → データ蓄積（出所を明らかにして）
```

蓄積されたものが**コンテキスト**になる。コンテキストがあるから次の会議での判断が構造化できる。コンテキストがないと毎回ゼロから議論する。

矛盾検出はコンテキストの上で走る応用の一つに過ぎない。

---

## 1. 営業のコンテキスト

### 1.1 タクソノミー

営業が議事録で語ることの分類体系。

```
営業知識
├── 顧客
│   ├── 顧客プロファイル（業種、規模、取引履歴）
│   ├── 顧客要求（明示的要求 / 暗黙的期待）
│   ├── 顧客クレーム（事象 / 原因推定 / 対応）
│   └── 顧客評価（満足度 / 継続意向 / リスク）
├── 市場
│   ├── 競合動向（製品 / 価格 / 技術）
│   ├── 市場トレンド（需要変動 / 規制変更）
│   └── 商機（案件 / 見積 / 受注確度）
├── 契約
│   ├── 仕様合意（図面承認 / 検収条件）
│   ├── 納期（約束 / 実績 / 遅延リスク）
│   └── 価格（見積根拠 / 値引き判断 / 原価意識）
└── 営業判断
    ├── 受注判断（やるべきか / やれるか / やりたいか）
    ├── 優先順位（顧客重要度 / 案件規模 / 戦略性）
    └── リスク判断（与信 / 技術リスク / 納期リスク）
├── ビジネスインテリジェンス
│   ├── 外部イベント検出（事故 / 規制変更 / 競合動向）
│   ├── 商機評価（ニーズ×自社製品の適合度）
│   └── 製品マッチング（スペック照合 / 適合スコア）
└── アクション追跡
    ├── タスク（担当 / 期限 / 進捗）
    ├── クリティカルパス（律速項目の識別）
    └── 完了判定（何をもって完了とするか）
```

### 1.2 オントロジー

営業知識の概念間関係。

```
Customer --[requires]--> Specification
Customer --[complains_about]--> Product
Specification --[constrains]--> DesignParameter
Complaint --[originates_from]--> ProcessDefect | DesignDefect | UsageError
Order --[has_deadline]--> DeliveryDate
Order --[has_price]--> QuotedPrice
QuotedPrice --[must_cover]--> ManufacturingCost
Competitor --[offers]--> AlternativeProduct
AlternativeProduct --[threatens]--> Order
Event --[creates]--> Opportunity
Opportunity --[matched_by]--> Product --[with]--> MatchScore
Opportunity --[competed_by]--> Competitor
Action --[responds_to]--> Opportunity | Complaint | Requirement
```

### 1.3 述語論理化

議事録の営業発言を論理式に変換する際の述語体系。

```
Requires(customer, spec, date_stated)
  — 顧客customerが仕様specを要求した。date_statedに発言

ExpectsImplicitly(customer, property)
  — 顧客customerが暗黙に期待している性質property
  — ★これは[DRV]。営業の推測が入る。出所タグ必須

Complained(customer, product, defect, date_occurred)
  — 顧客customerが製品productの不具合defectを報告した

Quoted(order, price, basis)
  — 注文orderに対しprice（根拠basis）で見積もった

DeliveryPromised(order, date)
  — 注文orderの納期をdateと約束した

Event(type, source, date)
  — 外部イベントtypeを情報源sourceからdateに検出した
  — ★営業がビジネスインテリジェンスとして捕捉する事象。[OBS]

Opportunity(need, specification, source)
  — 商機: needに対しspecificationの案件がsourceから発生
  — ★Eventから導出されることが多い。Event→Opportunityの連鎖を記録

Competitors(opportunity, competitor_list, source)
  — 商機opportunityに対する競合リストcompetitor_list。情報源source
  — ★競合情報の鮮度に注意。出所と日付で信頼度が変わる

MatchScore(product, opportunity, criteria, score)
  — 自社製品productが商機opportunityに対しcriteria基準でscore適合度
  — score ∈ {high, medium_high, medium, low}
  — ★これは営業の評価=[DRV]。設計・開発の検証でFeasibleに昇格

Action(task, assigned_to, deadline, status)
  — 営業タスクtaskを担当assigned_toが期限deadlineまでに実施。進捗status
  — status ∈ {planned, started, completed, overdue}
  — ★CriticalPathの識別に使用。overdue検出はエージェントの自律監視対象
```

### 1.4 様相論理化

営業知識に固有の様相。

```
□Requires(customerB, thickness≥3mm)
  — 顧客Bの肉厚3mm以上要求は必然（仕様書記載）

◇LoseOrder(orderX, if_delay > 2weeks)
  — 2週間超の遅延なら失注の可能性がある
  — ★これは◇（可能性）。□（必然）にしない

¬□ExpectsImplicitly(customerC, surface_finish_Ra0.8)
  — 顧客Cが面粗度Ra0.8を暗黙に期待しているかは不確定
```

### 1.5 蓄積と出所

```
{
  source: "営業",
  speaker: "田中",
  meeting: "2026-05-09 営業定例",
  claim: "顧客Bは肉厚3mm以上を要求",
  formalized: "□Requires(customerB, thickness≥3mm)",
  evidence: "仕様書Rev.3 §4.2",
  trust: "[FACT]",
  date_entered: "2026-05-09"
}
```

**出所が営業であることが消えてはならない。** 設計が参照するとき「これは営業が2026-05-09に言ったことで、根拠は仕様書Rev.3」と追跡できなければ、コンテキストとして機能しない。

---

## 2. 開発のコンテキスト

### 2.1 タクソノミー

```
開発知識
├── 製品企画
│   ├── コンセプト（何を / 誰に / なぜ）
│   ├── 要求仕様（機能要求 / 非機能要求 / 制約条件）
│   └── フィージビリティ（技術的可否 / コスト的可否 / 日程的可否）
├── 技術選定
│   ├── 採用技術（素材 / 工法 / センサ / ソフト）
│   ├── 採用根拠（実験データ / 文献 / 経験 / 推測）
│   └── 代替案（検討済み / 却下理由）
├── DR（デザインレビュー）
│   ├── DR段階（DR0構想 / DR1基本 / DR2詳細 / DR3量産移行）
│   ├── 判定結果（通過 / 条件付き / 差し戻し）
│   └── 残課題（未解決項目 / 担当 / 期限）
└── 開発判断
    ├── Go/NoGo（前提条件付きGoの前提は何か）
    ├── トレードオフ（性能vs.コスト / 重量vs.強度）
    └── リスク受容（どのリスクを受け入れたか / 誰が判断したか）
├── 認証・規制
│   ├── 適用規格（船級 / 防爆 / 環境 / 安全）
│   ├── 認証パス（申請→審査→取得の工程）
│   └── 認証状態（未申請 / 審査中 / 取得済 / 期限切れ）
└── アクション追跡
    ├── タスク（担当 / 期限 / 進捗）
    ├── クリティカルパス（律速項目の識別）
    └── 完了判定（何をもって完了とするか）
```

### 2.2 オントロジー

```
Concept --[decomposed_into]--> RequirementSpec
RequirementSpec --[constrained_by]--> Regulation | CustomerSpec | CostTarget
Technology --[selected_for]--> RequirementSpec
Technology --[evidenced_by]--> ExperimentData | Literature | Experience
DR --[judges]--> Technology + RequirementSpec
DR --[produces]--> Approval | ConditionalApproval | Rejection
ConditionalApproval --[has_condition]--> OpenItem
OpenItem --[assigned_to]--> Department + Person + Deadline
TradeOff --[sacrifices]--> Property_A --[for]--> Property_B
RiskAcceptance --[decided_by]--> Person --[at]--> DR
CertificationScheme --[required_for]--> Application
CertificationScheme --[grants]--> Compliance --[enables]--> Market_Access
Action --[tracks]--> OpenItem | CertificationScheme | TradeOff
```

### 2.3 述語論理化

```
Selected(technology, for_requirement, at_DR, with_evidence)
  — 技術technologyを要求for_requirementのためにDR段階at_DRで採用。根拠with_evidence

Feasible(technology, aspect, confidence)
  — 技術technologyはaspect面でconfidence（確度）のfeasibility
  — confidence ∈ {verified[FACT], estimated[EST], assumed[EST]}
  — ★「できそう」はestimated。「できる」はverified。混同禁止

ConditionalApproval(DR_id, condition_list)
  — DR_idは条件付き通過。条件はcondition_list
  — condition_listの各項目が完了するまで[FACT]にならない

TradeOff(sacrificed_property, gained_property, decided_by, at_DR)
  — 何を犠牲にして何を得たか。誰がどのDRで判断したか

CertificationRequired(application, scheme, status)
  — 用途applicationに認証schemeが必要。取得状態status
  — status ∈ {unknown, investigating, applied, granted, expired}
  — ★認証パスは開発が主導。設計のApplicableと対で使う

Action(task, assigned_to, deadline, status)
  — 開発タスクtaskを担当assigned_toが期限deadlineまでに実施。進捗status
  — status ∈ {planned, started, completed, overdue}
```

### 2.4 様相論理化

```
◇Feasible(materialA, machining) ∧ ¬□Feasible(materialA, machining)
  — 素材Aの加工は可能かもしれないが、確実ではない
  — ★開発が最もフグ級になる箇所。◇を□に昇格させるにはMeas(x)が要る

□(ConditionalApproval(DR2, [machining_test]) → ¬Approved(DR2) until Completed(machining_test))
  — 条件付き承認は、条件完了まで承認ではない
  — ★「DR通過」が「全面承認」に化けるお好み焼き偽装の防止
```

### 2.5 蓄積と出所

```
{
  source: "開発",
  speaker: "鈴木",
  meeting: "2026-05-09 DR2",
  claim: "素材A採用決定（強度15%向上）",
  formalized: "Selected(materialA, strength_requirement, DR2, experiment_n5)",
  evidence: "社内試験報告書 TEST-2026-042（n=5）",
  trust: "[OBS]",
  conditions: ["製造フィージビリティ未確認"],
  date_entered: "2026-05-09"
}
```

---

## 3. 設計のコンテキスト

### 3.1 タクソノミー

```
設計知識
├── 設計仕様
│   ├── 機能仕様（性能値 / 精度 / 寿命）
│   ├── 形状仕様（寸法 / 公差 / 幾何公差）
│   ├── 材料仕様（材質 / 熱処理 / 表面処理）
│   └── 制約条件（法規制 / 規格 / 顧客固有要求）
├── 設計根拠
│   ├── 強度計算（荷重条件 / 安全率 / 計算書番号）
│   ├── FMEA（故障モード / 影響度 / 検出度 / RPN）
│   ├── 過去トラブル事例（類似設計 / 失敗知識）
│   └── 経験則（★[DRV]止まり。根拠の明示が必要）
├── 設計変更
│   ├── 変更内容（Before / After / 図番 / Rev.）
│   ├── 変更理由（顧客要求 / コスト / 品質 / 製造性）
│   ├── 影響範囲（関連部品 / 関連工程 / 関連顧客）
│   └── 変更承認（誰が / いつ / どのDRで）
└── 設計ナレッジ（←①-A 畑村が直結）
    ├── 機能展開（畑村「実際の設計」）
    ├── 設計のチェック観点（見落としやすい項目）
    ├── 材料選定の判断木
    └── 公差設計の勘所
├── 規格適用
│   ├── 適用規格の識別（船級 / 防爆 / 振動 / 環境）
│   ├── 適用/非適用の根拠（用途による判断）
│   └── 規格間の競合（複数規格の要求が矛盾する場合）
└── アクション追跡
    ├── タスク（担当 / 期限 / 進捗）
    ├── クリティカルパス（律速項目の識別）
    └── 完了判定（何をもって完了とするか）
```

### 3.2 オントロジー

```
DesignSpec --[derived_from]--> RequirementSpec
DesignSpec --[justified_by]--> StrengthCalc | FMEA | PastFailure | Experience
DesignChange --[modifies]--> DesignSpec
DesignChange --[triggered_by]--> CustomerRequirement | CostReduction | QualityIssue
DesignChange --[impacts]--> RelatedPart + RelatedProcess + RelatedCustomer
DesignChange --[approved_at]--> DR
Tolerance --[determined_by]--> FunctionalRequirement + ManufacturingCapability
FMEA_Item --[has_RPN]--> RPN_Value
FMEA_Item --[mitigated_by]--> DesignCountermeasure
PastFailure --[similar_to]--> CurrentDesign
PastFailure --[teaches]--> DesignPrinciple  ← ①-A 畑村知識
Standard --[applicable_to]--> Application --[constrains]--> DesignSpec
Action --[tracks]--> DesignChange | FMEA_Item | Standard
```

### 3.3 述語論理化

```
Specified(parameter, value, tolerance, basis, rev)
  — パラメータparameterを値value±toleranceに設定。根拠basis、図面Rev. rev

Changed(parameter, from_value, to_value, reason, approved_by, at_DR)
  — パラメータを変更。理由、承認者、DR段階を全部記録

Justified(design_decision, by_calculation | by_FMEA | by_experience | by_assumption)
  — 設計判断の根拠の種類
  — by_calculation → [FACT]
  — by_FMEA → [OBS]+[DRV]
  — by_experience → [DRV]  ★畑村知識で補強可能
  — by_assumption → [EST]  ★フグ級

ImpactedBy(design_change, related_parts[], related_processes[], related_customers[])
  — 設計変更の影響範囲。空リストは「影響なし」ではなく「未調査」

Applicable(standard, to_application)
  — 規格standardが用途to_applicationに適用される
  — ★適用判断は設計が行う。¬Applicable は「適用不要」の根拠を要する
  — 開発のCertificationRequiredと対: 規格の識別は設計、認証パスの推進は開発

Action(task, assigned_to, deadline, status)
  — 設計タスクtaskを担当assigned_toが期限deadlineまでに実施。進捗status
  — status ∈ {planned, started, completed, overdue}
```

### 3.4 様相論理化

```
□(Specified(wallThickness, 2mm, ±0.1, calc_report_CR042, Rev.3)
    → Justified(wallThickness_2mm, by_calculation))
  — 肉厚2mmは計算書CR042に基づく。□（必然的に正当化される）

◇(ImpactedBy(change_wallThickness, [partB, partC], [process_machining], [customerB])
    ∧ ¬Investigated(impact_on_customerB))
  — 肉厚変更が顧客Bに影響する可能性があるが、まだ調査していない
  — ★この◇が放置されると後工程で事故になる
```

### 3.5 蓄積と出所

```
{
  source: "設計",
  speaker: "高橋",
  meeting: "2026-05-09 設計検討会",
  claim: "肉厚2mmに変更。強度計算で安全率2.0以上を確認",
  formalized: "Changed(wallThickness, 3mm, 2mm, cost_reduction, 高橋, DR2)",
  evidence: "計算書CR042",
  trust: "[FACT]",
  unchecked: ["顧客Bの要求との整合", "加工工程への影響"],
  date_entered: "2026-05-09"
}
```

**`unchecked`フィールドが重要。** 「まだ確認していないこと」を明示的に記録する。これがないと「確認済み」と区別できない。

---

## 4. 製造のコンテキスト

### 4.1 タクソノミー

```
製造知識
├── 工程
│   ├── 工程定義（工順 / 設備 / 治工具 / 条件）
│   ├── 工程能力（Cp/Cpk / 実績データ）
│   ├── 4M変更（Man / Machine / Material / Method）
│   └── 工程異常（事象 / 頻度 / 影響 / 暫定対策）
├── 品質
│   ├── 検査結果（測定値 / 合否 / ロット / 日時）
│   ├── 不具合（事象 / 原因区分 / 流出経路）
│   ├── 是正処置（暫定 / 恒久 / 水平展開 / 効果確認）
│   └── 工程内不良率（推移 / 目標 / 乖離）
├── 設備
│   ├── 稼働状況（稼働率 / 故障履歴 / 保全計画）
│   ├── 加工条件（回転数 / 送り / 切込 / 温度）
│   └── 設備制約（加工可能範囲 / 精度限界）
└── 製造判断
    ├── 特別採用（規格外だが使用可と判断。根拠と承認者）
    ├── 工程変更（変更前後の条件 / 検証結果）
    └── 生産計画（負荷 / 納期 / 優先順位）
```

### 4.2 オントロジー

```
Process --[produces]--> Product --[inspected_by]--> Inspection
Inspection --[yields]--> MeasuredValue --[compared_to]--> Specification
MeasuredValue --[out_of_spec]--> Defect
Defect --[caused_by]--> RootCause ∈ {Man, Machine, Material, Method}
RootCause --[identified_by]--> Analysis ∈ {FTA, WhyWhy, Statistical}
CorrectiveAction --[addresses]--> RootCause
CorrectiveAction --[verified_by]--> EffectivenessCheck
4MChange --[requires]--> Validation --[before]--> ProductionResume
Equipment --[has_capability]--> ProcessCapability(Cpk)
ProcessCapability --[limits]--> AchievableTolerance
```

### 4.3 述語論理化

```
Measured(part_id, parameter, value, date, operator)
  — 部品part_idのパラメータparameterを測定。値value、日時、測定者
  — ★製造データは最もMeas(x)に近い。[FACT]の供給源

OutOfSpec(part_id, parameter, measured, specified, deviation)
  — 規格外。測定値と規格値の乖離

RootCauseIdentified(defect_id, cause, method_of_analysis, confidence)
  — 不具合defect_idの根本原因。分析方法と確度
  — confidence = verified[FACT] | probable[DRV] | suspected[EST]
  — ★「たぶん治具」は[EST]。「治具摩耗量0.3mm確認」は[FACT]

SpecialAcceptance(part_id, deviation, justification, approved_by, date)
  — 特別採用。規格外だが使用可。根拠と承認者を記録
  — ★特別採用の蓄積は設計へのフィードバック源

Action(task, assigned_to, deadline, status)
  — 製造タスクtaskを担当assigned_toが期限deadlineまでに実施。進捗status
  — status ∈ {planned, started, completed, overdue}
  — ★製造のActionは進捗率（%）を伴うことが多い。Measured()と組み合わせて使用
```

### 4.4 様相論理化

```
□(OutOfSpec(part, param, measured, spec, dev) → RequiresDisposition(part))
  — 規格外品は必ず処置判定が必要

◇(RootCause(defect042, jig_wear) ∧ confidence=suspected)
  — 治具摩耗が原因かもしれない（可能性）
  — ★□にするには治具の測定データが要る

¬□(CorrectiveAction(jig_repair) → ¬Recurrence(defect042))
  — 治具修理で再発防止になるとは限らない
  — ★恒久対策の有効性は[EST]から始まる
```

### 4.5 蓄積と出所

```
{
  source: "製造",
  speaker: "山本",
  meeting: "2026-05-09 品質会議",
  claim: "ロットXXXで寸法NG 3/100個。治具摩耗が疑われる",
  formalized: "OutOfSpec(lotXXX, dim_A, 2.15mm, 2.00±0.05mm, +0.10mm)
               ∧ ◇RootCause(lotXXX_defect, jig_wear)",
  evidence: "検査成績書 QC-2026-0509",
  trust: "[FACT](測定値) + [EST](原因推定)",
  date_entered: "2026-05-09"
}
```

---

## 5. 研究のコンテキスト

### 5.1 タクソノミー

```
研究知識
├── 実験
│   ├── 実験条件（変数 / 水準 / 試料数 / 方法）
│   ├── 実験結果（測定値 / 統計量 / 有意差）
│   ├── 考察（結果の解釈 / 仮説との整合 / 異常値）
│   └── 再現性（追試 / 条件変動の影響）
├── 文献
│   ├── 論文引用（著者 / 年 / ジャーナル / 主張）
│   ├── 特許（出願人 / 請求項 / 抵触リスク）
│   └── 技術動向（学会 / 展示会 / 競合特許）
├── 仮説
│   ├── 作業仮説（検証対象 / 検証方法 / 検証基準）
│   ├── 仮説の状態（未検証 / 支持 / 反証 / 保留）
│   └── 仮説間の関係（前提→帰結 / 競合仮説 / 補完仮説）
└── 技術移転
    ├── 開発への適用可否（条件 / 制約 / スケール差）
    ├── 製造への適用可否（量産条件 / 設備要件）
    └── 残課題（実験室→量産のギャップ）
```

### 5.2 オントロジー

```
Hypothesis --[tested_by]--> Experiment
Experiment --[produces]--> Result
Result --[supports | refutes | is_inconclusive_for]--> Hypothesis
Hypothesis --[based_on]--> Literature | PriorExperiment | Theory
Hypothesis --[competes_with]--> AlternativeHypothesis
Technology --[at_TRL]--> TRL_Level(1-9)
Technology --[transferable_to]--> Development --[if]--> TransferCondition
TransferCondition --[includes]--> ScaleUp | EquipmentAvailability | CostFeasibility
Patent --[conflicts_with]--> Technology
Literature --[claims]--> TheoreticalPrediction
TheoreticalPrediction --[verified_by | contradicted_by]--> ExperimentResult
```

### 5.3 述語論理化

```
Tested(hypothesis, experiment_id, result, n, statistical_significance)
  — 仮説hypothesisを実験experiment_idで検証。結果、n数、統計的有意性

Supports(result, hypothesis, confidence_interval)
  — 結果resultが仮説hypothesisを支持。信頼区間付き

AtTRL(technology, level, evidence)
  — 技術technologyのTRLレベル。根拠evidence
  — TRL1-3: [EST]〜[DRV]（研究段階）
  — TRL4-6: [DRV]〜[OBS]（開発段階）
  — TRL7-9: [OBS]〜[FACT]（実証・量産段階）

TransferableIf(technology, condition_list, assessed_by)
  — 技術technologyはcondition_listが満たされれば移転可能。評価者assessed_by
  — ★condition_listの各項目が[EST]なら、移転判断全体も[EST]

Action(task, assigned_to, deadline, status)
  — 研究タスクtaskを担当assigned_toが期限deadlineまでに実施。進捗status
  — status ∈ {planned, started, completed, overdue}
  — ★研究のActionはlimitations解消（追試・条件変動試験等）と紐づくことが多い
```

### 5.4 様相論理化

```
◇(Supports(experiment042_result, hypothesis_materialA_strength, CI95))
  ∧ ¬□(Supports(...))
  — n=5で95%信頼区間で支持。しかし必然的に支持されるとは言えない
  — ★研究成果の信頼度は常に◇。□にするには再現性確認が要る

□(AtTRL(materialA, 3) → ¬ReadyForProduction(materialA))
  — TRL3の技術は量産準備完了ではない。必然的に

◇(TransferableIf(materialA, [scaleup_test, equipment_mod], 鈴木)
  ∧ ¬Completed(scaleup_test))
  — 移転可能かもしれないが、スケールアップ試験がまだ
```

### 5.5 蓄積と出所

```
{
  source: "研究",
  speaker: "佐藤",
  meeting: "2026-05-09 研究進捗会",
  claim: "素材Aで引張強度15%向上（n=5, p<0.05）",
  formalized: "Tested(hyp_materialA_strength, EXP042, +15%, n=5, p<0.05)
               ∧ AtTRL(materialA, 3, EXP042)",
  evidence: "社内試験報告書 TEST-2026-042",
  trust: "[OBS]",
  limitations: ["n=5（小標本）", "単一ロット", "加速劣化未実施"],
  date_entered: "2026-05-09"
}
```

**`limitations`フィールドが研究では必須。** 「何を確認していないか」が技術移転時の地雷になる。

---

## 6. 部門間のコンテキスト接続

蓄積された5部門のコンテキストは、独立ではなく接続する。

```
営業.Requires(customerB, thickness≥3mm)
  ↕ 突合
設計.Specified(wallThickness, 2mm)
  ↕ 根拠追跡
設計.Justified(wallThickness_2mm, by_calculation, CR042)
  ↕ 影響確認
製造.ProcessCapability(machining_dim, Cpk=1.8)
  ↕ 技術供給
研究.AtTRL(materialA, 3) → 開発.Selected(materialA, DR2)
  ↕ 前提確認
製造.¬Established(MachiningCondition(materialA))
```

この接続を**出所を保持したまま**辿れることがコンテキストの本質。誰が言ったか、何を根拠に言ったか、いつ言ったか、どの信頼度で言ったかが全部追跡できる。

### 6.1 部門間コミュニケーション述語

部門間の情報開示と提案は、出所追跡の観点から特に重要。どの情報が誰に開示されたか（されていないか）は、判断の前提条件を左右する。

```
Disclosed(information, from_department, to_party, at_time)
  — 情報informationがfrom_departmentからto_partyにat_timeに開示された
  — ★¬Disclosed(info, dept, party, _) は「まだ開示していない」= 情報非対称が存在
  — 部門間矛盾の主因は情報非対称。この述語で追跡可能にする

Proposal(content, from_department, to_party, limitations_included)
  — 提案contentをfrom_departmentからto_partyに提示。制約条件の記載有無
  — limitations_included ∈ {true, false, partial}
  — ★limitations_included=false は「制約条件を隠した提案」= フグ級リスク
  — 営業が顧客に制約なし提案を出すと、設計・製造が後で事故になる
```

---

## 7. 4プロジェクトとの関係（深い方）

| プロジェクト | 浅い理解 | 深い理解 |
|---|---|---|
| ①-A 工学知識RAG | 設計DRの支援ツール | **設計タクソノミーとオントロジーの種**。畑村の設計方法論がDesignKnowledgeノードの構造を与える。RAGは初期オントロジーの構築手段 |
| ①-B 形式論理学 | Resolution Workerの前提 | **全部門のコンテキストを論理式として蓄積可能にする基盤**。タクソノミーを述語に、オントロジーを関係に、判断を命題に変換する方法論 |
| ② ロビンソン導出 | 矛盾検出ツール | **蓄積されたコンテキスト上で走る推論エンジン**。矛盾検出は一応用。含意検証（AならばBが導かれるか）、前提欠落検出（Bを結論するのにCが欠けている）も可能 |
| ③ 論理哲学論考検査 | GPT出力の品質検査 | **コンテキスト蓄積の品質保証方法論**。[EST]が[FACT]に化けないこと、出所が消えないこと、◇が□に昇格しないことを検査する。藤原テスト = コンテキスト汚染防止 |

---

## 8. Factory内での位置づけ（改訂）

```
議事録（5部門）
  │
  ▼
受入係: タクソノミーに従って分類、信頼度タグ付与、出所記録
  │          ↑ ①-A/①-B がタクソノミーとオントロジーの種を供給
  ▼
製造係: オントロジーに従って概念間関係を構築、Source Card/Domain Note化
  │          ↑ 部門間のリンクを張る
  ▼
蓄積: Postgres（引くもの）+ Git/MD（読むもの）に出所付きで格納
  │          ↑ ここがコンテキスト
  ▼
推論: ②Resolution Workerが蓄積コンテキスト上で導出を実行
  │          ↑ 矛盾・含意・前提欠落を検出
  ▼
検査係: ③の方法論でコンテキストの品質を検査
             ↑ [EST]→[FACT]偽装、出所消失、◇→□昇格を検出
```

矛盾検出はこのパイプラインの**出口の一つ**に過ぎない。本体は**コンテキストの構築と蓄積**。

---

**信頼度**: [DRV]+[EST]
