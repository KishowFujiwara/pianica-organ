# ピアニカP-32D 22振動伝達経路のシステム同定

**日付**: 2026年4月28日
**モデル**: Claude Opus 4.6
**前提文書**:
- pianica_22paths_analysis.md (22経路の物理記述)
- pianica_22paths_acoustic_analysis.md (包括的音響解析)
**手法**: PRODECOS CSTATE準拠の連続時間状態空間法
**目的**: 22経路の各々を伝達関数 $H_i(s)$ として同定し、全系のMIMOブロック線図を構築する

---

## 0. システム同定の枠組み

### 0.1 信号の定義

| 信号 | 記号 | 物理量 | 単位 |
|------|------|--------|------|
| リード先端変位 | $x(t)$ | 片持ち梁先端の振動変位 | m |
| リード先端速度 | $\dot{x}(t)$ | 速度 | m/s |
| 箱内音圧 | $p_i(t)$ | ABS箱内の音圧変動 | Pa |
| 壁面速度 | $v_w(t)$ | ABS壁面の法線方向速度 | m/s |
| リードプレート速度 | $v_p(t)$ | リードプレートの速度 | m/s |
| 穴からの体積速度 | $U_h(t)$ | 穴を通過する空気の体積流量 | m³/s |
| 外部音圧（穴経由） | $p_{A1}(t)$ | A1経路の放射音圧 | Pa |
| 外部音圧（壁経由） | $p_{C1}(t)$ | C1経路の放射音圧 | Pa |
| 外部音圧（合成） | $p_{ext}(t)$ | リスナー位置での合成音圧 | Pa |
| 駆動圧力 | $p_0$ | 呼気圧力（DC成分） | Pa |

### 0.2 同定の基本原理

各経路を **2次系（共振系）** または **1次系（RC的減衰系）** の縦続接続で近似する。物理的根拠:

- 音響共鳴（ヘルムホルツ、定在波）: 2次系
- 機械共振（壁モード、プレートモード）: 2次系
- 粘性減衰（管内損失、ゴムパッキン）: 1次系
- 放射（穴、壁面）: 周波数依存の利得

一般的な2次系の標準形:

$$H(s) = \frac{K \omega_n^2}{s^2 + 2\zeta\omega_n s + \omega_n^2}$$

$K$: 定常利得、$\omega_n$: 固有角振動数、$\zeta$: 減衰比

$Q$ 値との関係: $\zeta = 1/(2Q)$

### 0.3 Laplace変数の規約

$s = j\omega$ で周波数応答、$\omega = 2\pi f$ 。以下では $\omega_n$ を $\omega_0$ と書く場合がある（文脈による）。

---

## 1. 音源モデル: リード自励振動

### 1.1 リードの運動方程式

片持ち梁としてのリード振動:

$$m_{eff}\ddot{x} + r_{mech}\dot{x} + k x = F_{aero}(p_0, x, \dot{x})$$

空気力学的駆動力を線形化（$x = 0$ 付近）:

$$F_{aero} \approx k_a x - r_a \dot{x} + p_0 S_{slot} \alpha$$

$k_a$: 空気ばね効果、$r_a$: 空気力学的負性減衰、$\alpha$: 静圧感度

代入すると:

$$m_{eff}\ddot{x} + (r_{mech} - r_a)\dot{x} + (k - k_a) x = p_0 S_{slot} \alpha$$

**発振条件**: $r_a > r_{mech}$ のとき実効減衰が負になり、自励振動が持続する。

### 1.2 リード系の伝達関数（駆動圧力 -> リード変位）

線形化された伝達関数:

$$G_{reed}(s) = \frac{X(s)}{P_0(s)} = \frac{S_{slot} \alpha / m_{eff}}{s^2 + 2\zeta_{eff}\omega_r s + \omega_r^2}$$

ここで:

$$\omega_r = \sqrt{\frac{k - k_a}{m_{eff}}} \quad (\text{空気負荷込みの共振角周波数})$$

$$\zeta_{eff} = \frac{r_{mech} - r_a}{2 m_{eff} \omega_r} \quad (\text{自励振動時は負})$$

**注意**: $\zeta_{eff} < 0$ は不安定系を意味する。定常振動は非線形飽和（リードがスロットを完全に塞ぐ振幅制限）によって有限振幅に安定化される。線形モデルでは小信号近似としてのみ有効。

### 1.3 数値パラメータ（A4 = 440 Hz）

| パラメータ | 値 | 計算根拠 |
|-----------|-----|---------|
| $m_{eff}$ | $2.4 \times 10^{-6}$ kg | $0.24 \times \rho_{brass} L w h$ |
| $k$ | $18.4$ N/m | $m_{eff} \omega_r^2$, $\omega_r = 2\pi \times 440$ |
| $\omega_r$ | $2765$ rad/s | $2\pi \times 440$ |
| $r_{mech}$ | $6.6 \times 10^{-4}$ N·s/m | $2 m_{eff} \omega_r / Q_{reed}$, $Q_{reed} = 20$ |
| $r_a$ | $\approx 1.5 r_{mech}$ | 発振条件 $r_a > r_{mech}$ |
| $\zeta_{eff}$ | $-0.013$ | $(r_{mech} - r_a)/(2 m_{eff} \omega_r)$ |
| $S_{slot}$ | $8 \times 10^{-5}$ m² | $20 \times 4$ mm |
| 定常振幅 $x_0$ | $0.5$ mm | 実測概算 |

### 1.4 リードからの3つの出力

リード変位 $x(t)$ から3系統の音源出力が発生する:

**S1: 流量音源（体積速度）**

$$U_{reed}(s) = H_{S1}(s) \cdot X(s)$$

$$H_{S1}(s) = S_{slot} \cdot s \cdot g(x_0)$$

$g(x_0)$ はスロット遮蔽関数。線形化すると $g \approx w_{reed} / \delta_{gap}$（リード幅/隙間比）。

$$H_{S1}(s) = \frac{S_{slot} w_{reed}}{\delta_{gap}} \cdot s = K_{S1} \cdot s$$

$$K_{S1} = \frac{8 \times 10^{-5} \times 0.004}{0.0001} = 3.2 \times 10^{-3}\ \text{m²}$$

微分器 $s$ は流量が速度に比例することを反映。

**S2: クランプ反力（機械力）**

$$F_{clamp}(s) = H_{S2}(s) \cdot X(s)$$

$$H_{S2}(s) = m_{eff} s^2 + r_{mech} s + k = m_{eff}(s^2 + 2\zeta_{mech}\omega_r s + \omega_r^2)$$

入力がリード先端変位で、出力がクランプ点反力。梁の境界条件から:

$$H_{S2}(s) = m_{eff} \omega_r^2 \left(\frac{s^2}{\omega_r^2} + \frac{s}{Q_{reed}\omega_r} + 1\right)$$

低周波（$s \ll \omega_r$）では $H_{S2} \approx k = 18.4$ N/m（ばね的応答）。
高周波（$s \gg \omega_r$）では $H_{S2} \approx m_{eff} s^2$（慣性的応答）。

