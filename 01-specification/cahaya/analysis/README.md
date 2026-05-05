# Cahaya 中華ピアニカ 分析結果

**分析日**: 2026-05-05
**分析者**: Claude Opus 4.6

## レポート

- **harmonic_analysis_report.md** -- 倍音構造分析の包括レポート

## 分析図 (SVG)

| ファイル | 内容 |
|---|---|
| chinese_pianica_taped_harmonic_decay.svg | 5音(F3,C4,E4,F5,C6)の倍音減衰勾配の比較チャート |
| pianica_instrument_position_map.svg | 倍音特性空間上での楽器ポジションマップ(ピアニカ vs 管楽器) |
| valve_duty_cycle_mechanism.svg | バルブ全閉メカニズム(初期モデル、後に修正) |
| reed_Ag_ratio_corrected_model.svg | A/g比(振幅/スロット隙間比)による修正モデル(確定版) |

## 主要発見

1. 全音域で非整数ピーク皆無 -- ガムテープ養生によるQ低下の効果
2. C4で2次倍音 > 基音(+2dB) -- フリーリード整流効果の実測証拠
3. 倍音減衰勾配: F3 = -1.8 dB/次 → C6 = -9.5 dB/次
4. 原因はA/g比(リード先端振幅/スロット隙間)の音域依存性
5. ピアニカは音域でキメラ: 低音=リードオルガン的、中音=オーボエ的、高音=フルート的
