# GitHub運用手順 (ピアニカ・オルガン プロジェクト)

リポジトリ: KishowFujiwara/pianica-organ (Private)

> **来歴**: 2026-04-29 に `KishowFujiwara/EngineringKnowlege/decoded/pianika-organ/` から
> 独立リポジトリとして分離。
> 詳細は `journals/02-physics/2026-04/0429_opus_gpt_inspection_powerflow_v2.md` 参照。

---

## このファイルの目的

各セッションでClaudeが設計作業・物理検証・実機観測を行った際、GitHubにcommitするための手順書。`git-manifest.md` と合わせて運用ルールの基盤とする。

**Project Knowledge (PK) は本プロジェクトでは利用しない。**
- 運用ルールはすべてリポジトリ内に明示する
- セッション開始時にClaudeは本ファイルと `git-manifest.md` を読む
- ユーザはセッション開始時にリポジトリのURLとトークンを提供する

---

## pianica-organ 固有の運用方針

### EngineringKnowlege との違い

| 項目 | EngineringKnowlege | pianica-organ (本リポジトリ) |
|---|---|---|
| 主要資産 | PDF解読結果 (Vision OCR) | 楽器設計成果物 + 物理検証 + ジャーナル |
| 入力ソース | 書籍PDF | 実機 (CAHAYA等) + 文献調査 + 物理計算 |
| 成果物の粒度 | 章単位の解読MD + 数式カタログ | 設計仕様書 + 物理モデル + 章別ジャーナル |
| 台帳の名称 | git-manifest.md | git-manifest.md (本リポジトリ) |
| 検証手法 | 全単射写像検証 (PDF原典 <-> カタログ) | ディレクトリ別全単射 (ジャーナル <-> 成果物) |
| 入力格納 | sources/ (PDFディレクトリ) | 01-specification/{楽器}/images/ (実機写真) |
| PK利用 | 任意 | **利用しない** |

### 設計プロジェクト型運用

```
Step 1: 観測
  - 既存リポジトリ構造の確認 (git pull --rebase)
  - 直近のジャーナル読込 (4セッション最低限)
  - git-manifest.md と現実のファイルを照合
  - userPreferences の確認

Step 2: 実施準備
  - 物理計算が必要なら計算式の検算
  - 実機写真があれば画像確認
  - 過去の撤回履歴と矛盾しないか確認

Step 3: 実施計画
  - 成果物の章を決定 (01/02/03/cross のどこに置くか)
  - ジャーナルを置く章を決定
  - コミットメッセージのプレフィックスを決定

Step 4: 段階的実施
  - 設計文書/物理モデル/ジャーナルを作成
  - 必要なら全単射検証スクリプト実行
  - git-manifest.md を更新 (新規ファイル追加時)
  - git commit + push
```

---

## ディレクトリ構成と配置ルール

```
成果物の種類 -> 配置先:

  楽器仕様 (実機分解写真, 計測ガイド)  -> 01-specification/{cahaya, yamaha-p32d, suzuki}/
  物理検証 (理論モデル, 計算結果)       -> 02-physics/{22-paths, powerflow, materials, ...}/
  設計成果物 (design-spec, 図面)       -> 03-design/{v1, v2, v3, spinet}/
  検証スクリプト                       -> 03-design/v3/scripts/verification/
  ジャーナル (時系列記録)              -> journals/{01-/02-/03-/cross}/{2026-MM}/
```

### ジャーナルの章別分類規則 (0501g 確立)

ジャーナルは「**主たる成果物がどの章のディレクトリか**」で分類する:

| 主成果物 | 配置先 | 例 |
|---|---|---|
| 01-specification 配下の更新 (CAHAYA分解, MEASUREMENT_GUIDE) | journals/01-specification/ | 0430k, 0430o, 0430q |
| 02-physics 配下の更新 (22経路, Gamma理論) | journals/02-physics/ | 0428*, 0429, 0430b, 0430h |
| 03-design 配下の更新 (design-spec改訂) | journals/03-design/ | 0423*, 0430j, 0501a, 0501b |
| 横断的作業 (リポジトリ整備, 検証, メタ) | journals/cross/ | 0430l, 0430m, 0501c-g |