定常振動（$\omega = \omega_r$）でのクランプ力:

$$|F_{clamp}| = m_{eff} \omega_r^2 x_0 = 2.4 \times 10^{-6} \times 2765^2 \times 5 \times 10^{-4} = 9.2\ \text{mN}$$


**S3: スロット隙間音圧（近接場）**

$$P_{gap}(s) = H_{S3}(s) \cdot X(s)$$

隙間の圧力は体積速度と隙間面積の比:

$$H_{S3}(s) = \frac{\rho_0 c}{S_{gap}} \cdot H_{S1}(s) = \frac{\rho_0 c \cdot K_{S1}}{S_{gap}} \cdot s$$

$$S_{gap} = L_{slot} \times \delta_{gap} = 0.020 \times 0.0001 = 2 \times 10^{-6}\ \text{m²}$$

$$\frac{\rho_0 c \cdot K_{S1}}{S_{gap}} = \frac{411 \times 3.2 \times 10^{-3}}{2 \times 10^{-6}} = 6.6 \times 10^{5}\ \text{Pa/m}$$

---

## 2. A系列: 空気伝搬経路の伝達関数

### 2.1 A1: リード -> 箱内空気 -> 穴 -> 外部

A1は3つのサブシステムの縦続接続:

$$H_{A1}(s) = H_{box}(s) \cdot H_{hole}(s) \cdot H_{rad,hole}(s)$$

**サブシステム (a): リード流量 -> 箱内音圧（ヘルムホルツ共鳴器）**

箱を集中定数系（体積 $V$、頸部面積 $S_h$、頸部長 $L_{eff}$）として:

$$H_{box}(s) = \frac{P_i(s)}{U_{reed}(s)} = \frac{\rho_0 c^2 / V}{s^2 + \frac{R_h}{M_h}s + \frac{1}{M_h C_a}} = \frac{\rho_0 c^2 / V}{s^2 + 2\zeta_H \omega_H s + \omega_H^2}$$

音響質量: $M_h = \rho_0 L_{eff} / S_h$
音響コンプライアンス: $C_a = V / (\rho_0 c^2)$
音響抵抗: $R_h = \rho_0 c (k a_h)^2 / (2 S_h)$（放射抵抗）

$$\omega_H = \frac{1}{\sqrt{M_h C_a}} = c\sqrt{\frac{S_h}{V L_{eff}}} = 340\sqrt{\frac{50 \times 10^{-6}}{3.84 \times 10^{-4} \times 5 \times 10^{-3}}} = 2087\ \text{rad/s}$$

$$f_H = \omega_H / (2\pi) = 332\ \text{Hz}$$

$$Q_H = \frac{1}{R_h}\sqrt{\frac{M_h}{C_a}} \approx 10$$

$$\zeta_H = \frac{1}{2 Q_H} = 0.05$$

数値代入:

$$H_{box}(s) = \frac{3.06 \times 10^{8}}{s^2 + 209 s + 4.36 \times 10^{6}}\ \ [\text{Pa/(m³/s)}]$$


**サブシステム (b): 箱内音圧 -> 穴の体積速度**

$$H_{hole}(s) = \frac{U_h(s)}{P_i(s)} = \frac{1}{Z_{neck}(s)} = \frac{S_h}{\rho_0 L_{eff} s + R_h}$$

$$= \frac{S_h / (\rho_0 L_{eff})}{s + R_h / (\rho_0 L_{eff} / S_h)}$$

1次系（RL回路のアナロジー）。低周波で通過、高周波で減衰。

$$H_{hole}(s) = \frac{8.26 \times 10^{-3}}{s + 20.9}\ \ [\text{(m³/s)/Pa}]$$


**サブシステム (c): 穴の体積速度 -> 外部音圧**

距離 $r$ での放射音圧:

$$H_{rad,hole}(s) = \frac{P_{ext}(s)}{U_h(s)} = \frac{\rho_0}{4\pi r} \cdot s$$

モノポール放射。微分器 $s$ は放射音圧が体積加速度に比例することを反映。

距離 $r = 0.3$ m で:

$$H_{rad,hole}(s) = \frac{1.21}{4\pi \times 0.3} \cdot s = 0.321 s\ \ [\text{Pa/(m³/s)}]$$

**A1の合成伝達関数**:

$$H_{A1}(s) = H_{S1}(s) \cdot H_{box}(s) \cdot H_{hole}(s) \cdot H_{rad,hole}(s)$$

$$= K_{S1} s \cdot \frac{\rho_0 c^2/V}{s^2 + 2\zeta_H \omega_H s + \omega_H^2} \cdot \frac{S_h/(\rho_0 L_{eff})}{s + R_h/M_h} \cdot \frac{\rho_0}{4\pi r} s$$

分子の $s$ 因子を整理すると $s^2$ が含まれ、高域で利得が上昇する。

ただし実際にはリードの流量波形は非正弦波（スロット遮蔽の非線形性）であり、倍音成分のレベルは基音に対して -6 to -12 dB/octave で低下する。この非線形性は $H_{S1}$ のフーリエ級数展開で記述するのが正確だが、線形モデルでは各倍音を個別の正弦入力として扱う。


### 2.2 音源指向性モデル $\Gamma(\theta)$

22経路文書セクション2「フリーリードの指向性」のシステム同定的表現。

フリーリードは等方音源ではなく、**モノポール + ダイポールの混合音源**である。指向性係数 $\Gamma(\theta)$ は音源から各壁面への入力利得を決定し、A2（壁面駆動）の伝達関数に直接乗算される。

**ダイポール成分**: リードがスロットを上下に横切ることで、上面に正圧/下面に負圧が交互に生じる。放射パターンは:

$$p_{dipole}(\theta) \propto \cos\theta$$

$\theta$: リード振動方向（=鉛直）からの角度

**モノポール成分**: 圧力型リードの整流作用により、一方向にのみ有意な気流が通過する。このDC的な流量変調がモノポール放射を生む:

$$p_{monopole} \propto 1 \quad (\text{全方向一定})$$

**混合指向性**:

実測ではモノポール:ダイポール比は概ね 4:1 のパワー比（圧力型リード）。合成指向性:

$$\Gamma(\theta) = \alpha + (1-\alpha)\cos\theta, \quad \alpha \approx 0.8$$

$\alpha$: モノポール比率。$\alpha = 1$ で完全モノポール、$\alpha = 0$ で完全ダイポール。

**各壁面への指向性係数**:

| 壁面 | 方向角 $\theta$ | $\cos\theta$ | $\Gamma(\theta)$ | 物理的意味 |
|------|---------------|-------------|-----------------|----------|
| ABS上面 | 0° | +1.0 | **1.0** | ダイポール最大方向。穴あり |
| ABS底面 | 180° | -1.0 | **0.6** | ダイポール最大（逆位相）。密閉壁 |
| ABS側面 | 90° | 0.0 | **0.8** | ダイポールのヌル。モノポール成分のみ |

