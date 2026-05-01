# 2026-04-30l: リポジトリ3章構造化 (01-specification / 02-physics / 03-design)

## セッションの目的

リポジトリ全体が**ルート階層に文書が散在する状態**だったため、3章構造に整理する。
ユーザ指示:
> 1) 仕様調査 Docもある 画像を格納して
> 2) 原理 物理的検証 いろんな楽器の仕組みを検討した
> 3) 設計 32用 37用 ジャーナル ギター・ベースの具体的設計

## 確定方針

### ディレクトリ構造

```
pianica-organ/
+-- README.md                  [ルート索引]
+-- 01-specification/          楽器の仕様調査
|   +-- README.md
|   +-- suzuki/                W-37C (画像3枚 + READMEのみ、仕様詳細不明)
|   +-- cahaya/                32鍵 (画像11枚 + 詳細README)
|   +-- yamaha-p32d/           P-32D相当 (画像12枚 + 公式仕様調査要)
+-- 02-physics/                原理・物理的検証
|   +-- README.md
|   +-- 22-paths/              22経路解析 (P-32D基準)
|   +-- powerflow/             パワーフローv2.0
|   +-- causal-mechanism/      因果機構 v1/v2
|   +-- materials/             空気室・魂柱・ブリッジ物理
|   +-- helmholtz/             ヘルムホルツ・音響弁
|   +-- three-instruments/     3楽器比較 (ギター・ピアノ・バイオリン)
|   +-- design-document-v2.docx (v2楔形ホーン物理考察、315行)
+-- 03-design/                 設計
    +-- README.md
    +-- v1/                    37本ラッパ (撤回)
    +-- v2/                    楔形ホーン1本 (撤回)
    +-- v3/                    共鳴箱14.2L + ボディ放射 (採用)
    +-- spinet/                スピネット形状 (撤回)
    +-- journals/2026-04/      19本のジャーナル
```

### 確定した判断

| Q | A |
|---|---|
| 履歴保持 | git mv で全移動 (139件) |
| 各章READMEの粒度 | 標準版 (目的 + ファイル一覧 + 主要発見の要約) |
| 鈴木のREADME | 簡易記述 (ジャーナル0430bからの抽出のみ) |
| P-32DのREADME | 枠組みのみ、ヤマハ公式仕様の調査要として明記 |
| spinet (撤回案) | 03-design/spinet/ に保持 (撤回記録として) |
| design-document-v2.docx | 02-physics/ 配下 (物理考察として) |
| 既存photos/melodica-disassembly/ | 01-specification/yamaha-p32d/images/ (真鍮リードでヤマハ識別) |

## 実施内容

### Phase 1: 01-specification/ 構築

- `01-specification/suzuki/images/`: photos/reference/ から3枚をgit mv
- `01-specification/cahaya/images/`: 今回の分解写真11枚を意味のある名前で格納
  - `cahaya_01_overview.jpg` ~ `cahaya_11_keyboard_side.jpg`
- `01-specification/yamaha-p32d/images/`: photos/melodica-disassembly/ から12枚をgit mv
- 各サブディレクトリに `README.md` 作成

### Phase 2: 02-physics/ 構築

ルートにあった以下を移動:

- 22-paths/ <- 11ファイル (md, html, json, py)
- powerflow/ <- 3ファイル
- causal-mechanism/ <- 2ファイル
- materials/ <- 2ファイル
- helmholtz/ <- 2ファイル
- design-document-v2.docx <- 1ファイル
- three-instruments/ <- 図のみ (本文は0430fジャーナル)

### Phase 3: 03-design/ 構築

- v1/ <- design-spec-v1.md
- v2/ <- design-spec-v2.md
- v3/ <- design-spec-v3.md + design-verification-v1.md
- spinet/ <- spinet_pianica_design.md (撤回記録として保持)
- journals/2026-04/ <- 既存19本そのまま移動

### Phase 4: figures/ 振り分け

- 02-physics/22-paths/figures/ <- 9枚
- 02-physics/22-paths/figures-sysid/ <- 6枚 (旧figures-sysid/)
- 02-physics/powerflow/figures/ <- 1枚
- 02-physics/causal-mechanism/figures/ <- 4枚
- 02-physics/materials/figures/ <- 3枚
- 02-physics/helmholtz/figures/ <- 6枚
- 02-physics/three-instruments/figures/ <- 5枚
- 03-design/v1/figures/ <- 1枚
- 03-design/v2/figures/ <- 8枚 + figures-v2/ 別ディレクトリで保持
- 03-design/v3/figures/ <- chapel_organ_v3/ + 2枚

### Phase 5: 各章READMEの作成

3章すべてに「章の目的 + サブディレクトリ構成 + 主要発見の要約 + 関連文書リンク」を記述。
特に以下を強調:

- 01-specification/: 3メーカー比較 (P-32D真鍮 vs CAHAYAアルミ vs 鈴木日本式)
- 02-physics/: 5つの知見階層 (L1 22経路 -> L2 パワーフロー -> L3 因果機構 -> L4 材料 -> L5 楽器比較)
- 03-design/: v1 -> v2 -> spinet -> v3 の進化軌跡 (3段の思想転換)

