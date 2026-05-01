"""
中華式ピアニカ パワー収支再分配 検算スクリプト
(pianica_chinese_style_paths_analysis.md v1.3 第3.3節の数値根拠)

実行: python3 power_balance_chinese_style.py
"""

import math


def main():
    # === 物性値 ===
    rho_brass, E_brass = 8400, 100e9  # 真鍮（P-32D）
    rho_alu, E_alu = 2700, 70e9       # アルミ（CAHAYA）

    # === B1a 伝達効率比 ===
    Z_brass = math.sqrt(rho_brass * E_brass)
    Z_alu = math.sqrt(rho_alu * E_alu)
    ratio_B1a = Z_brass / Z_alu

    print("=" * 60)
    print("B1a伝達効率（プレート材質差）")
    print("=" * 60)
    print(f"Z_brass = {Z_brass/1e6:.2f} MPa·s/m")
    print(f"Z_alu   = {Z_alu/1e6:.2f} MPa·s/m")
    print(f"伝達効率比（CAHAYA/P-32D） = {ratio_B1a:.2f}")
    print(f"-> プレート振動エネルギー実質増 +30%（理論値+111%は非物理的）")

    # === B2 多段効率 ===
    print("\n" + "=" * 60)
    print("B2多段効率（並列副経路含む）")
    print("=" * 60)
    eta_p32d = 0.80
    eta_cahaya_main = 0.80 * 0.80     # 多段（プレート→枠→ケース）
    eta_cahaya_sub = 0.80              # 副経路（直接接触ガスケットレス）
    eta_cahaya_eff = max(eta_cahaya_main, eta_cahaya_sub)
    print(f"P-32D（1段、ガスケット介在）: {eta_p32d:.2f}")
    print(f"CAHAYA主経路（2段）: {eta_cahaya_main:.2f}")
    print(f"CAHAYA副経路（直接接触）: {eta_cahaya_sub:.2f}")
    print(f"CAHAYA実効（並列合成）: {eta_cahaya_eff:.2f}")
    print(f"効率比（CAHAYA/P-32D）= {eta_cahaya_eff/eta_p32d:.2f}")

    # === B4 / C1 実効放射 ===
    print("\n" + "=" * 60)
    print("B4面積比 + σ doubling -> 実効C1放射比")
    print("=" * 60)
    S_p32d_total = 720      # 6面 (cm²)
    S_cahaya_total = 405    # 5面 = 天井190 + 4側面215 (cm²)
    sigma_ratio = 2.0       # 第5.3節
    print(f"P-32D ABS面積総計: {S_p32d_total} cm² (6面)")
    print(f"CAHAYA ABS面積総計: {S_cahaya_total} cm² (5面)")
    print(f"面積比: {S_cahaya_total/S_p32d_total:.2f}")
    print(f"σ比: {sigma_ratio:.1f}")
    print(f"実効C1放射比: {(S_cahaya_total/S_p32d_total) * sigma_ratio:.2f}")

    # === 段階的パワー再分配 ===
    print("\n" + "=" * 60)
    print("CAHAYA パワー収支 段階計算")
    print("=" * 60)

    # P-32D基準値
    P_reed = 48168
    print(f"\n[Step 1] リード総出力 P_reed = {P_reed} μW")

    # Step 2: プレート振動エネルギー
    P_plate_p32d = 35000
    plate_increase = 1.30
    P_plate_cahaya = P_plate_p32d * plate_increase
    print(f"\n[Step 2] プレート振動エネルギー")
    print(f"  P-32D: {P_plate_p32d} μW")
    print(f"  CAHAYA: {P_plate_cahaya:.0f} μW (+30%, B1a効率増)")

    # Step 3: ABS到達エネルギー
    P_ABS_p32d = 25000
    P_ABS_cahaya = 30000  # +20% (B3消失とB2同等)
    print(f"\n[Step 3] ABS壁到達エネルギー")
    print(f"  P-32D: {P_ABS_p32d} μW")
    print(f"  CAHAYA: {P_ABS_cahaya} μW (+20%, B3消失とB2同等)")

    # Step 4: ABS到達後の分配
    print(f"\n[Step 4] ABS到達後の分配")
    print(f"  CAHAYA fractions: C1=65%, C2=22%, 内部減衰=13% (B6/C4=0%)")
    P_C1_cahaya = P_ABS_cahaya * 0.65
    P_C2_cahaya = P_ABS_cahaya * 0.22
    P_int_cahaya = P_ABS_cahaya * 0.13
    print(f"  C1: {P_C1_cahaya:.0f} μW")
    print(f"  C2: {P_C2_cahaya:.0f} μW")
    print(f"  ABS内部減衰: {P_int_cahaya:.0f} μW")

    # Step 5: 最終外部放射
    P_A1_cahaya = 168 * 1.10
    P_others = 40
    P_radiation_total = P_C1_cahaya + P_C2_cahaya + P_A1_cahaya + P_others
    P_internal_total = P_reed - P_radiation_total

    print(f"\n[Step 5] CAHAYA最終予測")
    print(f"  外部放射合計: {P_radiation_total:.0f} μW")
    print(f"    C1: {P_C1_cahaya:.0f}")
    print(f"    C2: {P_C2_cahaya:.0f}")
    print(f"    A1: {P_A1_cahaya:.0f}")
    print(f"    その他: {P_others}")
    print(f"  内部減衰合計: {P_internal_total:.0f} μW")
    print(f"  保存則: {P_radiation_total + P_internal_total:.0f} = {P_reed} ✓")

    print(f"\n  P-32D比 外部放射 +{(P_radiation_total/21008-1)*100:.1f}%")
    print(f"  P-32D比 内部減衰 {(P_internal_total/27160-1)*100:+.1f}%")

    # 感度分析
    print("\n" + "=" * 60)
    print("感度分析（不確実性範囲）")
    print("=" * 60)

    scenarios = [
        ("下限（保守）", 1.20, 0.85, 1.5, 7000),
        ("中央値（v1.2）", 1.30, 1.00, 2.0, 5000),
        ("上限（楽観）", 1.50, 1.10, 2.5, 3000),
    ]

    print(f"\n{'シナリオ':<14} {'plate増':<8} {'B2比':<8} {'σ比':<8} {'P_loss':<10} {'P_radiation'}")
    print("-" * 70)

    for name, p_inc, b2_ratio, s_ratio, p_loss in scenarios:
        P_plate = 35000 * p_inc
        # ABSへの伝達: プレート振動 - プレート損失（B3消失後の残存損失）
        P_ABS = (P_plate - p_loss) * 0.80 * b2_ratio
        # C1 fraction（σ_ratioを反映: σ大なら radiation fraction up）
        c1_frac = 0.50 + 0.075 * s_ratio  # σ=1.5→0.61, σ=2.0→0.65, σ=2.5→0.69
        c2_frac = 0.22
        P_C1 = P_ABS * c1_frac
        P_C2 = P_ABS * c2_frac
        P_rad = P_C1 + P_C2 + 185 + 40
        print(f"{name:<14} +{(p_inc-1)*100:.0f}%     {b2_ratio:.2f}    {s_ratio:.1f}    {p_loss}    {P_rad:.0f} μW (+{(P_rad/21008-1)*100:.0f}%)")


if __name__ == "__main__":
    main()