底面は $|\Gamma| = 0.6$ で上面 1.0 より小さいが、底面は**密閉壁で最大面積（192 cm²）**であり、上面は穴だらけで振動板として機能しない。結果として**底面が壁面放射（C1）の支配面**となる。

**吸引型リードでの変化**: 吸引型では整流作用が逆転し、モノポール成分が弱まる。$\alpha$ が 0.8 -> 0.5 程度に低下し、ダイポール指向性がより顕著になる。

### 2.3 A2: 箱内空気 -> ABS壁面振動

$$H_{A2}(s) = \Gamma(\theta_{wall}) \cdot \frac{V_w(s)}{P_i(s)}$$

指向性係数 $\Gamma(\theta)$ が乗算される。壁面ごとに分離して記述:

**A2-bottom: 底面駆動**（C1/C2 の主駆動源）

$$H_{A2,bottom}(s) = \Gamma(180°) \cdot \frac{1/m_s}{s^2 + 2\zeta_w \omega_w s + \omega_w^2} = \frac{0.6 / m_s}{s^2 + 2\zeta_w \omega_w s + \omega_w^2}$$

$m_s$ = 面密度 = 1.575 kg/m²
$\omega_w = 2\pi \times 309 = 1942$ rad/s（底面(1,1)モード）
$Q_w = 33$, $\zeta_w = 1/(2 \times 33) = 0.0152$

$$H_{A2,bottom}(s) = \frac{0.381}{s^2 + 59.0 s + 3.77 \times 10^{6}}\ \ [\text{(m/s)/Pa}]$$

**A2-side: 側面駆動**（C1 への寄与は小）

$$H_{A2,side}(s) = \Gamma(90°) \cdot \frac{1/m_{s,side}}{s^2 + 2\zeta_{w,side} \omega_{w,side} s + \omega_{w,side}^2} = \frac{0.8 / m_{s,side}}{s^2 + 2\zeta_{w,side} \omega_{w,side} s + \omega_{w,side}^2}$$

側面は面積が小さく（20 x 60 mm²）、モード周波数が高い。$\Gamma = 0.8$（モノポール成分のみ）だが面積比で底面の 1/16。C1 への寄与は底面の約 -20 dB 以下。

**A2 合成の壁面速度ピーク値**（底面共振時）:

$$|H_{A2,bottom}(j\omega_w)| = \frac{0.6}{m_s \cdot 2\zeta_w \omega_w} = \frac{0.6}{1.575 \times 59.0} = 6.45 \times 10^{-3}\ \text{(m/s)/Pa}$$

（指向性なしの前版 1.08 x 10⁻² と比較して 0.6 倍 = -4.4 dB の減少）

**テープ処置と指向性の関係**: テープが底面に貼られる理由は、$\Gamma(180°) = 0.6$ が低いからではなく、底面が「$\Gamma$ が有意 (0.6) + 密閉壁 + 最大面積」の3条件を同時に満たす唯一の面だからである。上面は $\Gamma = 1.0$ だが穴だらけで振動板にならない。側面は密閉だが面積が 1/16。


### 2.4 A3: 箱内空気 -> 閉じたバルブ振動

バルブ（ゴムパッキン付き）の応答:

$$H_{A3}(s) = \frac{1/m_{valve}}{s^2 + 2\zeta_v \omega_v s + \omega_v^2}$$

ゴムの高い内部損失により $Q_v \approx 3$, $\zeta_v = 0.17$。

バルブの共振周波数は高い（$f_v \approx 2-5$ kHz、軽量で硬い支持）ため、低中域での応答は質量則に従って減衰:

$$|H_{A3}(j\omega)| \approx \frac{1}{m_{valve} \omega^2} \quad (f \ll f_v)$$

$$H_{A3}(s) = \frac{1/m_{valve}}{s^2 + 2\zeta_v \omega_v s + \omega_v^2}$$

$m_{valve} \approx 0.5$ g = $5 \times 10^{-4}$ kg（1鍵分のバルブパッド）
$\omega_v = 2\pi \times 3000 = 18850$ rad/s

$$H_{A3}(s) = \frac{2000}{s^2 + 6410 s + 3.55 \times 10^{8}}\ \ [\text{(m/s)/Pa}]$$


### 2.5 A4: 箱内空気 -> パイプ -> 奏者の口

パイプは分布定数系（transmission line）だが、集中定数で近似:

$$H_{A4}(s) = \frac{e^{-s\tau_{pipe}}}{1 + Z_{pipe}(s) / Z_{mouth}(s)}$$

$\tau_{pipe} = L_{pipe}/c = 0.4/340 = 1.18$ ms（伝搬遅延）

管の入力インピーダンス（開端に近い口腔側）:

$$Z_{pipe}(s) = Z_0 \frac{\tanh(\gamma L)}{1} \approx Z_0 \gamma L \quad (\gamma L \ll 1)$$

$Z_0 = \rho_0 c / S_{pipe}$, $S_{pipe} = \pi (0.004)^2 = 5.03 \times 10^{-5}$ m²

$$Z_0 = 411 / (5.03 \times 10^{-5}) = 8.17 \times 10^{6}\ \text{Pa·s/m³}$$

低周波近似:

$$H_{A4}(s) \approx \frac{e^{-1.18 \times 10^{-3} s}}{1 + s/\omega_{pipe,1}}$$

$\omega_{pipe,1} = \pi c / L_{pipe} = \pi \times 340 / 0.4 = 2670$ rad/s ($f = 425$ Hz)

$$H_{A4}(s) = \frac{e^{-0.00118 s}}{1 + s/2670}\ \ [\text{Pa/Pa (圧力伝達)}]$$

この伝達関数は、A1系の箱内音圧がほとんど減衰せずにパイプを通過し、425 Hz で管共鳴が生じることを示す。


### 2.6 A5: 箱内定在波 -> 隣リード連成

定在波による隣接リードへの圧力は、箱のモーダルインピーダンスで記述:

$$H_{A5,n}(s) = \frac{\psi_n(x_{reed,1}) \cdot \psi_n(x_{reed,2})}{V} \cdot \frac{c^2}{s^2 + 2\zeta_n \omega_n s + \omega_n^2}$$

$\psi_n(x)$: $n$ 次モードのモード形状（$\cos(n\pi x / L_x)$）
$x_{reed,1}$, $x_{reed,2}$: 発音リードと受影響リードの位置

(1,0,0) モードの場合:

$$\omega_1 = \pi c / L_x = \pi \times 340 / 0.32 = 3338\ \text{rad/s} \quad (f = 531\ \text{Hz})$$

Q 値は壁面損失で決まり、$Q_1 \approx 50$, $\zeta_1 = 0.01$。

$$H_{A5,1}(s) = \frac{\cos(\pi x_1/L_x)\cos(\pi x_2/L_x)}{V} \cdot \frac{c^2}{s^2 + 66.8s + 1.11 \times 10^{7}}$$

リードが箱の中央（$x = L_x/2$）にある場合 $\cos(\pi/2) = 0$ で連成がゼロ。
リードが端部にある場合 $\cos(0) = 1$ または $\cos(\pi) = -1$ で最大連成。

