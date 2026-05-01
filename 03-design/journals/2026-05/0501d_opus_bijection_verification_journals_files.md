# 2026-05-01d: 全ジャーナル・全ファイルの悉皆性 - 全単射写像検証

**セッション目的**: ユーザ指示「すべてのジャーナルとすべてのジャーナルに記されているすべてのMDファイルなどの悉皆性を全単射写像検証せよ」に基づく、リポジトリ全体の参照網羅性の集合論的検証。

**検証対象**:
- リポジトリ `KishowFujiwara/pianica-organ` 全170ファイル (md/svg/png/jpg/docx/html/json/py)
- うちジャーナル 28件、README 7件、その他 135件

**検証日時**: 2026-05-01

---

## 1. 全単射写像の定義

```
集合 J = {すべてのジャーナル} (28件)
集合 R = {すべてのリポジトリ内ファイル} (170件)
集合 N = R \ J = {ジャーナル以外のファイル} (142件)

写像 f : J -> 2^R (各ジャーナルから到達可能なファイル集合)

[単射性] 検証: ジャーナルが参照するパスは全て R の元に解決されるか?
            (= 幽霊参照 ghost references がゼロか)
[全射性] 検証: N の全要素は f の値域 (推移閉包) に含まれるか?
            (= 孤児ファイル orphan files がゼロか)

全単射が成立 <=> 幽霊参照ゼロ かつ 孤児ファイルゼロ
```

---

## 2. 検証結果サマリー

```
+----------------------------------+----------+----------+
| 項目                              | 件数      | 状態      |
+----------------------------------+----------+----------+
| 全リポジトリファイル               | 170      | 母集団    |
| ジャーナル                         | 28       | 起点集合  |
| README                             | 7        | 補助起点  |
| その他                             | 135      | 検証対象  |
+----------------------------------+----------+----------+
| 推移閉包により到達可能              | 127/170  | 74.7%   |
| 真の孤児 (どこからも参照なし)       | 43       | [NG]    |
| 幽霊参照 (ユニーク)                 | 36       | [NG]    |
+----------------------------------+----------+----------+
| 全単射成立?                        | NO       | 部分的   |
+----------------------------------+----------+----------+
```

**結論**: 全単射は **不成立**。74.7% のファイルがジャーナル/READMEから到達可能だが、残り25.3% (43件) は孤立、加えて36件の幽霊参照(リンク切れ)が存在する。

---

## 3. 単射性検証 (幽霊参照 36件)

ジャーナルが参照しているのに、リポジトリに実在しないファイル。**カテゴリ別に分類**：

### A. README の glob/概略表現 (5件) [PASS_意図的]

READMEがファイル群をglob風に列挙しているが、個別ファイル名と一致しない。これは**意図的な記述で実害なし**。

```
+-----------------------------------------+----------------------------+
| 参照                                      | 参照元                      |
+-----------------------------------------+----------------------------+
| ../../03-design/journals/2026-04/0430b_*.md | 01-specification/yamaha-p32d/README.md |
| ../03-design/journals/2026-04/0428_*.md   | 02-physics/README.md       |
| ../03-design/journals/2026-04/0430b_*.md  | 01-specification/README.md |
| ../03-design/journals/2026-04/0430f_*.md  | 02-physics/README.md       |
| ../03-design/journals/2026-04/0430k_*.md  | 01-specification/README.md |
+-----------------------------------------+----------------------------+
```

### B. 削除されたファイルへの参照 (12件) [NG_要対処]

過去のジャーナル/仕様書が **削除済みファイル** を参照している。

```
+--------------------------------+--------------------------------+----------+
| 削除されたファイル                | 参照元                          | 影響度   |
+--------------------------------+--------------------------------+----------+
| bell-shape-necessity.md         | 03-design/v1/design-spec-v1.md | 中       |
| free-reed-physics.md            | 03-design/v1/design-spec-v1.md | 中       |
| phase0-single-reed.md           | 03-design/v1/design-spec-v1.md | 中       |
| phase1-12key.md                 | 03-design/v1/design-spec-v1.md | 中       |
| webster-equation.md             | 03-design/v1/design-spec-v1.md | 中       |
| reed_design_37notes_G1_G4.docx  | 0430.md                        | 低       |
| reed_design_G1_G4.docx          | 0430.md                        | 低       |
| reed_material_design.docx       | 0430.md                        | 低       |
| pianica_organ_technical_report.docx | 0430.md                    | 低       |
| pianica_organ_repo_overview.svg | 0430.md                        | 低       |
| pianica_22paths_acoustic_analysis.html | 0428_sysid_verification | 低       |
| pianica_22paths_system_identification.html | 0428_sysid_verification | 低    |
| v3_soundboard_design.svg        | 0430b                          | 低       |
+--------------------------------+--------------------------------+----------+
```

