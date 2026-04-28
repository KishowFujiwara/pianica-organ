# pianica-organ

ピアニカ・オルガン設計プロジェクト + フリーリード音響学研究

## 概要

ヤマハ ピアニカP-32Dを音源とした足踏み式リードオルガン（アップライトピアノ筐体、37鍵）の設計と、
その基盤となるフリーリード音響学の研究成果を集約するリポジトリ。

## 主要な発見

- ピアニカP-32Dは「振動板型エンクロージャ・スピーカー」
- 外部放射の95.2%はABS壁面由来 (C1+C2)、鍵盤穴経由 (A1) はわずか0.8%
- ABS底面(1,1)曲げモード 323Hz (E4近傍) が音色の核
- 22の振動伝達経路を同定・分類・定量分析

## 文書の積層構造

```
レイヤ1 (What)      : pianica_22paths_analysis.md       -- 22経路の同定と分類
レイヤ2 (How much)  : path_comprehensive_analysis.md    -- 5軸マトリクス数値計算
レイヤ3 (So what)   : pianica_p32d_acoustic_report.md   -- 観測->分析->評価->性質特定
レイヤ4 (Now what)  : design-verification-v1.md         -- v1/v2への適用と評価
レイヤ5 (New design): v3設計仕様書 (未着手)
```

## v3設計の方向性 (未着手)

- 方向A: ABS箱を木製cassottoに置換
- 方向B: 内壁ダンピング処置
- ハイブリッド: 中音域B + 低音域A

## 来歴

`KishowFujiwara/EngineringKnowlege` の `decoded/pianika-organ/` から分離独立。