---

## 3. B系列: 固体伝搬経路の伝達関数

### 3.1 B1a: リード -> リベット -> リードプレート

入力: リード先端変位 $x(t)$
出力: リードプレート速度 $v_p(t)$

クランプ力 $F_{clamp}$ がリードプレートのポイントインピーダンス $Z_p$ を駆動:

$$H_{B1a}(s) = \frac{V_p(s)}{X(s)} = \frac{H_{S2}(s)}{Z_p(s)}$$

リードプレート（真鍮板、厚さ 1 mm）のポイントインピーダンス:

$$Z_p = 2.3 m_p c_{bending} h_p \approx 2.3 \sqrt{\rho_{brass} h_p} \cdot \sqrt[4]{E_{brass} h_p^3 / 12}$$

無限板のポイントインピーダンスは周波数に依存しない定数（Cremer-Heckl-Ungar）:

$$Z_p = 2.3 \sqrt[4]{\frac{E_{brass}^3 h_p^5 \rho_{brass}^3}{12}} \cdot \frac{1}{\sqrt{12}}$$

しかし有限サイズのリードプレートではモード的応答になる。プレートの曲げモード:

$$f_{p,mn} = \frac{\pi}{2}\sqrt{\frac{D_p}{\rho_{brass} h_p}} \left[\left(\frac{m}{a_p}\right)^2 + \left(\frac{n}{b_p}\right)^2\right]$$

$D_p = E_{brass} h_p^3 / [12(1-\nu^2)]$, $a_p \approx 160$ mm（リベット間距離）, $b_p \approx 30$ mm

$$D_p = \frac{100 \times 10^9 \times (0.001)^3}{12 \times (1 - 0.34^2)} = \frac{0.1}{10.61} = 9.43 \times 10^{-3}\ \text{N·m}$$

$$f_{p,11} = \frac{\pi}{2}\sqrt{\frac{9.43 \times 10^{-3}}{8400 \times 0.001}} \left[\left(\frac{1}{0.16}\right)^2 + \left(\frac{1}{0.03}\right)^2\right]$$

$$= \frac{\pi}{2} \times 1.06 \times 10^{-3} \times (39.1 + 1111) = \frac{\pi}{2} \times 1.06 \times 10^{-3} \times 1150 = 1.91\ \text{Hz}$$

...この値は明らかに低すぎる。修正: $\sqrt{D_p / (\rho h_p)}$ の計算を再確認。

$$\sqrt{\frac{D_p}{\rho_{brass} h_p}} = \sqrt{\frac{9.43 \times 10^{-3}}{8400 \times 0.001}} = \sqrt{\frac{9.43 \times 10^{-3}}{8.4}} = \sqrt{1.12 \times 10^{-3}} = 0.0335\ \text{m²/s}$$

$$f_{p,11} = \frac{\pi}{2} \times 0.0335 \times 1150 = 60.5\ \text{Hz}$$

リードプレート (1,1) モードは約 **60 Hz**。これは可聴域の低端であり、リードの振動周波数（174-1397 Hz）よりはるかに低い。つまりリードの駆動周波数ではプレートは**質量制御領域**にある。

質量制御領域でのポイントインピーダンス:

$$Z_p \approx j\omega m_p \quad (f > f_{p,11})$$

$m_p = \rho_{brass} \times a_p \times b_p \times h_p = 8400 \times 0.16 \times 0.03 \times 0.001 = 0.040$ kg

周波数 440 Hz でのプレートインピーダンス:

$$|Z_p(440)| = 2\pi \times 440 \times 0.040 = 111\ \text{N·s/m}$$

しかし上記は板全体の質量。実際にはポイント力が加わる点近傍の有効質量はもっと小さい。無限板のポイントインピーダンス:

$$Z_{p,\infty} = 8\sqrt{D_p \rho_{brass} h_p} = 8\sqrt{9.43 \times 10^{-3} \times 8400 \times 0.001} = 8\sqrt{7.92 \times 10^{-2}} = 8 \times 0.281 = 2.25\ \text{N·s/m}$$

よってプレートの真のポイントインピーダンスは約 2.25 N·s/m で、**周波数に依存しない定数**（無限板の特徴的性質）。

$$H_{B1a}(s) = \frac{H_{S2}(s)}{Z_{p,\infty}} = \frac{m_{eff}(s^2 + 2\zeta_{mech}\omega_r s + \omega_r^2)}{2.25}$$

$$= \frac{2.4 \times 10^{-6}}{2.25}(s^2 + 138 s + 7.64 \times 10^{6})$$

$$= 1.07 \times 10^{-6}(s^2 + 138 s + 7.64 \times 10^{6})\ \ [\text{(m/s)/m}]$$

440 Hz では:

$$|H_{B1a}(j\omega_r)| = 1.07 \times 10^{-6} \times |j^2\omega_r^2 + 138 j\omega_r + \omega_r^2|$$
$$= 1.07 \times 10^{-6} \times |-\omega_r^2 + \omega_r^2 + 138 j\omega_r| = 1.07 \times 10^{-6} \times 138 \times 2765$$
$$= 1.07 \times 10^{-6} \times 3.82 \times 10^{5} = 0.408\ \text{(m/s)/m}$$

プレート速度 $v_p = 0.408 \times x_0 = 0.408 \times 0.0005 = 2.04 \times 10^{-4}$ m/s


### 3.2 B1b: リード -> スロット隙間空気 -> リードプレート面

入力: リード先端変位 $x(t)$
出力: リードプレート速度 $v_p(t)$（B1aと同じ出力点）

隙間音圧がプレート面を駆動する:

$$H_{B1b}(s) = H_{S3}(s) \cdot \frac{S_{face}}{Z_{p,\infty}} \cdot H_{distance}(s)$$

$S_{face}$: スロット周囲の受圧面積（$\approx 1$ cm² = $10^{-4}$ m²）
$H_{distance}$: 隙間からプレート面までの距離減衰（ニアフィールド、$\propto 1/r^2$）

$$H_{B1b}(s) = \frac{6.6 \times 10^5 s \times 10^{-4}}{2.25} \times 0.1 = 2.93 s\ \ [\text{(m/s)/m}]$$

（距離減衰係数 0.1 は隙間 0.1 mm からプレート面 1 mm への距離比の概算）

440 Hz では:

$$|H_{B1b}(j\omega_r)| = 2.93 \times 2765 = 8102\ \text{(m/s)/m}$$

これは B1a（0.408）よりはるかに大きい値だが、$H_{S3}$ の距離減衰の不確実性が大きい。実際にはニアフィールドの非線形性により、線形モデルの信頼性は低い。

**修正**: 上記の計算は隙間音圧の到達面積と距離減衰の精度に強く依存する。保守的に推定すると:

$$|H_{B1b}| \approx 0.3 \times |H_{B1a}| \quad (\text{at } 440 \text{ Hz})$$

