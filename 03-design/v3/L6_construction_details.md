# L6 結合詳細 -- ギター製作1000年の暗黙知 + リードオルガン気密知識

**目的**: design-spec-v3 が「数値設計」段階で止まっていた部分を、製作直前に必要な接合・気密・組立順序の知識で埋める。
**対象**: 重要3項目 (リード気密 / X-brace接着順序 / サウンドホール補強)
**文献調査範囲**: フラットトップアコースティックギター製作実務 + 19世紀リードオルガン修復実務

---

## L6-1: リードプレート ↔ 共鳴箱 の気密 (リードオルガン流)

### 問題定義

ピアニカは「リードプレート ↔ 風箱(plenum)」の気密が必要。本機は鍵盤ユニット(CAHAYA流用)から共鳴箱14.2Lへ気流を導く際、**逆向きの問題**が発生する:

```
ピアニカ標準: 加圧空気 (口) -> 風箱 -> バルブ -> リード -> 外気
本機構成   : 加圧空気 (口) -> 風箱 -> バルブ -> リード -> 共鳴箱 -> SH+ボディ放射
```

リード下流側 (旧: 外気) が今度は **共鳴箱14.2L という閉空間**になる。気密はリード上流側(従来通り)とリード下流側(新規)の両方で必要。

### 文献からの知見

#### Reed Organ Society (R-1)

> 「ガスケットには soft leather (柔らかい革) が最適。paper や felt は porous (多孔性)で常に交換要。
> heavy blotting paper は使えるが、leather が真の解決。」
> 「ガスケットの繋ぎ目はほぼ見えないように。微小な不完全からも大量の wind が漏れる」

**翻訳**: フリーリード楽器の気密は革ガスケットが標準。フェルトは漏れる。継ぎ目の処理が決定的。

#### Organ Forum 2-Manual Harmonium (R-2)

> 「リード仕切り(partition)の縁に very thin leather (極薄革) をガスケットとして接着するのが通常」
> 「これらの仕切りは airtight に密閉しないと、別のランクへ漏れて音が損なわれる」

**翻訳**: ハルモニウムでは仕切り縁の革ガスケットが標準仕様。**極薄革(0.3-0.5mm)** が物理的に最適。

#### Reed Organ Restoration (R-3)

> 「Mason & Hamlin は風箱と bellows board を接着で固定したが、現代の修復では recommend されるのは **接着ではなくリーザー革ガスケット + ネジ留め**」

**翻訳**: 19世紀製造時点では接着が一般的だったが、修復時は革ガスケット+ネジに変更される。これは **メンテナンス性** を考慮した選択。本機はプロト段階で何度もリードプレートを取り外す必要があるため、**革ガスケット+ネジ留め一択**。

### 本機への適用

```
[リードプレート ↔ 共鳴箱 気密構造]

設計案 GA1: 革ガスケット + ネジ4本

  CAHAYA鍵盤ユニット側
       v
  [リードプレート]  <- 32鍵リード
       v
  [革ガスケット 0.5mm 黒色]  <- 上下面に圧縮力
       v
  [共鳴箱 Bridge patch (200x60x3mm 桐) のリードプレート用穴]
       v
  共鳴箱内部14.2L

  ネジ: M3 × 8mm 4箇所 (CAHAYA本体側のネジボス位置に整合)
  押え方向: 鍵盤ユニット側から共鳴箱側へ (上から下へ)
```

### 革ガスケット選定基準

| 項目 | 値 |
|---|---|
| 材質 | 鞣し革 (taned leather)、合皮は不可 (経年で硬化) |
| 厚み | 0.5mm (薄すぎると気密不足、厚すぎると圧縮過多) |
| 切り抜き形状 | リードプレート外形に合わせ + 穴部分を打ち抜き |
| 入手 | StewMac、東急ハンズ、革手芸店 |
| 接着 | ガスケット側にホットメルト極薄塗布 (粘着固定のみ、押圧は ネジで) |

### 注意点

1. **CAHAYAリードプレートのビス位置(L5実測項目A7)が決まらないと、ネジ穴位置が確定しない**
2. リード気密は「漏れゼロが理想」だが、現実は微小漏れあり。**0.1mm程度の漏れは許容**(リード励振に影響なし)
3. プロト段階では**シーリングテープ(マスキングテープ + スポンジ)で仮ガスケット**でも検証可。本格気密は最終組立時。

---

## L6-2: X-brace 接着順序 (Martin流)

### 問題定義

X-brace はトップ板の主骨格。接着順序を間違えると:
- アーチが正しく出ない (タップトーン悪化)
- 後から取り外せない (チューニング不可)

ギター製作1000年の暗黙知の核心領域。

### 文献からの順序集約