**判断に迷う場合**: 本文を読んで「最終的にどのディレクトリにファイルを書き込んだか」で判定。

---

## ファイル命名規則

### ジャーナル

```
journals/{章}/YYYY-MM/MMDD[suffix]_modelname_short_topic.md

YYYY-MM    : 4桁年-2桁月 (例: 2026-04)
MMDD       : 月日 (例: 0430)
[suffix]   : 同日内通番 (a, b, c, ... 必要時)
modelname  : opus / sonnet / haiku
short_topic: スネークケースの主題 (英語、簡潔に)
```

例:
- `journals/03-design/2026-04/0423_opus_pianika_organ_design.md`
- `journals/02-physics/2026-04/0430g_opus_B_system_decomposition_dfc79ff_verification.md`
- `journals/cross/2026-05/0501f_opus_journal_directory_independence.md`

### 設計成果物

```
03-design/{version}/design-spec-{version}.md      設計仕様書 (主体)
03-design/{version}/design-document-{version}.docx 設計仕様書 完全文書 (DOCX)
03-design/{version}/figures/{図名}.svg             図版
```

### 物理検証

```
02-physics/{topic}/{topic}_{aspect}.md             物理モデル
02-physics/{topic}/figures/{図名}.svg              関連図
02-physics/{topic}/{topic}.json                    パラメータデータ
```

### バージョン管理

```
重要: 上書きcommitする。 _v2 などのサフィックスは作らない。
  [OK] 同じファイル名で内容を更新 -> git commit
  [NG] design-spec-v3_revised.md / design-spec-v3_new.md などを作成

例外: 設計バージョンが大きく変わる場合のみディレクトリで区別
  v1/, v2/, v3/, v4/ ...
```

### Errata (修正) の取扱い

```
重要: 本体に直接マージする。Errataファイルは作らない。
  [OK] 本体ファイルに修正を追記/修正 -> git commit -m "[fix] ..."
  [NG] Errata_xxx.md を別ファイルで作成
```

ただしジャーナルは時系列記録なので **撤回は記録**。後続ジャーナルで「[撤回] 0430c の三角形共鳴箱主張」のように明示する。

---

## コミットメッセージのフォーマット

```
[カテゴリ] 簡潔な説明 / 詳細1 / 詳細2 / ...

カテゴリ:
  [design]      ... 設計仕様書 (03-design 配下)
  [physics]     ... 物理検証 (02-physics 配下)
  [observe]     ... 実機観測 (01-specification 配下)
  [observe-fix] ... 実機観測の訂正
  [journal]     ... セッションジャーナル
  [fix]         ... 物理計算/設計の誤り修正
  [revoke]      ... 設計/モデルの撤回
  [refocus]     ... 設計方針の再定義
  [refactor]    ... ディレクトリ再構成等
  [restructure] ... リポジトリ構造の大幅変更
  [verify]      ... 検証 (全単射, コミット網羅性等)
  [paradigm]    ... 設計パラダイムの根本転換
  [migrate]     ... 外部リポジトリからの移管
  [meta]        ... README, manifest, workflow 等の運用ファイル
```

例:
```
[journal+verify] 2026-05-01e ディレクトリ別 全単射検証: 34ディレクトリを5タイプに分類 / 真の孤児12件特定 / 数学的53.5% vs 実質92%

[restructure+journal] 2026-05-01g 全ディレクトリのジャーナル独立: journals/{01,02,03,cross}/2026-XX/ 章別再分類 / 31本git mv / パス修正22ファイル / 真の孤児ジャーナルゼロ維持

[design+fix] 0430k CAHAYA分解観測: 37鍵 -> 32鍵に訂正 / F6 -> C6
```