高域（$f > 2$ kHz）では $H_{B1b}$ が $H_{B1a}$ を上回る。

### 3.3 B2: リードプレート -> ネジ -> ABS上面

$$H_{B2}(s) = \frac{V_{ABS,top}(s)}{V_p(s)}$$

ネジ結合はほぼ剛体的。ただしネジ位置のモード重なりで制限:

$$H_{B2}(s) = \eta_{overlap} \cdot \frac{Z_{p,\infty}}{Z_{p,\infty} + Z_{ABS,\infty}}$$

ABS壁のポイントインピーダンス:

$$Z_{ABS,\infty} = 8\sqrt{D_{ABS} \rho_{ABS} h_{ABS}} = 8\sqrt{0.737 \times 1050 \times 0.0015} = 8\sqrt{1.16} = 8.62\ \text{N·s/m}$$

$$H_{B2} = 0.7 \times \frac{2.25}{2.25 + 8.62} = 0.7 \times 0.207 = 0.145 \quad (-16.8\ \text{dB})$$

モード重なり係数 $\eta_{overlap} = 0.7$ はネジ4本のモード適合を反映。

$$H_{B2}(s) = 0.145 \quad [\text{周波数依存なし（ポイントインピーダンスが定数のため）}]$$


### 3.4 B3: リードプレート -> パッキン -> ABS上面

面接触（パッキン経由）:

$$H_{B3}(s) = \frac{K_{pad}}{K_{pad} + Z_{ABS,\infty} \cdot s}$$

紙パッキンの動的剛性 $K_{pad}$:

$$K_{pad} = E_{paper} \cdot \frac{S_{pad}}{h_{pad}} = 3 \times 10^9 \times \frac{2 \times 10^{-3}}{0.3 \times 10^{-3}} = 2 \times 10^{7}\ \text{N/m}$$

1次ローパスフィルタ:

$$H_{B3}(s) = \frac{1}{1 + s \cdot Z_{ABS,\infty} / K_{pad}} = \frac{1}{1 + s / \omega_{B3}}$$

$$\omega_{B3} = K_{pad} / Z_{ABS,\infty} = 2 \times 10^7 / 8.62 = 2.32 \times 10^6\ \text{rad/s} \quad (f_{B3} = 369\ \text{kHz})$$

カットオフ周波数が 369 kHz と非常に高いため、可聴域全体で $|H_{B3}| \approx 1$。

実効伝達率は、面接触の不均一性で **0.8** 程度に低下:

$$H_{B3}(s) \approx 0.8 \cdot \frac{1}{1 + s/\omega_{B3}} \approx 0.8 \quad (-1.9\ \text{dB})$$


### 3.5 B4: ABS上面 -> 側面 -> 底面

コーナー伝達の2段:

$$H_{B4}(s) = T_{corner}^2 \cdot e^{-\alpha_{wall} d_{wall}} \cdot e^{-s \tau_{wall}}$$

コーナー透過率: $T_{corner} \approx 0.6$ (-4.4 dB per corner)

壁面伝搬の減衰:

$$\alpha_{wall} = \frac{\pi f \eta_{ABS}}{c_{bending,ABS}}$$

ABS の曲げ波速:

$$c_{bending} = \sqrt{2\pi f} \cdot \sqrt[4]{\frac{D_{ABS}}{\rho_{ABS} h_{ABS}}} = \sqrt{2\pi f} \times 0.684$$

440 Hz で: $c_{bending} = \sqrt{2765} \times 0.684 = 52.6 \times 0.684 = 36.0$ m/s

$$\alpha_{wall}(440) = \frac{\pi \times 440 \times 0.03}{36.0} = 1.15\ \text{Np/m}$$

伝搬距離 $d_{wall} \approx 100$ mm で: $e^{-1.15 \times 0.1} = 0.891$ (-1.0 dB)

伝搬遅延: $\tau_{wall} = d_{wall} / c_{bending} = 0.1/36 = 2.8$ ms

合成:

$$H_{B4}(s) = T_{corner}^2 \cdot 0.891 \cdot e^{-0.0028 s}$$
$$= 0.36 \times 0.891 \times e^{-0.0028 s} = 0.321 \cdot e^{-0.0028 s}$$

$$H_{B4} = 0.321 \quad (-9.9\ \text{dB})$$

（遅延を除く。遅延は位相のみに影響。）


### 3.6 B5: ABS箱 -> フレームパッキン -> フレーム -> 鍵盤

$$H_{B5}(s) = \frac{1}{1 + s \cdot Z_{rubber} / K_{rubber}} \times T_{frame-key}$$

ゴムパッキンのダンピング:

$$Z_{rubber} = K_{rubber}(1 + j\eta_{rubber}) / (j\omega)$$

$\eta_{rubber} = 0.3$, $K_{rubber} \approx 5 \times 10^5$ N/m

可聴域での透過率: $|H_{B5}| \approx 0.15$ (-16.5 dB)

### 3.7 B6: ABS箱 -> ネジ -> 外装カバー

B2と同様のネジ結合。外装カバーは ABS 箱より薄い（$h \approx 1$ mm）ため:

$$Z_{cover,\infty} = 8\sqrt{D_{cover} \rho_{ABS} h_{cover}} \approx 5.0\ \text{N·s/m}$$

$$H_{B6} \approx \frac{Z_{ABS,\infty}}{Z_{ABS,\infty} + Z_{cover,\infty}} = \frac{8.62}{8.62 + 5.0} = 0.633 \quad (-4.0\ \text{dB})$$

### 3.8 B7: 外装カバー -> テーブル面/手

接触条件依存。テーブル上では:

$$H_{B7} = \frac{Z_{cover}}{Z_{cover} + Z_{table}} \approx 0.1-0.5 \quad (-6\ \text{to}\ -20\ \text{dB})$$

---

## 4. C系列: 再放射経路の伝達関数

### 4.1 C1: ABS底面・側面 -> 外部放射

入力: 壁面速度 $v_w(t)$
出力: 外部音圧 $p_{C1}(t)$

板の放射効率を含む伝達:

$$H_{C1}(s) = \frac{\rho_0 s \cdot \sigma(s) \cdot S_{bottom}}{4\pi r}$$

放射効率 $\sigma$ は周波数依存。$f < f_c$ では:

$$\sigma(f) \approx \frac{S_{bottom}}{2\lambda^2} = \frac{S_{bottom} f^2}{2c^2}$$

$$\sigma(f) = \frac{0.0192 \times f^2}{2 \times 340^2} = 8.31 \times 10^{-8} f^2$$

309 Hz での放射効率: $\sigma = 8.31 \times 10^{-8} \times 309^2 = 7.9 \times 10^{-3}$

伝達関数:

$$H_{C1}(s) = \frac{\rho_0 \sigma S_{bottom}}{4\pi r} \cdot s = \frac{1.21 \times 7.9 \times 10^{-3} \times 0.0192}{4\pi \times 0.3} \cdot s$$
$$= \frac{1.84 \times 10^{-4}}{3.77} \cdot s = 4.88 \times 10^{-5} s$$

