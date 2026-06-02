# ボスポラスTBM案件 — 全社コンテキスト構築シミュレーション
## Step 1: 観測 → Step 2: 準備 → Step 3: 計画

**信頼度**: [EST] — 架空シミュレーション

---

## Step 1: 観測

### [2026-05-10 03:18] 営業エージェントがAGENT-DISCOVERY-001を登録

（simulation_bosphorus_agent_reasoning.md Week -1 参照）

```
status: "人間の判断待ち"
コンテキスト残高: 1レコード（エージェント検出のみ。人間発言ゼロ）
```

---

### [2026-05-12 10:00] 営業定例 — 人間が初めて動く

```
出席: 営業部長 中村、営業課長 藤田、海外営業 小林
議題: エージェント検出レポート AGENT-DISCOVERY-001 の確認
```

**中村**: エージェントが拾ってきたボスポラスの件。レポートを読んだ。リスク5件が付いている。小林、代理店に確認は取れるか。

**小林**: トルコ代理店のメフメットに連絡します。RFQが出ているか、施主が何を求めているか、競合は誰か。

**藤田**: うちは船舶用だろう。トンネルの発電機は畑が違う。

**小林**: エージェントのレポートにも「実績ゼロ」と書いてある。ただし出力帯は合う。6S35ME-Cで4.5MW。

**中村**: 開発と研究に話を通せ。設計にも。一週間でフィージビリティ。

```
コンテキスト動線:

  AGENT-DISCOVERY-001.status → "営業部長Go（条件付き）"
  ↓
  新規登録:
```

```json
[
  {"id":"SALES-001", "source":"営業", "speaker":"小林", "time":"2026-05-12 10:15",
   "claim":"トルコ代理店に状況確認する",
   "formalized":"Action(contact_turkey_agent, by=小林, deadline=2026-05-13)",
   "trust":"[FACT]（行動宣言）", "context_trigger":"AGENT-DISCOVERY-001"},

  {"id":"SALES-002", "source":"営業", "speaker":"小林", "time":"2026-05-12 10:20",
   "claim":"TBM発電機用。1基3-5MW。6S35ME-Cが出力的に合う",
   "formalized":"◇Suitable(6S35MEC, tbm_generator, 3to5MW)",
   "trust":"[DRV]", "unchecked":["TBM発電機の実際の仕様", "設置空間", "防爆要件"]},

  {"id":"SALES-003", "source":"営業", "speaker":"小林", "time":"2026-05-12 10:25",
   "claim":"アンモニアエンジンならトンネル内換気負荷が下がる",
   "formalized":"◇Advantage(NH3_engine, reduced_ventilation, tunnel)",
   "trust":"[EST]", "unchecked":["NOx実測値", "NH3漏洩リスク", "防爆規格"]},

  {"id":"SALES-004", "source":"営業", "speaker":"中村", "time":"2026-05-12 10:30",
   "claim":"地下トンネル内にエンジンを入れた実績はゼロ",
   "formalized":"¬∃x(PastProject(x) ∧ Underground(x) ∧ OurEngine(x))",
   "trust":"[FACT]"}
]
```

```
コンテキスト残高: 5レコード
unchecked: 6件 / conditions: 1件
HumanMatter消化: 1件（「追うか」→ Go）
```

---

### [2026-05-13 16:00] 代理店情報が入る

```
小林がSlackに投稿:
「メフメットから返信。RFQ非公開だが施主は代替案を求めている。
 競合はW社(FIN)とM社(DE)。うちがアジア唯一。施主希望6ヶ月以内」
```

```
エージェント自動処理 [16:05]:
  Slack検出 → コンテキスト登録 → SALES-001を"完了"に更新
```

```json
{"id":"SALES-005", "source":"営業", "speaker":"小林", "time":"2026-05-13 16:00",
 "claim":"RFQ非公開。競合W社M社。施主6ヶ月以内希望",
 "formalized":"¬Public(RFQ) ∧ Competitors([W_fin, M_de]) ∧ CustomerDeadline(6m)",
 "trust":"[OBS]（代理店経由）",
 "unchecked":["施主予算", "正式RFQ時期", "競合提案状況"]}
```