design-spec-v1.md が参照する 5件 (bell-shape, free-reed-physics, phase0/1, webster) は **v1 設計書の重要章だった可能性** がある。ただし v1 自体が撤回設計のため、再生成は不要。

### C. 計算スクリプト未保存 (4件) [NG_要対処]

```
+----------------------------------------+--------------------------------+
| 参照されているスクリプト                  | 参照元                          |
+----------------------------------------+--------------------------------+
| chapel_organ_design/phase1_physics.py    | 0430j_chassis, design-spec-v3  |
| phase1b_caseC.py                         | 0430j_chassis, design-spec-v3  |
| phase2_dimensions.py                     | 0430j_chassis, design-spec-v3  |
| /home/claude/sysid/identification_results.json | 02-physics/22-paths/sysid_22paths.py |
+----------------------------------------+--------------------------------+
```

これは **0430j で v3 筐体確定時に使われた計算スクリプトが未保存** ということ。Claudeセッションでは存在したが永続化されなかった。今後の検証可能性のため**再構築または明示的削除が望ましい**。

### D. リポジトリ外パス (2件) [INFO]

```
/home/claude/sysid/identification_results.json   <- 上記Cと重複
/mnt/user-data/outputs/design-spec-v3.html        <- 0501a (一時アクセス用パス)
```

セッション環境の一時パス。リポジトリ外のため検証不能。

### E. リネーム/集約された参照 (5件) [NG_要対処]

```
+----------------------------------+--------------------------------+----------------------------+
| 参照                              | 参照元                          | 実体                       |
+----------------------------------+--------------------------------+----------------------------+
| ../v3/figures/chapel_organ_v3/F1-F4.svg | 0430p                    | F1〜F4の4ファイル別々     |
| figures/chapel_organ_v3/F1-F4.svg | 0430j                          | 同上                       |
| figures-v2/*.png, figures-v2/*.svg | 0423_v2_wedge_horn            | 19ファイルのglob          |
| free_reed_acoustics_fundamentals.svg | 0430d, 0430e                | basename不一致で未解決   |
| impedance_mismatch_causal_chain.svg | 0430d, 0430e                 | basename不一致で未解決   |
+----------------------------------+--------------------------------+----------------------------+
```

「F1-F4.svg」は実体が `F1_three_view_drawing.svg`, `F2_brace_layout.svg` 等の4ファイル別々。**まとめ表記**による不一致。

### F. 旧リポジトリ/別プロジェクト参照 (4件) [INFO]

```
+----------------------------------+--------------------------------+
| 参照                              | 由来                            |
+----------------------------------+--------------------------------+
| git-manifest.md                  | 旧 EngineringKnowlege/ のファイル|
| overtourism/.../chatgpt_o3...md  | 別プロジェクトの参考引用         |
| v2.md, v3.md                     | 0430l 再構造化中の仮称名         |
| ルートREADME.md                   | 0430l (日本語の説明文中の言及)   |
+----------------------------------+--------------------------------+
```

別文脈の参照。実害なし、ただし整合性のため0430lなどでパスを正式化すべき。

---

## 4. 全射性検証 (孤児ファイル 43件)

リポジトリ内に存在するが、ジャーナル/READMEから到達不能なファイル。**全43件が完全孤立** (リポジトリ内のいかなるMD/HTMLにもbasenameが言及されていない)。

### A. v2 撤回設計の図版 (27件)

```
03-design/v2/figures-v2/  19件 (PNG 13 + SVG 6)
03-design/v2/figures/      8件 (SVG 8)

撤回理由: v1/v2 はリード下流にホーンを置く構成、v3 でボディ放射型に転換 (Phase 6 撤回)
保管理由: 設計史の記録として残置
```

**全孤児ファイル一覧**:
```
figures-v2/:
  final_3horn_flat_with_flatten_fold.png
  folded_horn_geometry_constraints.png
  free_reed_oscillator_mechanism.png
  horizontal_wedge_horn_plan_view.png/svg
  horn_geometry_webster_comparison.png
  one_wedge_three_folded.png
  piano_cabinet_37bell_layout.png/svg
  s_shape_wedge_creature_integrated.png/svg
  three_stage_coupling_block_diagram.png
  three_wedges_zigzag.png
  u_vs_creature_midrange_comparison.png
  user_sketch_transcription.png
  wedge_creature_hybrid_structure.png
  wedge_horn_uturn_confirmed.png/svg
  wedge_walls_completed.png

figures/:
  bass_horn_length_relationship.svg
  bell_vs_cylinder_vs_conical.svg
  horn_cutoff_physics.svg
  pianika_horn_design.svg
  pianika_organ_enclosure_final.svg
  upstream_vs_downstream_horn.svg
  v_horn_vs_column_baffle_13axes.svg
  valve_removal_horn_analysis.svg
```