共振ピーク込みの合成は A2 と C1 のカスケード:

$$H_{A2 \to C1}(s) = H_{A2}(s) \cdot H_{C1}(s) = \frac{0.635}{s^2 + 59.0 s + 3.77 \times 10^6} \times 4.88 \times 10^{-5} s$$

$$= \frac{3.10 \times 10^{-5} s}{s^2 + 59.0 s + 3.77 \times 10^6}$$


### 4.2 C2: ABS壁振動 -> 箱内再放射 -> 穴

壁面が箱内に放射する音圧 -> ヘルムホルツ共鳴器を経由して穴から放出:

$$H_{C2}(s) = H_{C1,int}(s) \cdot H_{box,internal}(s) \cdot H_{hole}(s) \cdot H_{rad,hole}(s)$$

箱内への再放射: $H_{C1,int}(s) = \rho_0 c \cdot \sigma_{int} \cdot s / V$ （箱の体積に注入）

$$H_{C2}(s) \approx H_{A2 \to C1}(s) \times \frac{S_{bottom}}{S_{hole}} \times \frac{V_{box}}{4\pi r^2}$$

C2 の利得は C1 と同程度だが、穴の放射条件が追加されるため周波数応答が異なる。


### 4.3 C3-C5: 微小放射経路

C3, C4, C5 はいずれも -40 dB 以下の微小経路。伝達関数は放射効率が非常に低い板振動のモデル:

$$H_{C3}(s) = H_{A3}(s) \times \sigma_{valve} \times \frac{\rho_0 S_{valve}}{4\pi r} \cdot s \approx 0 \quad (\text{negligible})$$
$$H_{C4}(s) \approx 0, \quad H_{C5}(s) \approx 0$$

---

## 5. D系列: フィードバック経路の伝達関数

### 5.1 D1: 自励振動ループ

D1 は伝達関数ではなく、**閉ループシステムの特性方程式**として記述する:

開ループ伝達関数:

$$L_{D1}(s) = G_{reed}(s) \cdot H_{aero}(s)$$

$H_{aero}(s)$: リード変位 -> 空気力学的力のフィードバック

$$H_{aero}(s) = -r_a s + k_a$$

閉ループ特性方程式:

$$1 + L_{D1}(s) = 0$$

$$m_{eff} s^2 + (r_{mech} - r_a)s + (k - k_a) = 0$$

根: $s = \sigma \pm j\omega_r$

$\sigma = -(r_{mech} - r_a)/(2m_{eff})$

$r_a > r_{mech}$ のとき $\sigma > 0$: 不安定（自励振動）

### 5.2 D2: ABS壁振動 -> 箱内 -> リード

帰還路伝達関数:

$$H_{D2}(s) = H_{C1,int}(s) \cdot H_{box}^{-1}(s) \cdot S_{slot}$$

壁の再放射がリードに圧力を加える:

$$H_{D2}(s) = \frac{\sigma_{int} \rho_0 c \cdot S_{bottom} \cdot S_{slot}}{V} \cdot \frac{\omega_w^2}{s^2 + 2\zeta_w \omega_w s + \omega_w^2}$$

数値計算:

$$K_{D2} = \frac{7.9 \times 10^{-3} \times 411 \times 0.0192 \times 8 \times 10^{-5}}{3.84 \times 10^{-4}} = \frac{5.00 \times 10^{-6}}{3.84 \times 10^{-4}} = 0.013$$

$$H_{D2}(s) = \frac{0.013 \times 3.77 \times 10^6}{s^2 + 59.0 s + 3.77 \times 10^6} = \frac{4.90 \times 10^4}{s^2 + 59.0 s + 3.77 \times 10^6}$$

共振ピークでの利得:

$$|H_{D2}(j\omega_w)| = \frac{4.90 \times 10^4}{59.0 \times 1942} = \frac{4.90 \times 10^4}{1.15 \times 10^5} = 0.43$$

**壁の共振周波数（309 Hz）では D2 の帰還利得が 0.43（-7.3 dB）**。これはリードの自励振動を有意に変調するレベル。E4 (330 Hz) が壁モードに近いため、E4 の音色が最も影響を受ける。

### 5.3 D3: リードプレート曲げ -> 隣リード

プレートの曲げ振動が隣接リードのクランプ剛性を変調:

$$H_{D3}(s) = \frac{\delta k_{clamp}(s)}{F_{reed,1}(s)} = \frac{Z_{p,rotational}}{Z_{p,\infty}} \cdot \psi_p(x_1) \cdot \psi_p(x_2)$$

$\psi_p$: プレートのモード形状

隣接リード間距離 $d_{reed} \approx 10$ mm での機械的クロストーク:

$$|H_{D3}| \approx e^{-k_{bending} d_{reed}} \approx e^{-0.5} = 0.61 \quad (\text{プレート内の曲げ波})$$

ただしこれは振動変位の伝達で、クランプ剛性の変調率は:

$$\frac{\delta k}{k} = \frac{v_{plate}}{c_{bending} \times (h_p/L_{reed})} \approx 0.001 \quad (-60\ \text{dB})$$

聴感上は無視可能だが、和音演奏時のうなり（ビーティング）の一因。

---

## 6. 全系のブロック線図（MIMO表現）

### 6.1 信号フローグラフ

22経路を結合した全系は、以下のMIMOシステムとして記述される:

**入力ベクトル**: $\mathbf{u} = [p_0]$ （駆動圧力、スカラー）

**状態ベクトル**: $\mathbf{x} = [x, \dot{x}, p_i, \dot{p}_i, v_w, \dot{v}_w, v_p, \dot{v}_p]^T$ （8状態）

**出力ベクトル**: $\mathbf{y} = [p_{A1}, p_{C1}, p_{C2}]^T$ （外部音圧3成分）

### 6.2 状態空間表現

$$\dot{\mathbf{x}} = \mathbf{A}\mathbf{x} + \mathbf{B}\mathbf{u}$$
$$\mathbf{y} = \mathbf{C}\mathbf{x} + \mathbf{D}\mathbf{u}$$

**$\mathbf{A}$ 行列（8x8）**:

状態変数の番号付け:
- $x_1 = x$（リード変位）, $x_2 = \dot{x}$
- $x_3 = p_i$（箱内音圧）, $x_4 = \dot{p}_i$
- $x_5 = v_w$（壁面変位）, $x_6 = \dot{v}_w$（壁面速度）
- $x_7 = v_{p,disp}$（プレート変位）, $x_8 = \dot{v}_{p,disp}$（プレート速度）

$$\mathbf{A} = \begin{pmatrix}
0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\
-\omega_r^2 & -2\zeta_{eff}\omega_r & a_{23} & 0 & 0 & 0 & 0 & 0 \\
0 & a_{32} & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & a_{42} & -\omega_H^2 & -2\zeta_H\omega_H & 0 & a_{46} & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\
0 & 0 & a_{63} & 0 & -\omega_w^2 & -2\zeta_w\omega_w & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \\
a_{81} & a_{82} & 0 & 0 & 0 & 0 & -\omega_p^2 & -2\zeta_p\omega_p
\end{pmatrix}$$

