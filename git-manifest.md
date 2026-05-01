# Git Repository Manifest -- ピアニカ・オルガン リポジトリコンテンツ台帳

最終更新: 2026-05-01

> このファイルはGitリポジトリの内容台帳である。
> 本リポジトリはGit側のSSOT (Single Source of Truth) として機能する。
> Project Knowledge (PK) は本プロジェクトでは利用しない。

> **来歴 (2026-04-29)**: 本リポジトリは `KishowFujiwara/EngineringKnowlege` の
> `decoded/pianika-organ/` から独立リポジトリとして分離 (29コミット時点)。
> 詳細は `journals/02-physics/2026-04/0429_opus_gpt_inspection_powerflow_v2.md` を参照。

---

## プロジェクト概要

**目的**: 足踏みペダル式リードオルガン (家庭の教会用) の試作

**設計原理**:
- ピアニカ (鍵盤ハーモニカ) のフリーリードを音源とする
- 桐の共鳴箱で音色を Trompette 8' に近づける
- パイプオルガンと違い「演奏中に呼気を一定保持できる」足踏みペダル方式

**現在地 (v3 + 2段構造パラダイム)**:
- フリーリード37音 (チューニングはCAHAYA 32鍵 = P-32D相当に整合)
- 桐空気箱 (スパン60mm) + 共鳴箱の2段構造
- 効率 Γ ≈ 41% (理論値、要実機検証)

**実験プラットフォーム**:
- CAHAYA CY0341-1 (鍵盤ハーモニカ32鍵、底面ABSを木材化して共鳴箱化)

---

## リポジトリ構成 (3章 + 章別ジャーナル)

```
pianica-organ/
├── 01-specification/   楽器仕様 (CAHAYA, P-32D, 鈴木 W-37C)
├── 02-physics/         物理検証 (22経路, パワーフロー, 因果機構, 楽器比較)
├── 03-design/          設計成果物 (v1/v2/v3/spinet)
├── journals/           設計プロセスの章別時系列記録
│   ├── 01-specification/
│   ├── 02-physics/
│   ├── 03-design/
│   └── cross/
├── README.md
├── git-manifest.md     (本ファイル)
└── github_workflow.md  (運用手順書)
```

---

## 楽器仕様台帳 (01-specification/)

| ディレクトリ | 楽器 | 役割 | 主要ファイル |
|---|---|---|---|
| cahaya/ | CAHAYA CY0341-1 | 実験プラットフォーム (32鍵) | README.md, MEASUREMENT_GUIDE.md, images/ |
| yamaha-p32d/ | Yamaha Pianica P-32D | 設計参照 (37鍵, 0423仕様の起点) | README.md, images/ |
| suzuki/ | 鈴木 W-37C | 構造比較参照 | README.md, images/ |