### Phase 6: ルートREADME.md 更新

- 旧: 「アップライトピアノ筐体、37鍵、足踏み式」(v1ベース、古い記述)
- 新: 「卓上型 550x350x80mm、32鍵 F3-C6、ピアニカ原理駆動」(v3採用版)
- 文書積層構造の旧記述は削除 (各章READMEに移動)

## 整理前後の比較

### 整理前 (ルートに散在)

```
/  
+-- README.md (古い記述、v1ベース)
+-- design-spec-v1.md, v2.md, v3.md  (3つ並列)
+-- design-verification-v1.md
+-- design-document-v2.docx
+-- design_c_acoustic_valve.md
+-- pianica_22paths_*.md (4本)
+-- pianica_powerflow_*.md (1本)
+-- pianica_v3_causal_*.md (2本)
+-- spinet_pianica_design.md
+-- sysid_22paths.* (3ファイル)
+-- helmholtz_resonance_design.md
+-- soundpost_physics_calculation.md
+-- air_chamber_material_physics.md
+-- ... (合計19MD + 各種ファイル)
+-- photos/         (既に整理済)
+-- figures*/       (3ディレクトリに分散)
+-- journals/       (既に整理済)
```

20+ファイルがフラット配置。新参者が見た時に**どこから読めばいいか不明**。

### 整理後 (3章構造)

```
/
+-- README.md (索引、v3採用版に更新)
+-- 01-specification/  (楽器仕様、3メーカー)
+-- 02-physics/        (物理検証、6サブテーマ)
+-- 03-design/         (設計進化、v1->v3 + journals)
```

ルートにあるのはREADME.mdと3章のみ。**3章の役割が見出しで明示**され、各章READMEで詳細にナビゲート可能。

## メタ考察

### Opus の整理プロセスにおける役割

userPreferences「Opusはデータアクセスに関する単純作業 (GIT, ファイル書き出し) は積極的に行う」を活かせた。
判断 (どこに何を置くか) はユーザに委ね、実行 (git mv, README作成) はOpusが担当。

特に以下の場面でユーザの**直接的な判断**が決定的だった:

1. design-document-v2.docx -> 02-physics (具体的楽器でないため)
2. 鈴木3枚 -> 01-specification/suzuki/
3. P-32D 12枚 -> 01-specification/yamaha-p32d/ (リードプレートが真鍮で識別)

特に最後の点で、私 (Claude) は「メーカー不明」と判断していたが、ユーザの「リードプレートが真鍮」の一言で**ヤマハと確定**できた。これは0430k末尾の認知バイアス分析で記録した「物理オブジェクトの観測ではユーザの直接観察が最高優先」の実践例。

### 副次的な発見

整理作業中に判明:

- design-document-v2.docx は v2楔形ホーン設計の正式文書で、315行の本格的内容
- ルートに散在していた文書は **5つの自然なクラスタ**に分かれる:
  - 22経路 (4本+データ)
  - パワーフロー (2本)
  - 因果機構 (2本)
  - 材料・構造物理 (4本)
  - 設計仕様書 (3本+検証)
- ジャーナルは独立クラスタ (時系列記録)、設計とは別軸

### 残課題への影響

3章構造化により、今後のセッションで以下が容易になった:

- 物理計算結果の追加 -> 02-physics/該当サブディレクトリ
- 新設計仕様の追加 -> 03-design/vN/
- 別メーカー機種の追加調査 -> 01-specification/メーカー名/

特に**P-32D公式仕様の調査**は、調査結果を 01-specification/yamaha-p32d/README.md に追記すれば完結する明確な作業として定義された。

## 残課題

### 短期 (本セッション内)

- [DONE] 3章ディレクトリ構造の構築
- [DONE] git mv で全文書移動 (履歴保持)
- [DONE] 各章READMEの作成
- [DONE] ルートREADME更新
- [DONE] 本ジャーナル (0430l) 作成
- [TODO] git commit + push

### 中期 (次セッション以降)

- **P-32D公式仕様の調査** (ヤマハサポート、製品マニュアル、銘板)
  - 01-specification/yamaha-p32d/README.md を更新
- **CAHAYAリードプレートの実測寸法取得**
  - 01-specification/cahaya/README.md の残課題に明記済
- **鈴木W-37Cの仕様詳細**
  - 01-specification/suzuki/README.md の残課題に明記済
- 03-design/v3/ で設計進行中の項目 (図面詳細化、製作計画Phase 1)

### 長期 (製作)

- CAHAYA入手 + 分解 (DONE: 0430k)
- リードプレート流用部品の確定
- 桐1.5mm共鳴箱の製作 (Phase 1)
- T0/T1実測 (Spectroid) -> ブレース調整 (Phase 2)
- 教会試演 (Phase 4)

## 参照

- 直前ジャーナル: `journals/01-specification/2026-04/0430k_opus_cahaya_disassembly_32keys_p32d_alignment.md`
- 各章索引: `01-specification/README.md`, `02-physics/README.md`, `03-design/README.md`
- ルート索引: `README.md` (本セッションで更新)