#### Westfarthing Woodworks (R-7)

```
1. ブレース位置を鉛筆で**マーク** (top板上)
2. **Bridge patch を最初に接着** (これが基準)
3. X-brace を**lap joint加工**して接着
4. Tone bar / finger brace を後から接着
5. すべて接着後に**carving (削り出し)** で形状調整
```

#### Eric Schaefer Guitars (R-3)

```
1. プレートを bookmatched 接着
2. ロゼッタ + サウンドホール加工
3. **X-brace のlap joint 加工** -> dry fit
4. **X-brace接着** (アーチを出す)
5. Bridge patch 接着 (X-brace のアーチ後)
6. Tone bar / finger brace 接着
7. Upper transverse bar 接着
8. すべての brace を carve (テーパー成形)
9. タップトーン調整
```

#### Acoustic Guitar Builder (Cumpiano流改変, R-2)

```
独自選択: X-brace を最初に接着 (Bridge patch より前)
理由: X-brace のアーチで top のドーム形状を確立してから、
他のブレースをそのカーブに合わせる方が確実
```

### 本機への適用 (推奨順序)

複数文献で意見が分かれるが、**初心者向け** には Westfarthing方式 (Bridge patch 先行) が安全。理由:

1. Bridge patch がリードプレート取付の基準点になる (本機特有)
2. X-brace は Bridge patch を**避けて配置**するため、後付けの方が衝突リスクが低い
3. アーチは本機ではフラット (curved soundboard ではなく flat) を採用、ドーミングは不要

```
[本機 X-brace 接着順序]

Step 1: トップ板を平面に固定 (work board)
Step 2: ブレース位置を鉛筆でマーク (F1 三面図参照)
Step 3: Bridge patch 接着 (200x60x3mm 桐)
        - リードプレートの取付穴に合わせ位置決め
        - エポキシ系接着剤 (Titebond は経年でクリープあり)
        - 24時間乾燥
Step 4: X-brace 加工
        - 8x12mm スプルース 2本を用意
        - 中央で**lap joint** をノミで切削 (角度90度)
        - dry fit で密着確認
Step 5: X-brace 接着 (左右同時 or 1本ずつ)
        - lap joint部分にエポキシ
        - クランプで圧着 (24時間)
        - 注: lap joint の交点に布パッチ + エポキシでさらに補強
              (Martin社製造ラインでは標準。 Bourgeois流は wood patch)
Step 6: Bass bar 接着 (8x12x400mm 中心から100mm低音側)
        - X-brace と平行 (干渉しないオフセット)
Step 7: Tone bar 接着 (8x12x300mm 中心から80mm高音側)
Step 8: タップトーン確認
        - トップ板の中央を指で軽く叩き、F4 (約350Hz) 近傍の音を聴取
        - スマホアプリ Spectroid で確認
        - 高すぎる → ブレースを削る
        - 低すぎる → 残念ながら別のブレース材で作り直し
Step 9: ブレース成形 (carving)
        - 端部を tapered (先細り) に削る
        - ピーク部の scalloping は推奨しない (dead zone 発生、R-2より)
        - 全体的に gentle parabola (ゆるやかな放物線) で削る
```

### lap joint 加工の注意

```
[X-brace 中央 lap joint 詳細]

  +-----+
  | 8mm |
  +-----+----+
  |   12mm  |
  |  ^^^^^  |  <- 上半分 (top側) 切除
  |  vvvvv  |  <- 下半分 (bottom側) 切除
  +---------+
       (両ブレース共通、6mmずつ重なる)

  注意:
  - sawcut は精度高く (ドブテイルソー推奨)
  - paring (ノミでの仕上げ) でぴったり嵌めるよう調整
  - lap jointが緩いと「entropic dissipation (エネルギー漏洩)」発生 (R-9)
```

---

## L6-3: サウンドホール補強

### 問題定義

サウンドホール(d=38mm)を切り抜くと、トップ板の繊維が断たれる。**応力集中 + 割れリスク**が発生。

### 文献からの知見

#### Stoll Guitars (R-18)

> 「ロゼッタは装飾だけでなく、内側の **sound hole reinforcement patch** と組み合わせて、
> サウンドホール周辺の rigidity を確保し、音波の transport を最適化する」

#### Jonathan Sevy (R-1)

> 「サウンドホール補強パッチは spruce で約 1/8" thick (= 3.2mm)、
> top材の余り (leftover material) を使う」

#### Delcamp Classical Forum (R-17)

> 「ロゼッタの veneer rings (突き板リング) は、繊維方向と直交するため、
> サウンドホール周辺の split (繊維割れ) を防ぐ」
> 「19世紀の楽器調査では、シンプルな ring inlay でも crack はほとんど発生していない」