結合要素:
- $a_{23} = S_{slot}\alpha/m_{eff}$: 箱内圧力 -> リード（D1 + D2 帰還）
- $a_{32} = K_{S1} \cdot \rho_0 c^2 / V$: リード速度 -> 箱内音圧（S1 音源）
- $a_{42} = K_{S1} \cdot \omega_H^2$: リード速度 -> ヘルムホルツ応答
- $a_{46} = -\sigma_{int} \rho_0 c S_{bottom}/V$: 壁面速度 -> 箱内（C2 経路）
- $a_{63} = \Gamma(\theta_{bottom})/m_s$: 箱内音圧 -> 壁駆動（A2 経路、指向性込み）
- $a_{81} = m_{eff}\omega_r^2 / Z_{p,\infty}$: リード変位 -> プレート（B1a 経路）
- $a_{82} = m_{eff} 2\zeta_{mech}\omega_r / Z_{p,\infty}$: リード速度 -> プレート（B1a 経路）

### 6.3 数値A行列（A4 = 440 Hz 基準）

$$a_{23} = \frac{S_{slot}\alpha}{m_{eff}} = \frac{8 \times 10^{-5} \times 0.5}{2.4 \times 10^{-6}} = 16.7\ \text{s}^{-2}\text{Pa}^{-1} \times p_i$$

$$a_{32} = K_{S1} \cdot \frac{\rho_0 c^2}{V} = 3.2 \times 10^{-3} \times \frac{1.21 \times 340^2}{3.84 \times 10^{-4}} = 3.2 \times 10^{-3} \times 3.65 \times 10^{5} = 1168$$

$$a_{63} = \frac{\Gamma(\theta_{bottom})}{m_s} = \frac{0.6}{1.575} = 0.381$$

$$a_{81} = \frac{m_{eff}\omega_r^2}{Z_{p,\infty}} = \frac{2.4 \times 10^{-6} \times 7.64 \times 10^6}{2.25} = 8.15$$

$$a_{82} = \frac{m_{eff} \times 2\zeta_{mech}\omega_r}{Z_{p,\infty}} = \frac{2.4 \times 10^{-6} \times 138}{2.25} = 1.47 \times 10^{-4}$$

**$\mathbf{B}$ ベクトル（8x1）**:

$$\mathbf{B} = \begin{pmatrix} 0 \\ S_{slot}\alpha/m_{eff} \\ 0 \\ 0 \\ 0 \\ 0 \\ 0 \\ 0 \end{pmatrix} = \begin{pmatrix} 0 \\ 16.7 \\ 0 \\ 0 \\ 0 \\ 0 \\ 0 \\ 0 \end{pmatrix}$$

**$\mathbf{C}$ 行列（3x8）**:

$$\mathbf{C} = \begin{pmatrix}
0 & 0 & c_{13} & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & c_{26} & 0 & 0 \\
0 & 0 & c_{33} & 0 & 0 & c_{36} & 0 & 0
\end{pmatrix}$$

- $c_{13}$: 箱内音圧 -> A1 外部放射（穴経由）
- $c_{26}$: 壁面速度 -> C1 外部放射（壁面直接）
- $c_{33}$, $c_{36}$: C2（壁振動 -> 箱内 -> 穴）

**$\mathbf{D}$ 行列**: $\mathbf{D} = \mathbf{0}$（直達項なし）

---

## 7. 伝達関数行列

入出力の伝達関数行列 $\mathbf{G}(s) = \mathbf{C}(s\mathbf{I} - \mathbf{A})^{-1}\mathbf{B}$:

$$\mathbf{G}(s) = \begin{pmatrix} G_{A1}(s) \\ G_{C1}(s) \\ G_{C2}(s) \end{pmatrix}$$

### 7.1 $G_{A1}(s)$: 駆動圧力 -> 穴からの音圧

$$G_{A1}(s) = \frac{K_{A1} \cdot s^2}{(s^2 + 2\zeta_{eff}\omega_r s + \omega_r^2)(s^2 + 2\zeta_H \omega_H s + \omega_H^2)}$$

4次系。リード共振とヘルムホルツ共振の2つのピーク。

$K_{A1} = B_2 \times a_{32} \times c_{13}$

### 7.2 $G_{C1}(s)$: 駆動圧力 -> 壁面放射音圧

$$G_{C1}(s) = \frac{K_{C1} \cdot s^2}{(s^2 + 2\zeta_{eff}\omega_r s + \omega_r^2)(s^2 + 2\zeta_H \omega_H s + \omega_H^2)(s^2 + 2\zeta_w \omega_w s + \omega_w^2)}$$

6次系。リード共振 + ヘルムホルツ共振 + 壁モード共振の3つのピーク。

### 7.3 $G_{C2}(s)$: 駆動圧力 -> 壁経由穴放射音圧

$$G_{C2}(s) = \frac{K_{C2} \cdot s^3}{(s^2 + 2\zeta_{eff}\omega_r s + \omega_r^2)(s^2 + 2\zeta_H \omega_H s + \omega_H^2)(s^2 + 2\zeta_w \omega_w s + \omega_w^2)(s + \omega_{hole})}$$

7次系。C1 に穴の放射特性が加わる。

---

## 8. 経路別伝達関数パラメータ一覧

### 8.1 同定結果まとめ

| 経路 | 伝達関数の次数 | 極の数 | 零点の数 | 支配的な極 | DC利得 |
|------|-------------|--------|---------|----------|--------|
| A1 | 4次 | 4 | 2 | $\omega_r$, $\omega_H$ | 0 (微分系) |
| A2 | 2次 | 2 | 0 | $\omega_w$ | $1/m_s\omega_w^2$ |
| A3 | 2次 | 2 | 0 | $\omega_v$ | $1/m_v\omega_v^2$ |
| A4 | 1次 + 遅延 | 1 | 0 | $\omega_{pipe}$ | 1.0 |
| A5 | 2次(各モード) | 2/mode | 0 | $\omega_{n_x}$ | $\psi^2/(V\omega_n^2)$ |
| B1a | 2次 | 2 | 2 | $\omega_r$ | $k/Z_p$ |
| B1b | 1次 | 1 | 1 | (広帯域) | 0 (微分系) |
| B2 | 0次(定数) | 0 | 0 | -- | 0.145 |
| B3 | 0次(定数) | 0 | 0 | -- | 0.80 |
| B4 | 0次 + 遅延 | 0 | 0 | -- | 0.321 |
| B5 | 1次 | 1 | 0 | $\omega_{rubber}$ | 0.15 |
| B6 | 0次(定数) | 0 | 0 | -- | 0.633 |
| B7 | 0次(定数) | 0 | 0 | -- | 0.1-0.5 |
| C1 | 1次(微分) | 0 | 1 | -- | 0 |
| C2 | 2次 | 2 | 1 | $\omega_H$ | 0 |
| C3-C5 | -- | -- | -- | -- | ~0 |
| D1 | 閉ループ | 2 | 0 | $\omega_r$ (不安定) | -- |
| D2 | 2次 | 2 | 0 | $\omega_w$ | 0.013 |
| D3 | 伝搬型 | -- | -- | -- | ~0 |