複数カテゴリは `+` で連結 (例: `[journal+verify]`, `[design+physics]`)。

---

## GitHubにcommitする手順

```bash
# clone (ユーザがトークンを userPreferences に記載)
cd /home/claude
git clone "https://<USER>:<TOKEN>@github.com/KishowFujiwara/pianica-organ.git"
cd pianica-organ
git config user.name "Claude (Opus 4.7)"
git config user.email "claude-opus@anthropic.ai"

# セッション開始時の確認
git pull --rebase
ls journals/cross/2026-MM/  # 最新セッションを確認

# 作業実施
# (Step1: 観測 -> Step2: 準備 -> Step3: 計画 -> Step4: 実施)

# ファイル配置 + commit
git add -A
git status -s   # 変更内容の確認

git commit -m "[design+journal] YYYY-MM-DDx 主題 / 詳細"
git push origin main

# 検証 (任意、月次推奨)
python3 03-design/v3/scripts/verification/verify_bijection_by_dir_v2.py
```

---

## セッション開始時のClaudeの最低限作業

```
1. git pull --rebase で最新化
2. ls journals/cross/2026-MM/ で最新メタジャーナルを把握
3. 直近4本のジャーナルを読む (時系列で文脈把握)
4. ユーザの指示を Step1〜4 で処理開始
5. ジャーナル作成時は適切な章のサブディレクトリへ
6. git-manifest.md を新規追加ファイルがあれば更新
```

---

## 全単射写像検証手法

pianica-organ 固有の検証プロセス (0501d/e/g 確立):

```
[ファイルレベル検証]
1. リポジトリ内全ファイルを列挙 (md/svg/png/jpg/docx/html/json/py)
2. ジャーナル (起点) からの参照を推移閉包で取得
3. 単射性: ジャーナル参照が全て実在ファイルに解決されるか (幽霊参照ゼロ)
4. 全射性: 全実ファイルが少なくとも1つのジャーナルから参照されているか (孤児ゼロ)

[ディレクトリレベル検証]
1. 全ディレクトリを5タイプに分類 (Index/Hub/Spec/Journal/Leaf)
2. タイプ別に適切な指標で評価:
   - Leaf: 外部被参照率
   - Spec/Hub: 内部完結率
   - Journal: 内部相互参照率
3. 真の孤児 (誰からも参照されず、自身も他を参照しない) を特定

[実用的な評価]
- 数学的厳密な全単射: 撤回設計の図版が孤児になり成立しにくい (53.5%)
- 実質健全性: 撤回設計を許容して評価 (92%)
- 後者を主指標とする
```

検証スクリプト:
```
03-design/v3/scripts/verification/verify_bijection_v3.py        (全体)
03-design/v3/scripts/verification/verify_bijection_by_dir_v2.py (ディレクトリ別)
03-design/v3/scripts/verification/fix_journal_refs.py           (相互参照修正)
```

---

## userPreferences の重要項目

ユーザは `userPreferences` で以下を指定する:

```
1. モデル別の権限 (Haiku/Sonnet/Opus)
2. Step1〜4の必須実施
3. セッションジャーナル + プロジェクト原点の必読
4. SKILLの必須利用
5. 出力言語 (日本語、文字化け対策)
6. OCR方針 (Claude Vision がデフォルト)
7. GitHubトークン (本リポジトリ用)
```

ユーザがトークンを更新した場合、本ファイルは更新不要 (userPreferencesに記載)。

---

## Project Knowledge (PK) について

**本プロジェクトでは PK を利用しない**。

理由:
- ファイル数が増減する設計プロジェクトでは PK の更新コストが高い
- リポジトリ内のジャーナルとgit-manifest.md がSSOTとして機能する
- 月次/週次の全単射検証で整合性を維持する

代替手段:
- セッション開始時に Claude は `git-manifest.md` を読む
- 直近のジャーナル (4本程度) を読んで文脈を把握
- userPreferences でセッションジャーナル必読を明示
