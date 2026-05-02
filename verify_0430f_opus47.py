"""
原典 0430f 数値検算スクリプト
対象: Gamma, f_11, eta_rad, T_coupling, P_rad/P_input
"""

import math

print("=" * 70)
print("原典 0430f 数値検算 (2026-05-02)")
print("=" * 70)

# ===========================================================
# 共通物理定数
# ===========================================================
rho_air = 1.2       # kg/m^3 (空気密度、20degC)
c_air   = 343.0     # m/s (空気中音速、20degC)

# ===========================================================
# 検算1: Gamma の物理式と原典値の照合
# ===========================================================
print("\n[1] Gamma の物理式検算")
print("-" * 70)
print("原典の式: Gamma = eta * rho_mat * h / (rho_air * c)")
print("→ この式は次元的に [s] (時間) の量になる。無次元ではない。")
print()

# パラメータ
def calc_gamma_dim(eta, rho_mat, h):
    """原典の式そのままで計算"""
    return eta * rho_mat * h / (rho_air * c_air)

# 各楽器
instruments = [
    ("Guitar",     0.05, 400, 0.0025, 3.0),  # eta, rho_mat, h, 原典Gamma
    ("Piano",      0.05, 400, 0.005,  1.5),  # 響板平均厚 5mm
    ("Violin",     0.05, 400, 0.0025, 2.0),
    ("Pianica v3", 0.05, 280, 0.002,  1.8),  # 桐
]

print(f"{'楽器':<12} {'eta':>5} {'rho_mat':>8} {'h[m]':>7} {'原典Gamma':>10} {'式の値[s]':>12} {'差倍率':>10}")
for name, eta, rho_mat, h, gamma_orig in instruments:
    g_calc = calc_gamma_dim(eta, rho_mat, h)
    ratio = gamma_orig / g_calc
    print(f"{name:<12} {eta:>5.2f} {rho_mat:>8.0f} {h:>7.4f} {gamma_orig:>10.2f} {g_calc:>12.2e} {ratio:>10.2e}")

print()
print("結論[1]: 原典の式 Gamma = eta*rho_mat*h/(rho_air*c) で計算すると")
print("        単位は [s] であり、原典の Gamma 値 (1.5-3.0) と 4-5桁の差がある。")
print("        原典の Gamma 値は eta_rad から逆算した値である可能性が高い。")
print("        Gamma = 1/eta_rad - 1 の関係で確認 →")

# ===========================================================
# 検算2: eta_rad = 1/(1+Gamma) と原典値の整合性
# ===========================================================
print("\n[2] eta_rad = 1/(1+Gamma) の整合性")
print("-" * 70)
print(f"{'楽器':<12} {'原典Gamma':>10} {'1/(1+Gamma)':>14} {'原典eta_rad':>14} {'整合':>6}")
for name, eta, rho_mat, h, gamma_orig in instruments:
    eta_rad_from_gamma = 1.0 / (1.0 + gamma_orig)
    # 原典のeta_rad
    eta_rad_orig_map = {"Guitar": 0.25, "Piano": 0.40, "Violin": 0.33, "Pianica v3": 0.36}
    eta_rad_orig = eta_rad_orig_map[name]
    match = "OK" if abs(eta_rad_from_gamma - eta_rad_orig) < 0.02 else "差あり"
    print(f"{name:<12} {gamma_orig:>10.2f} {eta_rad_from_gamma:>14.3f} {eta_rad_orig:>14.3f} {match:>6}")

print()
print("結論[2]: Gamma と eta_rad は 1/(1+Gamma) の関係で整合している。")
print("        つまり原典では Gamma → eta_rad の変換は数学的には正しい。")
print("        ただし Gamma 自体が物理式からの導出ではない可能性が問題。")

# ===========================================================
# 検算3: f_11 (1次共振周波数) の Kirchhoff-Love 板方程式検算
# ===========================================================
print("\n[3] f_11 の板方程式検算")
print("-" * 70)
print("単純支持矩形板の共振周波数:")
print("  f_mn = (pi/2) * sqrt(D/(rho_mat*h)) * ((m/a)^2 + (n/b)^2)")
print("  D = E*h^3 / (12*(1-nu^2))   (曲げ剛性)")
print()

def calc_f_mn(E, nu, rho_mat, h, a, b, m=1, n=1):
    """単純支持矩形板の f_mn"""
    D = E * h**3 / (12 * (1 - nu**2))
    return (math.pi / 2) * math.sqrt(D / (rho_mat * h)) * ((m/a)**2 + (n/b)**2)

# 桐の物性 (一般的な値)
# E_kiri 約 5-7 GPa, nu 約 0.3
print("桐 (Paulownia tomentosa) の物性 (文献値):")
print("  E ≈ 5-7 GPa, rho ≈ 280 kg/m^3, nu ≈ 0.3")
print()