### B. 02-physics 撤回/未参照の図 (13件)

```
+----------------------------------+----------+--------------------------------+
| ディレクトリ                       | 件数      | 該当                            |
+----------------------------------+----------+--------------------------------+
| 02-physics/22-paths/figures/      | 4        | melodica_cross_section_energy_paths.svg |
|                                   |          | phase_a_observation_map.svg    |
|                                   |          | pianika_analysis.svg           |
|                                   |          | pianika_physical_observation.svg |
| 02-physics/causal-mechanism/figures/ | 3     | melodica_cross_section_v2_1_corrected.svg |
|                                   |          | melodica_cross_section_v2_2.svg |
|                                   |          | melodica_cross_section_v3_final.svg |
| 02-physics/helmholtz/figures/     | 5        | column_baffle_reed_structure.svg |
|                                   |          | column_role_answer.svg         |
|                                   |          | pianika_valve_role.svg         |
|                                   |          | recorder_pressure_vs_suction.svg |
|                                   |          | suction_type_reed_structure.svg |
| 02-physics/three-instruments/figures/ | 1    | three_source_spectrum_comparison.svg |
+----------------------------------+----------+--------------------------------+
```

### C. v1 撤回設計の図 (1件)

```
03-design/v1/figures/pianika_37trumpets_design.svg
```

### D. 検証JSON (2件、自己生成)

```
./bijection_verification.json
./bijection_verification_v2.json
```

本検証セッションで生成されたもの。`bijection_verification_v3.json` は最新で、これも放置すれば孤児になる。**本ジャーナルから明示的に参照することで救済**。

---

## 5. 参照されないジャーナル 15件 [INFO]

ジャーナル間相互参照を見ると、**他のジャーナル/MDから参照されない**ジャーナルが15件:

```
+--------------------------------+----------+----------------------------+
| ジャーナル                      | 状態      | 補足                        |
+--------------------------------+----------+----------------------------+
| 0423_pianika_organ_v2_wedge_horn | [PASS]  | v2 スナップショット、参照不要 |
| 0428_22paths_comprehensive      | [PASS]   | 起点ジャーナル               |
| 0428_22paths_sysid_verification | [PASS]   | 起点                        |
| 0428_acoustic_report            | [PASS]   | 起点                        |
| 0428_pianika_design_verification | [PASS]  | 起点                        |
| 0428_sysid_22paths              | [PASS]   | 起点                        |
| 0429_gpt_inspection_powerflow_v2 | [PASS]  | 起点                        |
| 0430_reed_material_physics      | [PASS]   | 起点                        |
| 0430c_resonance_box_final_design | [INFO]  | 「最終形」を主張したが撤回された|
| 0430d_free_reed_acoustics_BN1   | [INFO]   | 0430e で発展、後続から非参照 |
| 0430e_22path_photo_BN2          | [INFO]   | 0430g, 0430h の前提だが参照無|
| 0430f_three_instruments         | [INFO]   | 0430h, 0430i の前提だが参照無|
| 0430g_B_system_dfc79ff          | [INFO]   | dfc79ff撤回の起点、要参照化 |
| 0501b_two_stage_paradigm_shift  | [PASS]   | 最新、参照されるのは次以降   |
| 0501c_full_commit_verification  | [PASS]   | 前回セッション(本セッション前段) |
+--------------------------------+----------+----------------------------+
```

**観察**:
- 起点ジャーナル (Phase 1-2) が参照されないのは時系列上当然。
- ただし **0430c (三角形共鳴箱を「最終形」と主張)、0430d, 0430e, 0430f, 0430g** は後続ジャーナルから明示的に引用されるべきだが、参照されていない。物理的根拠の連鎖が途切れている。

---

## 6. 全単射性 - 数学的判定

```
[単射性] 写像の値が一意に解決されるか?
  -> 36件の幽霊参照 (内訳: 削除12+スクリプト4+リネーム5+その他15)
  -> 単射性違反: 36件

[全射性] 値域がBの全要素をカバーするか?
  -> 43件の孤児ファイル
  -> 全射性違反: 43件

[全単射]: 単射性違反 + 全射性違反 = 79件のギャップ
  170件中 91件が「ジャーナル -> 実ファイル」の双対対応に欠ける
  対応率: 91/170 = 53.5%
```