```
コンテキスト残高: 6レコード / unchecked: 9件
```

---

## Step 2: 準備

### [2026-05-15 14:00] 開発フィージビリティ会議

```
出席: 開発部長 山田、主任 岡本、アンモニアPJ 佐々木、営業 小林
```

**岡本**: ディーゼルなら6S35ME-Cで4.5MW。枯れた技術。ただしトンネル内はSCR+DPFが要る。

```
エージェント [14:15]:
  SALES-003[EST]「換気が楽」vs 岡本[DRV]「換気計算が要る」→ 楽観性フラグ
  ★会議中は介入しない
```

**佐々木**: アンモニアはTRL4。単気筒専焼確認済み。多気筒は来年6月。間に合わない。

**岡本**: 地下据付は防爆規格が要る。船舶用は非防爆。

**山田**: 短期ディーゼル＋中長期アンモニア。2段構え。設計に防爆を振れ。研究にNH3リスクを。

```json
[
  {"id":"DEV-001", "source":"開発", "speaker":"岡本",
   "claim":"ディーゼル6S35ME-C 4.5MW。枯れた技術",
   "formalized":"Feasible(diesel_6S35MEC, 4.5MW, verified)", "trust":"[FACT]"},

  {"id":"DEV-002", "source":"開発", "speaker":"岡本",
   "claim":"トンネル内SCR+DPF必要。換気量計算未了",
   "formalized":"Requires(tunnel, SCR_DPF) ∧ ¬Completed(ventilation_calc)",
   "trust":"[DRV]", "unchecked":["トルコ排気規制値", "断面と換気能力", "SCR空間"]},

  {"id":"DEV-003", "source":"開発", "speaker":"佐々木",
   "claim":"NH3エンジンTRL4。多気筒は来年6月",
   "formalized":"AtTRL(NH3_engine, 4) ∧ ¬Available(multi_cyl, before_2027_06)",
   "trust":"[FACT]+[EST]", "limitations":["単→多気筒未検証", "NH3インフラ未確認"]},

  {"id":"DEV-004", "source":"開発", "speaker":"岡本",
   "claim":"船舶用は非防爆。地下は設計変更要の可能性",
   "formalized":"¬ExplosionProof(marine_engine) ∧ ◇Requires(underground, exproof_mod)",
   "trust":"[FACT]+[EST]", "unchecked":["ATEX適用範囲", "改造範囲"]},

  {"id":"DEV-005", "source":"開発", "speaker":"山田",
   "claim":"短期diesel＋中長期NH3の2段構え",
   "formalized":"Strategy(short=diesel, mid_long=NH3_proposal)",
   "trust":"[DRV]", "conditions":["設計の防爆見積", "研究のNH3リスク評価", "営業RFQ確認"]}
]
```

```
エージェント動線処理 [14:40]:
  AGENT-DISCOVERY-001.risks[R2]「非防爆」= DEV-004[FACT] → 一致確認
  
コンテキスト残高: 11レコード / unchecked: 15件 / conditions: 4件
```

---

### [2026-05-19 10:00] 設計検討会

```
出席: 設計課長 高橋、構造 伊藤、補機 渡辺、開発 岡本
```

**伊藤**: 6S35ME-C: 全長12m×幅4m×高さ8m、180t。トンネル14mに入るか。

```
エージェント [10:05]:
  H=8m + exhaust≈8m = 16m > 14m → ◇Conflict(vertical) を即時検出
  ★記録のみ。レイアウト検討で解消される可能性
```

**渡辺**: SCR+DPF据付面積≈エンジン3倍。

**高橋**: ATEX Zone2なら電装系防爆。本体は変更不要。

**伊藤**: 岩盤据付の振動伝播が船舶と異なる。FEM要。

**渡辺**: NH3配管はIGCコードと別基準。二重管・漏洩検知・緊急遮断弁が必須。

