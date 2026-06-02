# manufacturing_ai_scenario — 製造業AIエージェント導入シミュレーション

## 概要

製造業の企業がAIエージェントを導入したとき、仕事の仕方がどう変わるかを示す**架空シナリオ集**。

同一の案件（ボスポラスTBMモータ焼損）を4つのPhaseで処理し、情報の流れ・判断の速度・見落としの有無がどう変化するかを比較する。ClaudeFactoryの製品として、シナリオの量産・品質管理を行う。

シナリオ内の各発言には`formalized`フィールドがあり、自然言語→述語論理（NL→FOL）の変換実例を含む。シナリオ制作とロビンソン導出パイプラインの素材制作は表裏一体。

**核心原則: エージェントが判断すること＝0件。エージェントが提示すること＝全部。**

## 位置づけ

本シナリオ集はClaudeFactory（`KishowFujiwara/ClaudeFactory`）の**最終目標のイメージ**である。

ClaudeFactoryは「生素材を受入→加工→検査→出荷する知識処理パイプライン」を設計・実装する工場プロジェクトであり、その工場が完成したとき何が実現されるかを示しているのが本シナリオ集である。具体的には:

- **Phase 1**（PCのみ、エージェントなし、20日遅延）= 工場稼働前の世界
- **Phase 4**（同時並列エージェント、リアルタイム情報交差）= 工場稼働後の世界

ClaudeFactoryの実装が完成したとき、Phase 3 `detail/` の議事録7本を入力として与えればPhase 4の挙動が再現される、というのが受入条件である。本シナリオ集は単なる製品サンプルではなく、Factoryの**要件定義書かつ受入テスト仕様書**として機能する。

## 来歴

ClaudeHouseの`projects/02_robinson_resolution/`から移行（2026-05-19）。元はロビンソン導出パイプラインの素材として作成されたが、ClaudeFactoryではシナリオ制作が独立した目的。パラモジュレーション関連（paramod_trace系）はClaudeHouse側に残留。

## シミュレーション題材

**ボスポラスTBMモータ焼損案件** — 架空シナリオ

トルコ・ボスポラス海峡トンネル掘削中のTBM駆動モータが焼損。代替発電エンジンの緊急需要が発生。船舶用エンジンメーカーがこの案件を追うかどうか、16日間のシミュレーション。5部門（営業・開発・設計・製造・研究）の視点で情報が交差する。

## Phase定義

| Phase | 名称 | 特徴 |
|---|---|---|
| 1 | PCのみ | エージェントなし。メール・電話の属人化世界。20日経過で競合に先行される |
| 2 | 人間会議のみ | 定例会議で情報共有。週次の壁で10日遅延 |
| 3 | 逐次エージェント | 部門別にエージェントが情報整理。週次detail記録あり。遅延が圧縮される |
| 4 | 同時並列エージェント | 全部門のエージェントが同時稼働。リアルタイムで情報が交差 |

## 文書一覧

| ファイル | 内容 | 行数 |
|---|---|---|
| **phase1_pc_only/** | | |
| simulation.md | Phase 1シミュレーション本体 | 543 |
| **phase2_human_meetings/** | | |
| simulation.md | Phase 2シミュレーション本体 | 571 |
| **phase3_sequential/** | | |
| simulation.md | Phase 3シミュレーション本体（全体） | 1181 |
| detail/week-1_discovery.md | 週-1: 案件発見 | 408 |
| detail/week0d1_sales_meeting.md | 週0日目1: 営業会議 | 369 |
| detail/week0d2-3_standalone.md | 週0日目2-3: 単独作業 | 224 |
| detail/week1d1_dev_meeting.md | 週1日目1: 開発会議 | 250 |
| detail/week1d2_design_meeting.md | 週1日目2: 設計会議 | 213 |
| detail/week1d3_mfg_meeting.md | 週1日目3: 製造会議 | 222 |
| detail/week1d4_research_meeting.md | 週1日目4: 研究会議 | 279 |
| detail/week2_planning.md | 週2: 計画策定 | 323 |
| **phase4_simultaneous/** | | |
| reasoning.md | Phase 4シミュレーション＋設計思考 | 795 |
| **context_design/** | | |
| applied_case_bosphorus.md | ボスポラス案件の適用事例詳細 | 795 |
| context_building.md | 議事録からのコンテキスト構築設計 | 664 |
| factory_adaptation.md | ClaudeFactory適応設計（5部門議事録パイプライン） | 299 |
| **verification/** | | |
| bijection_verification.md | Phase間の全単射検証結果 | 273 |

## 読む順番

1. この`README.md` — Phase定義を把握
2. `phase1_pc_only/simulation.md` — エージェントなしの世界
3. `phase3_sequential/simulation.md` → `detail/` — Phase 3が最も詳細
4. `phase4_simultaneous/reasoning.md` — 最終形の設計思考
5. `context_design/factory_adaptation.md` — ClaudeFactoryとの接続

## ステータス

シナリオ Phase 1〜4 完成。context_design整理中。今後の拡張は別題材（別業種・別案件）でのシナリオ量産。

## 関連

- `projects/ClaudeFactory/` — 工場設計文書。このシナリオが工場の「製品」になる
- `projects/integrated_agent_design/` — 統合エージェント設計。シナリオの設計根拠
- **ClaudeHouse `projects/02_robinson_resolution/`** — ロビンソン導出パイプライン（①-D段階）。本シナリオ内の`formalized`フィールド（NL→FOL変換）がパイプラインの入力素材になる。シナリオ制作と導出パイプラインは表裏一体