### 8.2 python-control 実装パラメータ

```python
import control as ct
import numpy as np

# 物理定数
c = 340       # 音速 [m/s]
rho = 1.21    # 空気密度 [kg/m³]
rho_c = 411   # 特性インピーダンス [Pa·s/m]

# リード (A4 = 440 Hz)
m_eff = 2.4e-6   # 等価質量 [kg]
k_reed = 18.4    # ばね定数 [N/m]
w_r = 2765       # 共振角周波数 [rad/s]
Q_reed = 20
zeta_reed = 1/(2*Q_reed)  # 0.025 (機械的)
zeta_eff = -0.013          # 自励(負)
S_slot = 8e-5    # スロット面積 [m²]

# ヘルムホルツ
V_box = 3.84e-4  # 箱容積 [m³]
S_hole = 50e-6   # 穴面積 [m²]
L_eff = 5e-3     # 有効頸部長 [m]
w_H = 2087       # Helmholtz角周波数 [rad/s]
Q_H = 10
zeta_H = 1/(2*Q_H)  # 0.05

# ABS壁モード
w_w = 1942       # 壁(1,1)角周波数 [rad/s]
Q_w = 33
zeta_w = 1/(2*Q_w)  # 0.0152
m_s = 1.575      # 面密度 [kg/m²]
S_bottom = 0.0192  # 底面面積 [m²]

# 音源指向性（セクション2.2）
alpha_monopole = 0.8     # モノポール比率
Gamma_top    = alpha_monopole + (1 - alpha_monopole) * np.cos(0)         # 1.0
Gamma_bottom = alpha_monopole + (1 - alpha_monopole) * np.cos(np.pi)    # 0.6
Gamma_side   = alpha_monopole + (1 - alpha_monopole) * np.cos(np.pi/2)  # 0.8

# リードプレート
Z_plate = 2.25   # ポイントインピーダンス [N·s/m]

# 伝達関数の構築
# A1: リード -> 穴 -> 外部
num_reed = [S_slot*0.5/m_eff]
den_reed = [1, 2*zeta_eff*w_r, w_r**2]
G_reed = ct.tf(num_reed, den_reed)

# Helmholtz
num_helm = [rho*c**2/V_box]
den_helm = [1, 2*zeta_H*w_H, w_H**2]
G_helm = ct.tf(num_helm, den_helm)

# 壁応答 A2（指向性込み、底面）
num_wall = [Gamma_bottom / m_s]   # 0.6/1.575 = 0.381
den_wall = [1, 2*zeta_w*w_w, w_w**2]
G_wall = ct.tf(num_wall, den_wall)

# D2 帰還
K_D2 = 0.013
num_D2 = [K_D2 * w_w**2]
den_D2 = den_wall
G_D2 = ct.tf(num_D2, den_D2)
```

---

## 9. 全系の特性

### 9.1 固有値（極）の一覧

| 極 | 角周波数 [rad/s] | 周波数 [Hz] | 減衰比 $\zeta$ | Q | 物理的起源 |
|----|----------------|-----------|-------------|---|----------|
| $s_{1,2}$ | 2765 | 440 | -0.013 | -- | リード自励振動(不安定) |
| $s_{3,4}$ | 2087 | 332 | 0.050 | 10 | ヘルムホルツ共鳴 |
| $s_{5,6}$ | 1942 | 309 | 0.015 | 33 | ABS底面(1,1)モード |
| $s_{7,8}$ | 380 | 60 | 0.010 | 50 | リードプレート(1,1) |

不安定極 $s_{1,2}$ はリードの自励振動を表す。実際には非線形飽和で有限振幅に安定化される。線形モデルの有効範囲を超えるが、小信号解析と安定性判定には使える。

### 9.2 ナイキスト安定性（D1 + D2 ループ）

D2 帰還を含む開ループ伝達関数:

$$L(s) = G_{reed}(s) \cdot H_{aero}(s) \cdot (1 + \Gamma(\theta_{bottom}) \cdot H_{D2}(s))$$

壁モード $\omega_w$ = 1942 rad/s でのD2利得が 0.43 だが、壁振動の駆動に指向性係数 $\Gamma(180°) = 0.6$ が掛かるため:

$$|1 + \Gamma \cdot H_{D2}(j\omega_w)| = |1 + 0.6 \times 0.43| = |1 + 0.26| = 1.26 \quad (+2.0\ \text{dB})$$

指向性なし（$\Gamma = 1$）の +3.1 dB と比較して +2.0 dB に低下。壁帰還の実効的な影響は指向性によって -1.1 dB 緩和されている。

壁帰還がリードの発振条件を**強化**する方向に作用。リード基音が壁モードに近い音（E4 = 330 Hz）では、発振閾値が下がり、より弱い息で発音する。

逆に壁帰還の位相が反転する周波数（ヘルムホルツ共鳴の反共振帯域）では、発振が抑制される方向に作用する。

### 9.3 全系の周波数応答まとめ

外部リスナーへの総合伝達関数:

$$G_{total}(s) = G_{A1}(s) + G_{C1}(s) + G_{C2}(s)$$

この3項の重ね合わせで外部音圧が決まる。周波数応答の特徴:

- **100-250 Hz**: A1 のみが支配。ヘルムホルツの下裾
- **250-350 Hz**: A1 + C1 + C2 が競合。**壁共鳴帯域**。位相干渉でディップ/ピークが生じる
- **332 Hz**: ヘルムホルツピーク（A1 のピーク）
- **309 Hz**: 壁モードピーク（C1/C2 のピーク）。A1 と 23 Hz 離れておりビートが生じる
- **350-600 Hz**: A1 が支配に戻る。壁モードから離れる
- **531 Hz**: 箱内定在波(1,0,0)。A5 経由で微弱な連成
- **600 Hz 以上**: A1 が支配。倍音の自然減衰

---

## 10. テープ処置のシステム同定的解釈

テープ処置は、A行列の以下のパラメータを変更する操作として記述できる:

$$\mathbf{A}_{taped} = \mathbf{A}_{stock} + \Delta\mathbf{A}$$

変更される要素:
- $\omega_w$: 1942 -> 2049 rad/s (+5.5%)
- $\zeta_w$: 0.0152 -> 0.0179 (+18%)
- $m_s$: 1.575 -> 1.65 kg/m² (+4.8%)

これにより:
- C1, C2 のピーク周波数が 309 -> 326 Hz にシフト
- C1, C2 のピーク高さが -1.2 to -1.8 dB 低下
- C1, C2 のリンギング時間が 34 ms -> 28 ms に短縮
- D2 帰還の壁モードでの利得が 0.43 -> 0.37 に低下

A1 の伝達関数は変化しない。楽音本体はそのままで、壁由来の着色のみが変わる。
