# Session Journal: 2026-04-30 (Session F)
# Opus 4.6 -- 3楽器の共鳴構造 物理モデル比較

## セッション概要

ギター、グランドピアノ、バイオリンの共鳴構造を統一物理フレーム
ワークで比較分析。5層モデル(Source, Bridge, Soundboard, Cavity,
Radiation)で3楽器を定量的に記述し、ピアニカv3との対応を導出。

**核心的発見**: ピアニカv3の物理パラメータはバイオリンに最も近い。
連続励振 + 小型共鳴箱 + 空洞結合という構造類似性に加え、
T_coupling=97%という異常に高い結合率がピアニカ固有の優位性。

## 成果物

| # | ファイル | 内容 |
|---|---------|------|
| 1 | figures/three_instruments_resonance_cross_section.svg | 3楽器断面構造比較図 |
| 2 | figures/bridge_impedance_matching_model.svg | 駒インピーダンス整合モデル |
| 3 | figures/soundboard_gamma_helmholtz_comparison.svg | 共鳴板Gamma + ヘルムホルツ比較 |
| 4 | figures/unified_resonance_model_with_pianica.svg | 4楽器統一モデル(ピアニカ含む) |

## 物理モデル 5層構造

### Layer 1: 励振源 (Source)

弦振動の共通方程式:
```
f_n = (n / 2L) * sqrt(T / mu)
```

| 楽器 | 励振方法 | 倍音構造 | 持続性 |
|------|---------|---------|--------|
| Guitar | Pluck (impulse) | a_n ~ sin(n*pi*x0/L) / n^2 | 減衰 2-5s |
| Piano | Strike (impulse) | H(f) ~ sinc(f*tau) LP filter | 減衰 10-30s |
| Violin | Bow (continuous) | a_n ~ 1/n (Helmholtz motion) | 連続 |
| Pianica | Reed (continuous) | Dipole near-field | 連続 |

### Layer 2: 駒 (Bridge) -- インピーダンス変換

伝達率方程式:
```
T = 4*Z1*Z2 / (Z1 + Z2)^2
```

| 楽器 | Z_source | Z_board | Ratio | T |
|------|----------|---------|-------|---|
| Guitar | 0.3 Ns/m | 50 Ns/m | 1:170 | 2.3% |
| Piano | 1-20 Ns/m | 200 Ns/m | 1:10-200 | 2-30% |
| Violin | 0.15 Ns/m | 30 Ns/m | 1:200 | 2% |
| Pianica v3 | (ABS wall) | (kiri plate) | ~1:1 | 97% |

**設計パラドックス**: T が低いことは、弦楽器では意図的設計。
```
tau_decay = 2*m_string / (T * Z_bridge)
```
T が高すぎると弦エネルギーが即座に流出し音が消える。
ピアニカ/バイオリンは連続励振なのでこの制約なし。

### Layer 3: 共鳴板 (Soundboard)

モード方程式:
```
f_mn = (pi/2) * sqrt(D / (rho*h)) * ((m/a)^2 + (n/b)^2)
D = E*h^3 / (12*(1-nu^2))
```

放射効率パラメータ:
```
Gamma = eta * rho_mat * h / (rho_air * c)
eta_radiation = 1 / (1 + Gamma)
```

| 楽器 | Material | h [mm] | S [m^2] | f_11 [Hz] | Gamma | eta_rad |
|------|----------|--------|---------|-----------|-------|---------|
| Guitar | Spruce | 2.5 | 0.08 | 170 | 3.0 | 25% |
| Piano | Spruce | 8->5 | 2.0 | 45 | 1.5 | 40% |
| Violin | Spruce | 2.5 | 0.035 | 460 | 2.0 | 33% |
| Pianica v3 | Kiri | 2 | 0.09 | 96 | 1.8 | 36% |

### Layer 4: 空洞 (Cavity) -- ヘルムホルツ共鳴

```
f_H = (c / 2*pi) * sqrt(S_hole / (l_eff * V))
```

| 楽器 | V [L] | S_hole | f_H [Hz] | 役割 |
|------|-------|--------|----------|------|
| Guitar | 13 | 50 cm^2 | ~100 | 低域補完 (E2=82Hz) |
| Piano | (open) | N/A | N/A | 不要 (板面積2m^2で直接放射) |
| Violin | 2 | 18 cm^2 | ~290 | A0 body resonance |
| Pianica v3 | TBD | TBD | TBD | 実験で決定 |

### Layer 5: 統合 -- エネルギー収支

```
P_rad / P_input = T_coupling * eta_radiation
```

| 楽器 | T | eta_rad | Total | SPL @1m |
|------|---|---------|-------|---------|
| Guitar | 2.3% | 25% | 0.6% | 80-85 dB |
| Piano | 15% avg | 40% | 6.0% | 90-100 dB |
| Violin | 2% | 33% | 0.7% | 85-95 dB |
| Pianica v3 | 97% | 36% | 35% | 85 dB (est) |
| Pianica P-32D | 18% | 1% | 0.2% | 72 dB |

ピアニカv3の放射効率35%は全楽器中最高。
P-32D比 35/0.2 = 175x = +22dB の改善ポテンシャル。

## 核心的知見

1. **バイオリンが最も近い構造的アナログ**
   - 連続励振 + 小型共鳴箱 + 空洞結合
   - Sound post = ABS仕切り壁 (BN2経路)
   - Bass bar = 長手方向の構造リブ

2. **T_coupling=97%はピアニカ固有の優位性**
   - 弦楽器はサスティンのためにTを低く設計
   - フリーリードは連続励振なのでT制約なし
   - ABS-桐界面 T=97%は「構造的偶然」ではなく物理的必然

3. **桐はスプルースより優れた共鳴板材**
   - rho_kiri=280 < rho_spruce=400
   - rho*h: 桐2mm=560 vs スプルース2.5mm=1000
   - -> 桐の方が Gamma が低い = 放射効率が高い

4. **ヘルムホルツ共鳴の実験的検証が次の課題**
   - ギター/バイオリンは共鳴板面積が小さいため空洞共鳴で低域補完
   - ピアニカv3も板面積0.09m^2なので同じ手法が有効な可能性

## 知見の積層構造 (更新)

```
L7: Cross-instrument comparison [NEW]
    L7a: 5層統一モデル [完了]
    L7b: 3楽器パラメータ比較 [完了]
    L7c: バイオリン=最近傍同定 [完了]
    L7d: T_coupling優位性の理論的根拠 [完了]
```

## 申し送り事項

1. ヘルムホルツ共鳴ポートの設計 -- 桐箱にポートを開け、f_H を
   F3(175Hz)付近にチューニングする設計計算
2. バイオリンのsound post構造のピアニカへの応用可能性
3. 実験: CAHAYA改造 + Spectroid FFT測定