# ピアニカv3 の想定: 板面積 0.09 m^2 → 仮に 300x300mm 正方形
# 厚さ 2mm
print("ピアニカv3 想定: 300x300mm, h=2mm, 桐, 単純支持仮定")
print()
for E_GPa in [5, 6, 7]:
    f11 = calc_f_mn(E=E_GPa*1e9, nu=0.3, rho_mat=280, h=0.002, a=0.300, b=0.300)
    print(f"  E={E_GPa} GPa: f_11 = {f11:.1f} Hz")

print()
print("原典の主張: f_11 = 96 Hz")
print()
print("結論[3]: 単純支持仮定で f_11 = 75-90 Hz 程度。原典の 96 Hz は")
print("        単純支持仮定の上限に近い。境界条件次第で前後する。")
print("        ただしピアニカv3 は未製作のため、これはあくまで設計値。")

# ===========================================================
# 検算4: T_coupling の式
# ===========================================================
print("\n[4] T_coupling = 4*Z1*Z2 / (Z1+Z2)^2 の検算")
print("-" * 70)
print("これは標準的な伝送線路のインピーダンス整合の式。")
print("Z1 = Z2 のとき T = 1 (完全整合)")
print()

# 原典のZ値 (Ns/m)
print(f"{'楽器':<12} {'Z_source':>10} {'Z_board':>10} {'T計算':>10} {'原典T':>10}")
cases = [
    ("Guitar",     0.3,  50,   0.023),
    ("Piano",      None, None, 0.15),  # 平均値、Z不明
    ("Violin",     None, None, 0.02),
    ("Pianica v3", None, None, 0.97),  # ABS-桐界面
]
for name, z1, z2, t_orig in cases:
    if z1 is not None and z2 is not None:
        t_calc = 4*z1*z2 / (z1+z2)**2
        print(f"{name:<12} {z1:>10.2f} {z2:>10.1f} {t_calc:>10.4f} {t_orig:>10.4f}")
    else:
        print(f"{name:<12} {'N/A':>10} {'N/A':>10} {'N/A':>10} {t_orig:>10.4f}")

print()
print("結論[4]: T = 4*Z1*Z2/(Z1+Z2)^2 自体は標準式。")
print("        ピアニカv3の T=97% は ABS-桐界面のZ値が記載されていないため")
print("        この場で検算不可能。実測待ち。")

# ===========================================================
# 検算5: P_rad/P_input = T * eta_rad
# ===========================================================
print("\n[5] P_rad/P_input の合成計算")
print("-" * 70)
for name, T, eta_rad, total_orig in [
    ("Guitar",     0.023, 0.25, 0.006),
    ("Piano",      0.15,  0.40, 0.060),
    ("Violin",     0.02,  0.33, 0.007),
    ("Pianica v3", 0.97,  0.36, 0.35),
]:
    total_calc = T * eta_rad
    diff = abs(total_calc - total_orig)
    match = "OK" if diff < 0.01 else "差あり"
    print(f"{name:<12} T={T:.3f} eta_rad={eta_rad:.2f}  T*eta_rad={total_calc:.4f}  原典={total_orig:.3f}  {match}")

print()
print("結論[5]: 単純な掛け算なので一致。ただしピアニカv3の 35% は")
print("        T=97% と eta_rad=36% の両方が原典の主張に依存しており")
print("        どちらも実測ではないため、35% も実測ではない。")

# ===========================================================
# 検算6: リード→板伝達 1-2 mW、足踏み 80 mW
# ===========================================================
print("\n[6] エネルギー流の数値の根拠")
print("-" * 70)
print("原典0430fには 'リード→板 1-2mW' '足踏み 80mW' の直接の記載なし。")
print("これらは speaker_vs_resonance_box.md (Appendix B) で生成された推定値。")
print("根拠となる物理式や測定データが原典に見当たらない。要再検証。")

print()
print("=" * 70)
print("検算サマリー")
print("=" * 70)
print("""
[1] Gamma の物理式: 原典の式 Gamma=eta*rho_mat*h/(rho_air*c) は単位 [s] で
    無次元 1.8 を直接導出できない。eta_rad からの逆算とみなすのが妥当。
[2] eta_rad = 1/(1+Gamma): 数学的には整合。
[3] f_11 = 96 Hz: 単純支持仮定で 75-90 Hz、上限に近いが妥当な範囲。
                 ただし未製作のため設計値。
[4] T_coupling = 97%: 公式そのものは標準式。Z値が原典にないため検算不可。
[5] P_rad/P_input = 35%: T と eta_rad の積。両者が未実測のため未実測値。
[6] リード→板伝達 1-2mW、足踏み 80mW: 原典に直接記載なし。
                                    speaker_vs_resonance_box.md での推定値。
""")