```json
[
  {"id":"DES-001", "source":"設計", "speaker":"伊藤",
   "claim":"6S35ME-C: 12m×4m×8m, 180t",
   "formalized":"Dim(6S35MEC, L=12m, W=4m, H=8m) ∧ Weight(dry,180t)",
   "trust":"[FACT]", "unchecked":["トンネル内径との干渉"]},

  {"id":"DES-002", "source":"設計", "speaker":"渡辺",
   "claim":"SCR+DPF据付面積≈エンジン3倍",
   "formalized":"InstallArea(exhaust) ≈ 3×InstallArea(engine)",
   "trust":"[DRV]", "unchecked":["最適化レイアウト"]},

  {"id":"DES-003", "source":"設計", "speaker":"高橋",
   "claim":"ATEX Zone2→電装系防爆。本体変更不要",
   "formalized":"If(ATEX_Zone2) then Requires(elec, exproof) ∧ ¬Requires(body, change)",
   "trust":"[DRV]", "unchecked":["トルコがATEX準拠か", "Zone判定者"]},

  {"id":"DES-004", "source":"設計", "speaker":"伊藤",
   "claim":"岩盤据付の振動解析(FEM)が必要",
   "formalized":"¬Applicable(marine_vibration, rock) ∧ Requires(FEM)",
   "trust":"[DRV]", "unchecked":["岩盤弾性係数", "掘削面不整"]},

  {"id":"DES-005", "source":"設計", "speaker":"渡辺",
   "claim":"NH3配管はIGCコードと別基準",
   "formalized":"¬Applicable(IGC, tunnel_NH3) ∧ Requires([double_pipe, leak_det, shutoff])",
   "trust":"[DRV]", "unchecked":["トルコ危険物配管規格", "NH3拡散シミュレーション"]}
]
```

```
エージェント動線処理 [10:45]:
  DES-003.unchecked「トルコATEX」= DEV-004.unchecked「ATEX適用」→ 統合Issue候補
  
コンテキスト残高: 16レコード / unchecked: 23件
```

---

### [2026-05-20 13:00] 製造検討会

```
出席: 製造部長 佐藤、工程管理 田辺、品管 木下、設計 高橋
```

**田辺**: K向け同型機が組立70%完了。転用すれば4ヶ月。

**高橋**: K向けは標準船舶仕様。ボスポラスは防爆電装+振動対策が追加。本体共通、補機は作り直し。

**田辺**: 補機だけなら2ヶ月。

**木下**: 船級認証（NK/DNV）はトンネル用に使えるか。

```
エージェント [13:25]:
  木下「認証」= AGENT-DISCOVERY-001.R3 = DEV-004.unchecked = DES-003.unchecked
  → 4つの独立ソースが同じ問題を指摘。誰も答えを持っていない。
  → 優先度引き上げ
```

```json
[
  {"id":"MFG-001", "source":"製造", "speaker":"田辺",
   "claim":"K向け同型機組立70%。転用で4ヶ月出荷可能",
   "formalized":"∃unit(ForCustomer(K) ∧ Progress(70%)) ∧ If(Diverted) then LT(4m)",
   "trust":"[FACT]+[DRV]",
   "conditions":["K社了解", "仕様差確定", "認証解決"]},

  {"id":"MFG-002", "source":"製造", "speaker":"田辺",
   "claim":"補機のみ新製なら2ヶ月", "trust":"[FACT]"},

  {"id":"MFG-003", "source":"製造", "speaker":"木下",
   "claim":"船級認証はトンネル用に使えない可能性",
   "formalized":"◇¬Valid(NK_DNV, for_tunnel)",
   "trust":"[DRV]", "unchecked":["トンネル用認証機関"]}
]
```

```
コンテキスト残高: 19レコード / unchecked: 24件 / conditions: 7件
```

---

### [2026-05-21 15:00] 研究進捗会

```
出席: 研究部長 松本、アンモニア燃焼 佐々木、安全評価 野田、開発 山田
```

