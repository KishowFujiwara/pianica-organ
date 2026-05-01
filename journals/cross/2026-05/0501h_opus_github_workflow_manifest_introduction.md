# 2026-05-01h: GitHub運用ドキュメント導入 (PKは利用しない)

**セッション目的**: ユーザ指示「`https://github.com/KishowFujiwara/EngineringKnowlege` ルートのファイルにGITHUB運用 PK-Manifest を このレポジトリでも導入 ただし PKは利用しない」に基づき、運用ドキュメント `git-manifest.md` と `github_workflow.md` を pianica-organ リポジトリに導入する。

**前段**:
- 0501c〜g (cross): リポジトリ構造の安定化フェーズ
- 0501g (cross): ジャーナル章別分類完了 (本セッションは構造的にクリーンな状態で運用ドキュメントを置く)

---

## 1. 観測 - EngineringKnowlege の運用ドキュメント

### git-manifest.md (台帳)

EngineringKnowlege/git-manifest.md は **PDF解読プロジェクト** の台帳:
```
原典台帳        : sources/ のPDFを書籍別に管理
解読成果物台帳   : decoded/書籍名/ の章別MD + 数式カタログ
Session Journal台帳: journals/YYYY-MM/ の時系列記録
コミット履歴台帳  : 主要コミットの分類・要約
統計             : ファイル数・行数のサマリー
```

特徴:
- PK (Project Knowledge) との同期は任意で、Git側がSSOT
- 全単射写像検証 (PDF原典 ↔ 数式カタログ) を主検証手段とする
- 書籍ごとのディレクトリ構造 (decoded/{書籍短縮名}/)

### github_workflow.md (運用手順)

EngineringKnowlege/github_workflow.md は:
```
- engineeringknowledge 固有の運用方針
- 解読プロセス標準手順 (Step1-4)
- ディレクトリ構成と配置ルール
- ファイル命名規則
- コミットメッセージのフォーマット
- GitHubにcommitする手順
- 既存ファイルの更新時 / Errata発生時の規則
- 全単射写像検証手法
- Project Knowledge (PK) について
```

---

## 2. 適応 - pianica-organ への翻訳

### EngineringKnowlege と pianica-organ の本質的違い

```
+---------------+----------------------+--------------------------------+
| 項目           | EngineringKnowlege   | pianica-organ                  |
+---------------+----------------------+--------------------------------+
| 主資産         | PDF解読結果           | 設計成果物 + 物理検証 + ジャーナル |
| 入力ソース     | 書籍PDF              | 実機 (CAHAYA等) + 文献 + 計算   |
| 成果物粒度     | 章単位の解読MD        | 設計仕様書 + 物理モデル + 章別ログ|
| 検証手法       | PDF<->カタログ全単射  | ジャーナル<->成果物全単射(ディレクトリ別)|
| 入力格納       | sources/ (PDF)       | 01-specification/{楽器}/images/  |
| バージョン管理  | (基本一品もの)        | v1/v2/v3/spinet (4世代)          |
| PK利用         | 任意                  | **利用しない** ★                 |
+---------------+----------------------+--------------------------------+
```

### PK利用しない方針の意義

```
[本プロジェクトでPKを利用しない理由]

1. ファイル数の動的変化
   - 設計プロジェクトでは v3->v4 移行などでファイル群が大きく変わる
   - PKの更新コストがGit管理より高い
   
2. リポジトリ内自己充足
   - git-manifest.md がSSOTとして機能する
   - 直近のジャーナル (4本程度) で文脈継承可能
   
3. 全単射検証で整合性維持
   - 月次/週次で verify_bijection_by_dir_v2.py を実行
   - 構造健全性を定量的に追跡
   
4. userPreferencesでの最低限の継承
   - GitHubトークン
   - 必読ファイル指示 (セッションジャーナル + 原点)
```

---

## 3. 作成した文書

### git-manifest.md (本リポジトリ台帳)

```
構成 (全11セクション):

  1. プロジェクト概要 (目的、設計原理、現在地、実験プラットフォーム)
  2. リポジトリ構成 (3章 + 章別ジャーナル)
  3. 楽器仕様台帳 (01-specification/)
  4. 物理検証台帳 (02-physics/)
  5. 設計成果物台帳 (03-design/)
     - v1, v2, v3, spinet の世代別
     - v3 主要ドキュメント詳細
     - v3 残課題 (2段構造改訂など)
  6. ジャーナル台帳 (journals/)
     - 章別件数 (01:3, 02:12, 03:10, cross:7)
     - 章別ジャーナル一覧
  7. コミット履歴台帳 (Phase 0-10、44コミット)
  8. 統計
  9. 検証台帳 (実施済み3件 + スクリプト + 残課題)
```

### github_workflow.md (運用手順書)

```
構成 (全11セクション):

  1. このファイルの目的 (PK利用しない方針を明示)
  2. pianica-organ 固有の運用方針
     - EngineringKnowlege との違い
     - 設計プロジェクト型運用 (Step1-4)
  3. ディレクトリ構成と配置ルール
     - 成果物の種類別配置
     - ジャーナル章別分類規則 (0501g 確立)
  4. ファイル命名規則
     - ジャーナル / 設計成果物 / 物理検証
     - バージョン管理 / Errata取扱
  5. コミットメッセージのフォーマット
     - カテゴリ14種類
     - 具体例
  6. GitHubにcommitする手順
  7. セッション開始時のClaudeの最低限作業
  8. 全単射写像検証手法 (0501d/e/g 確立)
  9. userPreferences の重要項目
  10. Project Knowledge (PK) について (利用しない理由を明記)
```