### 本機への適用

```
[サウンドホール補強構造]

[トップ板 1.5mm 桐]
 上面: ロゼッタ装飾 (任意、本機では simple ring 推奨)
 下面: 補強パッチ (重要)

設計値:
  - サウンドホール直径: 38mm
  - 補強パッチ外径: 60mm
  - 補強パッチ内径: 38mm
  - 補強パッチ厚: 2mm 桐 (本機では top と同材で軽量化)
  - 接着: Titebond (薄塗り、24時間)
```

### 加工順序

```
Step 1: トップ板にサウンドホール中心をマーク
Step 2: 中心ピン穴を 3mm で開ける (circle cutting jig 用)
Step 3: ルーター + circle jig で外径 38mm 切り抜き
        - 切り抜き材は捨てない (補強パッチに使える)
Step 4: 補強パッチを別途切り出し
        - 外径 60mm、内径 38mm 円環
        - 材は Top と同じ桐 (柾目方向を Top と直交させる)
Step 5: 補強パッチをトップ板下面に接着
        - 接着剤: Titebond (薄塗り)
        - クランプ: 円形カウル + 中央を空けたクランプ
        - 24時間乾燥
Step 6: ロゼッタ装飾 (任意)
        - simple black ring (黒檀突き板) 1mm幅
        - サウンドホール外周に inlay
        - 装飾なしでも構造上問題なし

注意: 補強パッチを X-brace 接着前に取り付ける
      (X-brace の接着剤がパッチに被ると塗装時に問題)
```

### 重要な仕様変更

design-spec-v3 第2章2.3節の「サウンドホール補強 外径60 内径38 t=2mm 桐」は本文献調査と整合。**変更なし、設計通り採用**。

---

## L6 まとめ

### 設計仕様書への反映項目

design-spec-v3 への追記候補 (次セッションで整理):

```
[追記候補A] 第2章 2.5節 リードプレート配置 に「気密構造」サブセクション追加
  - 革ガスケット 0.5mm 黒色
  - M3 × 8mm ネジ4本 (CAHAYA本体ボス位置)
  - 仮組ではマスキングテープ + スポンジで代替可

[追記候補B] 第5章 5.2節 製作計画に「組立順序」サブセクション追加
  - Step 1-9 の X-brace 接着順序 (本ドキュメント L6-2 より)
  - タップトーンチェックを必須項目化

[追記候補C] 第6章 6.1節 製作前検証に追加項目
  - 革ガスケット材入手 (StewMac or 東急ハンズ)
  - lap joint 治具 (ドブテイルソー、ノミ、円形クランプ)
  - 円形ルータービット (38mm用 stewmac jig)
```

### L7 (製作工程) で次に詰めるべき項目

本ドキュメントは L6「結合詳細」止まり。L7「製作工程」で詰めるべき残課題:

1. **治具の設計**
   - X-brace 接着クランプ (どんな形状?)
   - サウンドホール ルーター jig (StewMac標準でOK?)
   - サイド板の bend (曲げ) 不要 (本機は矩形なので) -- 確認

2. **部材切り出し順序**
   - 桐板 1.5mm をどのサイズで購入し、どう切り出すか
   - スプルース ブレース材 8x12mm の歩留まり

3. **塗装・仕上げ**
   - 桐は通常無塗装 or 薄塗り
   - リードプレート周辺の塗装は ガスケット圧縮に影響しない厚みで

これらは L5 実測値が出揃った後、プロト製作と並行して詰める。

---

## 参照

### 一次文献 (Web)

- R-1: Jonathan Sevy, Building a Steel String Acoustic Guitar (Top Bracing)
- R-2: Acoustic Guitar Build Blogspot, Bracing the Soundboard
- R-3: Eric Schaefer Guitars, Building a Steel String Acoustic Guitar Step-by-step
- R-7: Westfarthing Woodworks, How to Make an Acoustic Guitar Series Part 4
- R-9: Edwinson Guitar, Soundboard Bracing and Tuning
- R-17: Delcamp Classical Guitar Forum, Soundhole Patch Discussion
- R-18: Stoll Guitars, Rosette and Sound Hole Reinforcement
- R-21: The Reed Organ Society, Reed Organ Repair
- R-22: Organ Forum, Two-manual Harmonium Discussion
- R-23: Daniel Graves, Restoring a Reed Organ Part 8

### 関連ドキュメント

- 本機設計: `../v3/design-spec-v3.md` (第2章 2.3節 ブレース構造、2.5節 リード配置)
- 図面: `../v3/figures/chapel_organ_v3/F2_brace_layout.svg`
- 製作前検証: `../v3/design-spec-v3.md` 第6章 6.1節