**佐々木**: NH3燃焼排気。CO2=0。NOx=200ppm（単気筒）。管理濃度25ppmを満たすには追加処理が要る。

```
エージェント [15:08]:
  ★★★ 重大照合:
  SALES-003[EST]「換気が楽」 vs RES-001[FACT] NOx=200ppm >> 25ppm
  → 「NH3=クリーン=換気不要」の短絡リスク確定
  → SALES-003に注記付与: "CO2のみ成立。NOxは別途対策要"
```

**野田**: NH3 IDLH=300ppm。密閉空間の拡散シミュレーション必要。

**佐々木**: 部分負荷で失火リスク。TBM負荷変動への追従性が課題。

**松本**: 不可能ではないが未検証領域が多い。報告書は2ヶ月。

```json
[
  {"id":"RES-001", "source":"研究", "speaker":"佐々木",
   "claim":"NH3排気: CO2=0, NOx=200ppm（単気筒）",
   "formalized":"Emission(NH3, CO2, 0) ∧ Emission(NH3, NOx, 200ppm)",
   "trust":"[FACT]", "limitations":["単気筒", "定常のみ", "過渡未測定"]},

  {"id":"RES-002", "source":"研究", "speaker":"野田",
   "claim":"NH3 IDLH=300ppm。拡散シミュレーション必要",
   "trust":"[FACT]+[OBS]", "unchecked":["トンネル断面", "換気風速", "漏洩量"]},

  {"id":"RES-003", "source":"研究", "speaker":"佐々木",
   "claim":"部分負荷で失火リスク。TBM負荷追従が課題",
   "formalized":"◇Risk(misfire, partial_load) ∧ ¬Tested(transient)",
   "trust":"[OBS]", "limitations":["多気筒不明", "TBM負荷パターン未取得"]},

  {"id":"RES-004", "source":"研究", "speaker":"野田",
   "claim":"NH3爆発下限15.0vol%。H2混合時は低下",
   "trust":"[FACT]（化学便覧）"}
]
```

```
エージェント動線処理 [15:45]:

  信頼度不整合確定:
    SALES-003[EST] ←部分否定→ RES-001[FACT]
  
  研究データの限界マーキング:
    RES-001.limitations + DEV-003[TRL4] + DEV-005[NH3提案]
    → 提案根拠がTRL4+単気筒のみ → limitations明記の要否をHumanMatter化

コンテキスト残高: 23レコード
  AGENT:1 / 営業:5 / 開発:5 / 設計:5 / 製造:3 / 研究:4
  unchecked: 27件 / conditions: 7件 / limitations: 5件
  信頼度不整合: 1件
```

---

## Step 3: 計画

### [2026-05-22 08:00] エージェント全コンテキスト走査 → 計画立案

```
[08:00] 走査開始: 23レコード / 27 unchecked / 7 conditions / 5 limitations / 1 信頼度不整合
```

---

### 計画A: 空間干渉の解決

```
推論:
  DES-001 [FACT] engine H=8m
  DES-002 [DRV]  exhaust ≈ engine×3（高さも同等と仮定）
  SALES-002 [OBS] tunnel Ø=14m
  → 垂直配置: 8m + 8m = 16m > 14m → ◇Conflict

  ただし:
  ・排気系は必ずしも上方配置ではない
  ・横配置、別区画、坑口配置の可能性
  ・DES-002は[DRV]（概算）

計画:
  宛先: 設計（伊藤・渡辺）
  依頼: トンネル断面図を入手し、3案（横並び/別区画/坑口）のレイアウトスタディ
  前提: 営業がトンネル断面図をトルコ代理店経由で取得
  期限: 概念設計2週間（高橋の宣言に準拠）
  HumanMatter: No（設計の通常業務）
```

---

### 計画B: 納期の全工程積み上げ