**結論**: 厳密な数学的全単射は **53.5% でしか成立しない**。これは多数の撤回設計の図版が残置されていることが主因。

---

## 7. 改善提案 (優先度順)

### 最優先 (整合性回復)

1. **design-spec-v1.md の削除済み参照を撤回マーク化** (B群5件)
   - bell-shape-necessity.md など5ファイルの参照を「[撤回] v1設計時の章名、未生成のまま終了」と注記
2. **計算スクリプト4件の保存** (C群4件)
   - phase1_physics.py, phase1b_caseC.py, phase2_dimensions.py を `03-design/v3/scripts/` に永続化
3. **F1-F4.svg のglob記法を実体名に修正** (E群)
   - 0430j, 0430p で `F1_three_view_drawing.svg` 等4ファイル個別に参照

### 中優先 (構造化)

4. **撤回設計図のREADME化**
   - `03-design/v1/figures/README.md`, `03-design/v2/figures/README.md` を作成し、各ファイルを撤回設計の記録として明示参照
   - これで孤児ファイル27+1=28件が救済される
5. **02-physics 各サブディレクトリのfigures に対するREADME**
   - 同様に13件が救済される
6. **ジャーナル間相互参照の補強**
   - 0430g 以降のジャーナルで 0430c, 0430d, 0430e, 0430f を明示引用

### 低優先 (クリーンアップ)

7. **bijection_verification_v1/v2 JSON の削除または .gitignore** (検証成果物v3のみ残置)
8. **README の glob記法を実ファイル名列挙に展開**

---

## 8. 改善後の予測

```
現状 (全単射成立率 53.5%):
  孤児 43 + 幽霊 36 = 79件のギャップ

改善後 (推定):
  最優先 (1-3) 実施 -> 9件減 (12-3スクリプト書き出し+5v1注記+F1-F4×2修正/2(0430j,0430p))
  中優先 (4-5) 実施 -> 41件減 (撤回図のREADME化で救済)
  低優先 (7) 実施 -> 2件減 (検証JSON自己救済)

  合計: 79 - 9 - 41 - 2 = 27件
  全単射成立率: (170-27)/170 = 84.1%

完全な全単射 (100%) は撤回設計の徹底削除を伴うため非推奨
```

---

## 9. 哲学的考察 - リポジトリの「書架」性

```
リポジトリ = 図書館の書架
ジャーナル = 索引カード (目録)
全単射要求 = 「すべての本に索引カードがある、すべての索引カードに対応する本がある」
```

完全な全単射が達成されない理由は **リポジトリが時間軸上の認識の堆積** だからである：
- 過去の認識(撤回された設計の図)を消すと **訂正の歴史** が失われる
- 索引(ジャーナル)を全数引いて参照すると **時系列が壊れる**

ゆえに「**実質的な全単射**」を目指すべき：
- 撤回設計の図は撤回理由付きREADMEで救済 → 孤児解消
- 旧仕様書の幽霊参照は「[撤回]」明示で意味を保持 → 単射違反の許容

**0501b の知見「19世紀物理学の実装実験」** にも通じる:
> Claude は 計算 + 整理を担う。撤回・訂正の履歴管理もその一部。

---

## 10. 残課題

### 最優先

- [TODO] design-spec-v1.md の削除済み参照5件に [撤回] マーク追記
- [TODO] 03-design/v3/scripts/ ディレクトリ作成、phase1/2 スクリプトの再生成または削除明示
- [TODO] 0430j, 0430p の F1-F4.svg 参照を実体名4件に分解

### 中期

- [TODO] 03-design/v1, v2/figures*, 02-physics/各figures/ にREADME追加
- [TODO] 0430g 以降のジャーナルで 0430c-0430f を明示引用

### 長期

- [TODO] 月次/週次でこの全単射検証を回す自動化スクリプト整備
- [TODO] CI で「新規ジャーナル追加時に幽霊参照ゼロ」を保証

---

## 参照

- 検証スクリプト: `verify_bijection_v3.py` (推移閉包, 170ファイル)
- 詳細結果: `bijection_verification_v3.json`
- 前段セッション: `0501c_opus_full_commit_verification_39commits.md`
- 直接の起点: 全28ジャーナル (`03-design/journals/2026-{04,05}/*.md`)
- リポジトリ全体: 170ファイル (md56 + svg58 + png36 + jpg11 + json3 + html2 + py1 + docx1)