---

## 4. 実施詳細 (Step1〜4)

### Step1: 観測

```
- KishowFujiwara/EngineringKnowlege をクローン
- ルート直下のファイル確認: README.md, git-manifest.md, github_workflow.md
- 両運用ドキュメントの全文読込
- 構造とトーンを把握
```

### Step2: 実施準備

```
- pianica-organ の現状確認 (44コミット, 178ファイル, 32ジャーナル)
- 0501g時点のクリーンな構造を起点とする
- 翻訳方針: PK削除、設計プロジェクト型に書き換え
```

### Step3: 実施計画

```
1. git-manifest.md 作成 (11セクション、台帳)
2. github_workflow.md 作成 (11セクション、運用手順)
3. README.md に運用ドキュメント節を追加
4. ジャーナル 0501h で記録
5. コミット&push
```

### Step4: 段階的実施

```
4-1: git-manifest.md 作成 (約600行)
4-2: github_workflow.md 作成 (約400行)
4-3: README.md に「運用ドキュメント」節を追加
4-4: 本ジャーナル作成
4-5: コミット&push
```

---

## 5. 翻訳における重要な変更点

### EngineringKnowlege → pianica-organ への翻訳パターン

```
+----------------------------+-----------------------------+
| EngineringKnowlege          | pianica-organ                |
+----------------------------+-----------------------------+
| sources/{書籍名}.pdf         | 01-specification/{楽器}/    |
| decoded/{書籍短縮名}/        | 03-design/{バージョン}/      |
| (なし)                       | 02-physics/{topic}/          |
| journals/YYYY-MM/foo.md      | journals/{章}/YYYY-MM/foo.md|
| 章別解読MD                   | 設計仕様書 (design-spec)     |
| 数式カタログ                  | パワーフロー数理モデル        |
| 全単射写像検証 (PDF<->数式)  | 全単射写像検証 (ジャーナル<->成果物)|
| [decode] [equation] [verify]| [design] [physics] [journal] [verify] |
+----------------------------+-----------------------------+
```

### PK同期記述の削除

EngineringKnowlege/github_workflow.md には:
> 「Project Knowledge (PK) について
> PKに何を載せるかはユーザーが判断する。Claudeは関与しない。」

これを pianica-organ/github_workflow.md では:
> 「Project Knowledge (PK) について
> 本プロジェクトでは PK を利用しない。」

積極的な不採用宣言に変更。

---

## 6. 副次的効果

### Phase 10 のメタ作業群が完結

```
0501c (cross): 全39コミット検証
0501d (cross): 全単射写像検証 (53.5%)
0501e (cross): ディレクトリ別検証 (実質92%)
0501f (cross): Journal独立化
0501g (cross): ジャーナル章別分類
0501h (本セッション、cross相当): 運用ドキュメント導入 ★
```

これでPhase 10 (メタ検証 + 構造化 + 運用ドキュメント) が完結。リポジトリの構造的・運用的基盤が確立。

### git-manifest.md の役割

将来のセッションで:
- Claudeはセッション開始時に `git-manifest.md` を読んでリポジトリ全体像を把握
- 直近ジャーナル4本で時間的文脈を継承
- userPreferences でGitHubトークン取得

これによりPK不要でセッション間継承が成立。

---

## 7. 残課題

### 解消された問題

```
[CLOSED] 運用ルールがリポジトリ外 (PK) にある状態
[CLOSED] 新規セッションでの運用混乱リスク
[CLOSED] git-manifest台帳の不在
```

### 残存する設計課題 (前段から継続)

```
[OPEN] design-spec-v3 の 2段構造への改訂 (0501b で宣告済の最優先)
[OPEN] 03-design/v1/design-spec-v1.md の削除済み章6件
[OPEN] 03-design/v3/scripts の計算スクリプト3件未保存
[OPEN] 03-design/v2/figures-v2 の孤児4件 (READMEで救済可能)
```

### 中期残課題

```
[TODO] 月次の全単射検証を自動化 (CI)
[TODO] 撤回設計のアーカイブ整理
```

---

## 8. 関連

- 直前: `./0501g_opus_journals_chapter_classification.md` (ジャーナル章別分類)
- 検証履歴: `./0501c-e_*.md` (Phase 10 メタ検証群)
- 運用ドキュメント: `../../../git-manifest.md`, `../../../github_workflow.md`
- 起点: EngineringKnowlege/git-manifest.md, EngineringKnowlege/github_workflow.md

## 9. 次セッションへの引き継ぎ

```
[完了]
  - git-manifest.md 導入 (リポジトリコンテンツ台帳)
  - github_workflow.md 導入 (運用手順書)
  - README.md に運用ドキュメント節追加
  - PK利用しない方針の明示

[次の論理ステップ]
  Phase 11 候補:
  Option A: design-spec-v3 の 2段構造への改訂 (最優先)
  Option B: 撤回設計のアーカイブ整理 (v1/v2 撤回図のREADME化)
  Option C: 計算スクリプト3件の再生成 (phase1, phase1b, phase2)
  Option D: L5実測ガイド実行による実機作成準備
```