```
推論:
  SALES-005 [OBS] 施主希望: 6ヶ月
  MFG-001 [FACT]  製造LT: 4ヶ月（転用時）
  DES-003         防爆電装設計LT: 未見積
  MFG-003         認証取得LT: 未見積
  （据付LT）      未見積

  4m + ?m + ?m + ?m = ? vs 6m
  → 未見積の工程が3つ。合計が6ヶ月を超える可能性

  並行作業の可能性:
  ・防爆電装設計と本体製造を並行 → 圧縮可能
  ・認証は出荷後取得のスキームがあるかも
  ・据付はトルコ側作業の可能性

計画:
  宛先: 開発（山田）＋設計（高橋）＋製造（田辺）
  依頼: 全工程WBSを合同で作成。クリティカルパスを特定
  含めるべき工程:
    ・K社交渉（営業） → 転用可否の確定
    ・防爆電装設計（設計） → LT見積
    ・補機新製（製造） → 2ヶ月（確定済み）
    ・認証取得（開発） → LT見積（認証パス特定後）
    ・輸送＋現地据付 → トルコ側と調整
  HumanMatter: Yes — 納期が超過する場合の顧客交渉は営業判断
    エージェントは「超過の可能性」を示す。「遅れます」とは言わない
```

---

### 計画C: 「アンモニア＝クリーン」の信頼度修正

```
推論:
  SALES-003 [EST] 「NH3ならトンネル換気負荷が下がる」
  RES-001 [FACT]  NOx=200ppm（単気筒テスト）
  管理濃度 25ppm（日本基準。トルコ基準は未確認）

  200ppm >> 25ppm
  → CO2面: 正しい（CO2=0）
  → NOx面: 追加処理なしでは管理濃度を超える
  → SALES-003は「部分的にのみ成立」に格下げ

  短絡リスク:
  「アンモニア=クリーン=換気不要」と提案書に書くと
  納入後にNOx問題が発覚 → 信頼失墜

計画:
  宛先: 営業（小林）
  通知: SALES-003の信頼度注記
    「CO2排出ゼロは正しい。ただしNOx=200ppmは管理濃度25ppmを超える。
     SCR脱硝後の値は未確認。『換気が楽になる』はCO2面のみ成立。
     提案書には『NOx追加処理が必要』と明記すべき」

  宛先: 研究（佐々木）
  依頼: 多気筒でのNOx見込み値を推算（シミュレーション or スケーリング則）
        SCR処理後のNOx見込みを算出

  HumanMatter: 半分
    技術的事実の通知はエージェントが行う
    提案書にどう書くかは営業判断
```

---

### 計画D: K社交渉の準備

```
推論:
  MFG-001 [FACT+DRV] K向け同型機が組立70%。転用で4ヶ月
  MFG-001.conditions[0]: 「K社の了解」 — 未着手
  SALES-005 [OBS] 施主希望6ヶ月 → 転用でないと間に合わない可能性
  全レコード走査: K社交渉に関する行動記録 = 0件

  Go判断はまだ出ていない（経営会議は来週）
  しかしGoが出てからK社交渉を始めると遅い
  → 事前準備（K社の納期余裕の確認、代替案の検討）は今から可能

  K社が拒否した場合:
  ¬∃(AlternativePlan, if_K_refuses)
  → 新造6ヶ月（施主希望ギリギリ）or 中古エンジン調達（品質リスク）

計画:
  宛先: 営業（藤田 — K社担当）
  依頼:
    a) K社の納期状況を非公式に確認（「仮に納期変更があった場合…」）
    b) K社拒否時の代替シナリオを2案準備
       案1: 新造（LT=6ヶ月。施主希望ギリギリ）
       案2: 中古同型機の市場調査
    c) 経営判断会議までに上記を報告

  HumanMatter: Yes
    K社との関係は営業の専管事項
    エージェントは「交渉記録が0件」という事実と「Go後では遅い」という推論を示す
```

---

### 計画E: 認証パスの特定