| ファイル | 内容 | コミット |
|---|---|---|
| 01-specification/cahaya/README.md | CAHAYA仕様まとめ | (移管時) |
| 01-specification/cahaya/MEASUREMENT_GUIDE.md | L5実測ガイド + 倍音計測 (0430o) | 8e1e556 |
| 01-specification/cahaya/images/*.jpg | 分解写真12枚 | 8bea55d, 6425f92 |
| 01-specification/yamaha-p32d/README.md | P-32D仕様 | (移管時) |
| 01-specification/yamaha-p32d/images/*.jpg | P-32D写真12枚 | (移管時) |
| 01-specification/suzuki/README.md | W-37C構造比較 | (移管時) |
| 01-specification/suzuki/images/*.jpg | 公式断面図など3枚 | f1604d1 |

---

## 物理検証台帳 (02-physics/)

| サブディレクトリ | テーマ | 状態 |
|---|---|---|
| 22-paths/ | 22振動伝達経路の包括解析 + システム同定 | [完了] |
| powerflow/ | パワーフロー数理モデル v2.0 | [完了] |
| causal-mechanism/ | v3因果機構解析 (0430g B系3層分解) | [完了] |
| materials/ | 桐/ABS/フェルト等の音響特性 + Gamma理論 | [完了] |
| helmholtz/ | ヘルムホルツ共鳴 + ポート設計 | [部分撤回] T0/T1パラダイムへ |
| three-instruments/ | ギター/ピアノ/バイオリン共鳴構造比較 | [完了] |

| 主要ドキュメント | 内容 | 行数 |
|---|---|---|
| 22-paths/path_comprehensive_analysis.md | 22経路の包括音響分析 (5軸マトリクス) | 約530行 |
| 22-paths/pianica_22paths_acoustic_analysis.md | 22経路解析 (KaTeX レンダリング想定) | 約400行 |
| 22-paths/pianica_chinese_style_paths_analysis.md | 中華式（一体成形）ピアニカ経路解析 (22 -> 17経路、ABS壁直接接触5現象、17経路の個別構造検証 v1.2) | 約1000行 |
| powerflow/pianica_powerflow_v2.md | パワーフロー v2.0 (1000Pa統一) | 約1000行 |
| causal-mechanism/pianica_v3_causal_mechanism.md | v3因果機構 (BN1復元、3.4%効率) | 約400行 |
| materials/air_chamber_material_physics.md | 材料物理 + Gamma計算 | 約300行 |
| three-instruments/three_instruments_comparison.md | 3楽器共鳴構造比較 | 約350行 |

---

## 設計成果物台帳 (03-design/)

| ディレクトリ | バージョン | 設計コンセプト | ステータス |
|---|---|---|---|
| v1/ | v1.0 (2026-04-23) | 37個別トランペット型ラッパ + 家具級1m + 足踏みペダル | 撤回 (壁面放射99%判明) |
| v2/ | v2.0 (2026-04-23) | 楔形ホーン1本 + 縦潰し折り返し | 撤回 (ホーン不要) |
| v3/ | v3.0 (2026-04-30) | 共鳴箱14.2L + ボディ放射 + ピアニカ原理駆動 | **採用** |
| spinet/ | (撤回案) | スピネット形状 + 2重箱 + バスレフ | 撤回 (B系3層分解で物理誤り発覚) |

### v3 主要ドキュメント

| ファイル | 内容 | コミット |
|---|---|---|
| 03-design/v3/design-spec-v3.md | v3 設計仕様書 (主体) | 3743c7a, ffdb6ad |
| 03-design/v3/design-document-v3.docx | v3 完全文書 | 3743c7a |
| 03-design/v3/figures/F1-F4_*.svg | 三面図 + ブレース配置等 4図 | 3743c7a |
| 03-design/v3/figures/chapel_organ_v3/*.svg | チャペル用筐体図 | 3743c7a |
| 03-design/v3/scripts/verification/verify_bijection_v3.py | リポジトリ全体 全単射検証 | 8b23075 |
| 03-design/v3/scripts/verification/verify_bijection_by_dir_v2.py | ディレクトリ別 全単射検証 | b9ec57b |
| 03-design/v3/scripts/verification/fix_journal_refs.py | ジャーナル間相互参照の章別マッピング | cc2921e |

### v3 残課題 (最重要)

- [ ] **2段構造への全面改訂** (0501b で宣告、0501h 時点で未着手)
  - 旧: 14.2L共鳴箱 + 桐1.5mm板で共振
  - 新: 桐空気箱(スパン60mm) + 共鳴箱の2段構造
- [ ] phase1_physics.py / phase1b_caseC.py / phase2_dimensions.py の保存
- [ ] L5実測の実施

---

## ジャーナル台帳 (journals/)

ジャーナルは章別に分類 (0501g セッションで再構成)。

### 章別 件数

| 章 | 件数 | 主成果物 |
|---|---|---|
| 01-specification | 3本 | CAHAYA分解、計測ガイド |
| 02-physics | 12本 | 22経路、Gamma、T0/T1 |
| 03-design | 10本 | 設計仕様書 v1/v2/v3 改訂 |
| cross | 7本 | リポジトリ整備、検証、メタ |
| **合計** | **32本** | |

### 01-specification ジャーナル (3本)

| ファイル | 日付 | 内容 |
|---|---|---|
| 01-specification/2026-04/0430k_opus_cahaya_disassembly_32keys_p32d_alignment.md | 2026-04-30 | CAHAYA分解 - 32鍵=P-32D相当の確定 |
| 01-specification/2026-04/0430o_opus_harmonic_measurement_integration.md | 2026-04-30 | 倍音計測のL5実測ガイド組込 |
| 01-specification/2026-04/0430q_opus_gasket_observation_correction.md | 2026-04-30 | ガスケット問題訂正 (認知バイアス3段階記録) |

### 02-physics ジャーナル (12本)

| ファイル | 日付 | 内容 |
|---|---|---|
| 02-physics/2026-04/0428_opus_22paths_comprehensive.md | 2026-04-28 | 22経路 包括音響分析 |
| 02-physics/2026-04/0428_opus_22paths_sysid_verification.md | 2026-04-28 | 22経路検証 + システム同定 |
| 02-physics/2026-04/0428_opus_acoustic_report.md | 2026-04-28 | 22経路包括分析の正式レポート |
| 02-physics/2026-04/0428_opus_sysid_22paths.md | 2026-04-28 | 22経路システム同定 |
| 02-physics/2026-04/0429_opus_gpt_inspection_powerflow_v2.md | 2026-04-29 | GPT検査 + パワーフロー v2.0 |
| 02-physics/2026-04/0430_opus_reed_material_physics_windchest.md | 2026-04-30 | リード材料物理 + 気室設計 |
| 02-physics/2026-04/0430b_opus_soundboard_design_cahaya_experiment.md | 2026-04-30 | L5d共鳴板 + Gamma理論 |
| 02-physics/2026-04/0430d_opus_free_reed_acoustics_fundamentals_BN1_verification.md | 2026-04-30 | フリーリード音響基礎 + BN1検証 |
| 02-physics/2026-04/0430e_opus_22path_photo_verification_BN2_redefinition.md | 2026-04-30 | 22経路写真検証 + BN2再定義 |
| 02-physics/2026-04/0430f_opus_three_instruments_resonance_physics.md | 2026-04-30 | 3楽器共鳴構造比較 |
| 02-physics/2026-04/0430g_opus_B_system_decomposition_dfc79ff_verification.md | 2026-04-30 | B系3層分解 + dfc79ff撤回 |
| 02-physics/2026-04/0430h_opus_T0T1_paradigm_energy_scale_classification.md | 2026-04-30 | T0/T1パラダイム |

### 03-design ジャーナル (10本)

| ファイル | 日付 | 内容 |
|---|---|---|
| 03-design/2026-04/0423_opus_pianika_organ_design.md | 2026-04-23 | プロジェクト原点: 設計仕様書v1.0起草 |
| 03-design/2026-04/0423_opus_pianika_organ_v2_wedge_horn.md | 2026-04-23 | v2 楔形ホーン |
| 03-design/2026-04/0428_opus_pianika_design_verification.md | 2026-04-28 | v1/v2 設計検証 |
| 03-design/2026-04/0430c_opus_resonance_box_final_design.md | 2026-04-30 | 共鳴箱設計到達 (三角形は後に撤回) |
| 03-design/2026-04/0430i_opus_flat_top_guitar_chapel_organ_redesign.md | 2026-04-30 | フラットトップギター3DOF + 教会用回帰 |
| 03-design/2026-04/0430j_opus_chassis_design_finalized_caseC.md | 2026-04-30 | v3筐体確定 (案C 14.2L) |
| 03-design/2026-04/0430n_opus_distance_overview_L5_guide_L6_research.md | 2026-04-30 | 製作距離 + L6結合詳細 |
| 03-design/2026-04/0430p_opus_design_targets_per_component.md | 2026-04-30 | 部位設計目標 (P1-P12 x 3層) |
| 03-design/2026-05/0501a_opus_cahaya_damping_experiment_side_material_pde.md | 2026-05-01 | 側面材料 + PDE数理モデル |
| 03-design/2026-05/0501b_opus_two_stage_structure_paradigm_shift.md | 2026-05-01 | 2段構造パラダイム転換 |

### cross ジャーナル (7本)

| ファイル | 日付 | 内容 |
|---|---|---|
| cross/2026-04/0430l_opus_repository_three_chapter_restructure.md | 2026-04-30 | リポジトリ3章構造化 |
| cross/2026-04/0430m_opus_observation_after_repository_restructure.md | 2026-04-30 | 整理後の観測 |
| cross/2026-05/0501c_opus_full_commit_verification_39commits.md | 2026-05-01 | 全39コミット検証 |
| cross/2026-05/0501d_opus_bijection_verification_journals_files.md | 2026-05-01 | 全単射写像検証 |
| cross/2026-05/0501e_opus_bijection_verification_by_directory.md | 2026-05-01 | ディレクトリ別検証 |
| cross/2026-05/0501f_opus_journal_directory_independence.md | 2026-05-01 | Journal独立化 |
| cross/2026-05/0501g_opus_journals_chapter_classification.md | 2026-05-01 | ジャーナル章別再分類 |

---

## コミット履歴台帳 (主要コミット)

### Phase 0: 起点 (2件)

| コミット | 日付 | カテゴリ | 内容 |
|---|---|---|---|
| 1d25e94 | 2026-04-28 | [meta] | Initial commit |
| be25f6f | 2026-04-28 | [migrate] | EngineringKnowlege/decoded/pianika-organ/ から分離独立 (80ファイル) |

### Phase 1: 22経路解析 〜 パワーフロー v2.0 (4件)

| コミット | 日付 | カテゴリ | 内容 |
|---|---|---|---|
| 9a78a27 | 2026-04-28 | [physics] | 22経路包括解析 + システム同定 (1891行) |
| 6755051 | 2026-04-28 | [physics] | パワーフロー数理モデル v2.0 (1006行) |
| d22da23 | 2026-04-29 | [fix] | 1500Pa->1000Pa統一 (GPT5.4指摘) |
| 171612c | 2026-04-29 | [journal] | GPT食品検査ジャーナル |

### Phase 2: リード 〜 共鳴板 (4件)

| コミット | 日付 | カテゴリ | 内容 |
|---|---|---|---|
| 381e888 | 2026-04-30 | [physics] | リード設計37音 + 気室2層 |
| 6ba756a | 2026-04-30 | [physics] | L5d共鳴板 + Gamma理論 + CAHAYA改造実験 |
| 192f0db | 2026-04-30 | [design] | 共鳴箱への到達 (三角形を最終形と主張、後に撤回) |
| b68969c | 2026-04-30 | [physics] | 音響基礎論 + BN1外部検証 |

### Phase 3-4: 写真検証 〜 v3起点 (11件)

| コミット | 日付 | カテゴリ | 内容 |
|---|---|---|---|
| 8bea55d | 2026-04-30 | [observe] | 鍵盤ハーモニカ分解写真12枚 |
| 39115d0 | 2026-04-30 | [physics] | エネルギー経路モデル v2.0 (BN2再定義) |
| 636eab4 | 2026-04-30 | [physics] | 構造C (ABS-桐 T=97%) |
| 252c584 | 2026-04-30 | [physics] | 断面構造図 SVG + DOCX |
| 0ac63b4 | 2026-04-30 | [physics] | v2.1 (パッキン位置誤訂正) |
| ba489c9 | 2026-04-30 | [fix] | v2.2 差し戻し |
| f1604d1 | 2026-04-30 | [observe] | 鈴木公式断面図など |
| 6783ffa | 2026-04-30 | [physics] | 3楽器共鳴構造比較 |
| f27e34d | 2026-04-30 | [design] | v3最終確定 (2部品構造) |
| c4dfd57 | 2026-04-30 | [physics] | v3因果機構 (35%、後に訂正) |
| 965e678 | 2026-04-30 | [fix] | 因果機構v2 (35% -> 3.4%、BN1復元) |

### Phase 5-6: 構造解析 〜 撤回 〜 方針再定義 (8件)

| コミット | 日付 | カテゴリ | 内容 |
|---|---|---|---|
| 00a31e5 | 2026-04-30 | [physics] | 魂柱構造 (Gamma=1.8) |
| 013b473 | 2026-04-30 | [physics] | 桐0.7mm+リブ60mm 効率7.3% (後に撤回) |
| e34cb07 | 2026-04-30 | [physics] | ヘルムホルツ +4.3dB |
| 0e9591c | 2026-04-30 | [design] | 設計C 音響弁 |
| dfc79ff | 2026-04-30 | [design] | スピネット形状 (10.3%、後に撤回) |
| c3ea9de | 2026-04-30 | [revoke] | dfc79ff撤回: B系3層分解 (83.5%反射発見) |
| 3a82b07 | 2026-04-30 | [physics] | T0/T1パラダイムシフト |
| 91e96af | 2026-04-30 | [refocus] | フラットトップギター3DOF + 教会用回帰 |

### Phase 7-8: v3筐体確定 〜 結合詳細 (8件)

| コミット | 日付 | カテゴリ | 内容 |
|---|---|---|---|
| 3743c7a | 2026-04-30 | [design] | v3筐体確定 (案C 14.2L) + design-spec-v3.md (336行) |
| 6425f92 | 2026-04-30 | [observe-fix] | CAHAYA分解: 37鍵 -> 32鍵, F6 -> C6 |
| a0a0a0d | 2026-04-30 | [refactor] | リポジトリ3章構造化 (01/02/03) |
| b57c95d | 2026-04-30 | [journal] | 整理後の観測 |
| 8e1e556 | 2026-04-30 | [design] | L0-L9 + L5実測 + L6結合詳細 |
| 63566d3 | 2026-04-30 | [design] | 倍音計測のL5組込 |
| b160976 | 2026-04-30 | [design] | L6-0 部位設計目標 (P1-P12 x 3層) |
| c63a1e5 | 2026-04-30 | [observe-fix] | ガスケット観測ミス3段階訂正 (認知バイアス記録) |

### Phase 9: パラダイム転換 (2件)

| コミット | 日付 | カテゴリ | 内容 |
|---|---|---|---|
| ffdb6ad | 2026-05-01 | [design] | 側面材料アルミ + PDE数理モデル / design-spec-v3 178行更新 |
| 9d68acc | 2026-05-01 | [paradigm] | 桐空気箱+共鳴箱 2段構造発見 / Γ計算が最初から正解 |

### Phase 10: メタ検証 + 構造化 (本セッション群、本日)

| コミット | 日付 | カテゴリ | 内容 |
|---|---|---|---|
| dd70a3a | 2026-05-01 | [verify] | 全39コミット検証 (0501c) |
| 8b23075 | 2026-05-01 | [verify] | 全単射写像検証 53.5% (0501d) |
| b9ec57b | 2026-05-01 | [verify] | ディレクトリ別検証 (0501e) |
| e6a6eef | 2026-05-01 | [restructure] | Journal独立化 (0501f) |
| cc2921e | 2026-05-01 | [restructure] | ジャーナル章別分類 (0501g) |
| (本commit) | 2026-05-01 | [meta] | git-manifest + github_workflow 導入 (0501h) |

---

## 統計

| 項目 | 数量 |
|---|---|
| 総コミット数 | 44 (本commit含めず) |
| プロジェクト期間 | 4日間 (2026-04-28 〜 2026-05-01) |
| 全ファイル数 | 178 (本commit含めず、md/svg/png/jpg/docx/html/json/py) |
| 章別 (01-specification) | 31 |
| 章別 (02-physics) | 56 |
| 章別 (03-design) | 58 |
| journals/ | 33 |
| ジャーナル本数 | 32本 (本セッション含めず) |
| 設計バージョン | v1, v2, v3, spinet (4世代、現役はv3) |
| 撤回された設計 | v1, v2, spinet, 三角形共鳴箱、効率連鎖モデル |

---

## 検証台帳

### 実施済み検証

| ジャーナル | 検証内容 | 結果 |
|---|---|---|
| cross/2026-05/0501c | 全39コミット物理的妥当性 | [PASS] (訂正サイクル4件はすべて健全) |
| cross/2026-05/0501d | 全ジャーナル悉皆性 (リポジトリ全体全単射) | [PARTIAL] 数学的53.5% / 実質92% |
| cross/2026-05/0501e | ディレクトリ別全単射 | [PASS] 23ディレクトリ完璧, 4ディレクトリ要対処 |

### 検証スクリプト

```
03-design/v3/scripts/verification/
├── verify_bijection_v3.py            (リポジトリ全体)
├── verify_bijection_by_dir_v2.py     (ディレクトリ別)
├── fix_journal_refs.py               (ジャーナル間参照修正)
├── bijection_verification_v3.json    (結果)
└── bijection_by_dir_v2.json          (結果)
```

### 残存する整合性課題 (0501e から継続)

| ディレクトリ | 課題 | 件数 |
|---|---|---|
| 03-design/v1 | 削除済み章への幽霊参照 | 6件 |
| 03-design/v3/scripts | 計算スクリプト未保存 | 3件 (phase1_physics.py 等) |
| 03-design/v2/figures-v2 | 撤回設計の孤児図 (READMEで救済可能) | 4件 |