```
推論:
  4つの独立ソースが同じ問題を指摘:
    AGENT-DISCOVERY-001.risks[R3]: 「認証不明」 [EST]（エージェント初期評価）
    DEV-004.unchecked: 「ATEX/IECExの適用範囲」（開発）
    DES-003.unchecked: 「トルコがATEX準拠か」（設計）
    MFG-003 [DRV]: 「船級認証はトンネル用に使えない可能性」（製造）

  しかし:
  ∀cert(CertificationScheme(cert) → ¬Identified(cert))
  → 「何の認証が必要か」すら特定されていない

  認証問題は「解決に時間がかかる」のではなく「何を解決すべきか不明」
  → 計画Bの全工程WBSにも認証LTが入れられない

計画:
  宛先: 開発（山田）＋営業（小林→トルコ代理店）
  依頼:
    a) トルコの産業設備認証制度を調査
       ・トルコはATEX指令を採用しているか
       ・トンネル内動力設備に固有の認証があるか
       ・施主（国営建設会社）が独自の安全基準を持っているか
    b) ドイツH社（TBMモータ元メーカー）がどの認証で納入したかを調査
       → 同じスキームに乗れる可能性
    c) 「認証不要」のスキーム（施主自己責任型、暫定使用許可）の存在を確認

  HumanMatter: Yes
    トルコ規制当局との公式接触は経営判断を含む
    エージェントは「認証パスが存在しない」という事実と調査候補3案を示す
```

---

### 計画F: 研究データの適用限界と提案書

```
推論:
  DEV-005 [DRV]: 中長期提案にNH3エンジンを含める
  DEV-003 [FACT]: TRL4
  RES-001 [FACT]: NOx=200ppm, limitations=[単気筒, 定常のみ, 過渡未測定]
  RES-003 [OBS]: 部分負荷で失火リスク, limitations=[多気筒不明, TBM負荷未取得]

  提案書の根拠:
  ・TRL4（単気筒テスト段階）
  ・NOxデータは単気筒・定常のみ
  ・TBM負荷パターンでの運転は未試験

  If(Proposal(NH3, to_customer) ∧ ¬Disclosed(limitations))
  then Risk(customer_misunderstanding, technology_maturity)

  逆に全部書くと:
  If(Disclosed(all_limitations))
  then ◇Perception(customer, "この技術は使えない")

計画:
  宛先: 営業（中村）＋開発（山田）
  判断依頼:
    提案書にTRL・limitationsをどこまで書くか

    案1: 全部書く
      「TRL4。単気筒テスト段階。多気筒実機は2027年6月。
       トンネル内運転は未検証。短期はディーゼルのみ」
      → 正直。信頼構築。ただし「使えない」と読まれるリスク

    案2: 段階的に書く
      「アンモニアエンジンは開発中。短期はディーゼルで対応し、
       中長期でアンモニアへの転換を提案」
      → TRLの数字を出さない。嘘はない。ただし情報の省略

    案3: 技術ロードマップとして書く
      「2027年Q2に多気筒実機完成予定。それまではディーゼル運転。
       アンモニア転換時の換気負荷削減効果は○○（CO2面）。
       NOx処理はSCRで対応（詳細設計は転換時に実施）」
      → 将来の価値を提示。現在の限界も示す。バランス型

  HumanMatter: Yes
    情報開示の範囲は営業戦略であり経営判断
    エージェントは3案を提示する。選ぶのは人間
```

---

### 計画の全体像

```
[08:30] 計画立案完了

入力:  23レコード / 27 unchecked / 7 conditions / 5 limitations
出力:  計画6件（A〜F）

                        宛先        HumanMatter
計画A 空間干渉         設計         No
計画B 納期積み上げ     開発+設計+製造  Yes（超過時の顧客交渉）
計画C NH3信頼度修正    営業+研究     半分（事実通知No、書き方Yes）
計画D K社交渉準備      営業         Yes（取引先関係）
計画E 認証パス特定     開発+営業     Yes（規制戦略）
計画F 提案書の限界明記  営業+開発     Yes（情報開示戦略）

経営判断会議（2026-05-26予定）の議題として上記を配布する
```

---

**信頼度**: [EST] — 架空シミュレーション
