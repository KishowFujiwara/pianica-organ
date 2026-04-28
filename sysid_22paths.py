"""
22振動伝達経路 システム同定
入力: u(t) = リード変位 x_reed(t)
出力: y(t) = 外部音圧 p_ext(t)

各経路を伝達関数 G_i(s) でモデル化:
- 1次系 (low-pass): G(s) = K / (τs + 1)
- 2次共振系: G(s) = K ω_n² / (s² + 2ζω_n s + ω_n²)
- 遅延要素: G(s) = e^(-Ls) ≈ Padé近似

22経路を並列接続として全体伝達関数を構成
"""
import numpy as np
import control as ct
import json

# =================================================
# Phase A: 各経路の伝達関数同定
# =================================================

# 物理パラメータ (前レポートと整合)
def second_order(K, omega_n, zeta):
    """2次共振系の伝達関数を返す"""
    num = [K * omega_n**2]
    den = [1, 2*zeta*omega_n, omega_n**2]
    return ct.tf(num, den)

def first_order(K, tau):
    """1次遅れ系"""
    return ct.tf([K], [tau, 1])

def pade_delay(L, order=2):
    """Padé近似による遅延要素"""
    if L < 1e-6:
        return ct.tf([1], [1])
    return ct.tf(*ct.pade(L, order))

# 周波数 -> ω_n 変換
def fhz_to_wn(f):
    return 2 * np.pi * f

# Q -> ζ 変換
def Q_to_zeta(Q):
    return 1 / (2 * Q)

# === 22経路の伝達関数モデル ===
# 形式: 各経路 G_i = K_i × G_dynamic_i × delay_i

paths = {}

# A系列 (空気経由) - 主にHelmholtz共振や箱内伝搬
# A1: リード -> 箱内 -> 鍵盤穴 -> 外部
# Helmholtz共振 124Hz, Q=5
paths['A1'] = {
    'name': 'リード -> 箱内 -> 鍵盤穴 -> 外部',
    'K': np.sqrt(168e-6 / 48168e-6),  # パワー比から振幅ゲイン
    'fn_hz': 124, 'Q': 5, 'delay_ms': 0.07,
    'type': 'resonant_2nd', 'category': 'A'
}
# A2: 箱内空気 -> ABS壁面駆動
paths['A2'] = {
    'name': '箱内空気 -> ABS壁面 (音圧駆動)',
    'K': np.sqrt(8e-6 / 48168e-6),
    'fn_hz': 323, 'Q': 33, 'delay_ms': 0.07,
    'type': 'resonant_2nd', 'category': 'A'
}
# A3: バルブ振動
paths['A3'] = {
    'name': '箱内空気 -> 閉じたバルブ振動',
    'K': np.sqrt(0.5e-6 / 48168e-6),
    'fn_hz': 50, 'Q': 3, 'delay_ms': 0.07,
    'type': 'resonant_2nd', 'category': 'A'
}
# A4: パイプ逆流
paths['A4'] = {
    'name': '箱内 -> パイプ逆流 -> 奏者口腔',
    'K': np.sqrt(10e-6 / 48168e-6),
    'fn_hz': 200, 'Q': 8, 'delay_ms': 0.5,
    'type': 'resonant_2nd', 'category': 'A'
}
# A5: 箱内定在波
paths['A5'] = {
    'name': '箱内定在波 -> 隣リード連成',
    'K': np.sqrt(3e-6 / 48168e-6),
    'fn_hz': 536, 'Q': 15, 'delay_ms': 0.1,
    'type': 'resonant_2nd', 'category': 'A'
}

# B系列 (固体伝導)
# B1a: リード -> リベット -> リードプレート (固体直接, 超低損失)
paths['B1a'] = {
    'name': 'リード -> リベット -> リードプレート',
    'K': np.sqrt(30000e-6 / 48168e-6),
    'fn_hz': 440, 'Q': 1000, 'delay_ms': 0.001,
    'type': 'resonant_2nd', 'category': 'B'
}
# B1b: リード -> スロット隙間空気 -> プレート
paths['B1b'] = {
    'name': 'リード -> スロット隙間空気 -> プレート面',
    'K': np.sqrt(18000e-6 / 48168e-6),
    'fn_hz': 880, 'Q': 30, 'delay_ms': 0.05,
    'type': 'resonant_2nd', 'category': 'B'
}
# B2: ネジ経由
paths['B2'] = {
    'name': 'リードプレート -> ネジ -> ABS上面',
    'K': np.sqrt(15000e-6 / 48168e-6),
    'fn_hz': 440, 'Q': 50, 'delay_ms': 0.01,
    'type': 'resonant_2nd', 'category': 'B'
}
# B3: パッキン経由
paths['B3'] = {
    'name': 'リードプレート -> パッキン -> ABS上面',
    'K': np.sqrt(10500e-6 / 48168e-6),
    'fn_hz': 440, 'Q': 20, 'delay_ms': 0.05,
    'type': 'resonant_2nd', 'category': 'B'
}
# B4: ABS全体振動 (最重要)
paths['B4'] = {
    'name': 'ABS上面 -> 側面 -> 底面 (一体成型)',
    'K': np.sqrt(25000e-6 / 48168e-6),
    'fn_hz': 323, 'Q': 33, 'delay_ms': 0.21,
    'type': 'resonant_2nd', 'category': 'B'
}
# B5: フレーム/鍵盤
paths['B5'] = {
    'name': 'ABS -> パッキン -> フレーム -> 鍵盤',
    'K': np.sqrt(200e-6 / 48168e-6),
    'fn_hz': 100, 'Q': 5, 'delay_ms': 0.5,
    'type': 'resonant_2nd', 'category': 'B'
}
# B6: 外装
paths['B6'] = {
    'name': 'ABS -> ネジ -> 外装カバー',
    'K': np.sqrt(1500e-6 / 48168e-6),
    'fn_hz': 250, 'Q': 20, 'delay_ms': 0.1,
    'type': 'resonant_2nd', 'category': 'B'
}
# B7: テーブル接触
paths['B7'] = {
    'name': '外装カバー -> テーブル/手',
    'K': np.sqrt(50e-6 / 48168e-6),
    'fn_hz': 150, 'Q': 3, 'delay_ms': 0.5,
    'type': 'resonant_2nd', 'category': 'B'
}

# C系列 (再放射)
paths['C1'] = {
    'name': 'ABS底面/側面振動 -> 外部空気 (主経路)',
    'K': np.sqrt(15000e-6 / 48168e-6),
    'fn_hz': 323, 'Q': 33, 'delay_ms': 0.0,
    'type': 'resonant_2nd', 'category': 'C'
}
paths['C2'] = {
    'name': 'ABS壁 -> 箱内再放射 -> 鍵盤穴',
    'K': np.sqrt(5000e-6 / 48168e-6),
    'fn_hz': 323, 'Q': 33, 'delay_ms': 0.10,
    'type': 'resonant_2nd', 'category': 'C'
}
paths['C3'] = {
    'name': '閉じたバルブ振動 -> 外部',
    'K': np.sqrt(0.2e-6 / 48168e-6),
    'fn_hz': 50, 'Q': 3, 'delay_ms': 0.0,
    'type': 'resonant_2nd', 'category': 'C'
}
paths['C4'] = {
    'name': '外装カバー振動 -> 外部',
    'K': np.sqrt(800e-6 / 48168e-6),
    'fn_hz': 250, 'Q': 20, 'delay_ms': 0.0,
    'type': 'resonant_2nd', 'category': 'C'
}
paths['C5'] = {
    'name': 'パイプ振動 -> 外部',
    'K': np.sqrt(30e-6 / 48168e-6),
    'fn_hz': 200, 'Q': 10, 'delay_ms': 0.0,
    'type': 'resonant_2nd', 'category': 'C'
}

# D系列 (フィードバック) - 別途記述
paths['D1'] = {
    'name': '箱内圧 -> リード (自励振動本体)',
    'K': 1.0,  # 単位ループゲイン
    'fn_hz': 440, 'Q': 100, 'delay_ms': 0.07,
    'type': 'feedback', 'category': 'D'
}
paths['D2'] = {
    'name': 'ABS壁 -> 箱内 -> リード (二次FB)',
    'K': 0.1,
    'fn_hz': 323, 'Q': 33, 'delay_ms': 0.20,
    'type': 'feedback', 'category': 'D'
}
paths['D3'] = {
    'name': 'リードプレート曲げ -> 隣リード',
    'K': 0.05,
    'fn_hz': 517, 'Q': 80, 'delay_ms': 0.001,
    'type': 'feedback', 'category': 'D'
}

# 各経路の伝達関数を構成
def build_tf(p):
    """経路パラメータから伝達関数を構成"""
    K = p['K']
    wn = fhz_to_wn(p['fn_hz'])
    zeta = Q_to_zeta(p['Q'])
    G_dyn = second_order(1.0, wn, zeta)  # ゲイン1の動特性
    G_delay = pade_delay(p['delay_ms'] * 1e-3, order=2)
    G = K * G_dyn * G_delay
    return G

print("=" * 70)
print("22経路 伝達関数モデル (Phase A)")
print("=" * 70)

tfs = {}
for pid, p in paths.items():
    G = build_tf(p)
    tfs[pid] = G
    print(f"\n[{pid}] {p['name']}")
    print(f"  カテゴリ: {p['category']}, 種別: {p['type']}")
    print(f"  K = {p['K']:.4e}, fn = {p['fn_hz']} Hz, Q = {p['Q']}, delay = {p['delay_ms']} ms")
    print(f"  zeta = {Q_to_zeta(p['Q']):.4f}, ωn = {fhz_to_wn(p['fn_hz']):.1f} rad/s")

# 統計
print("\n" + "=" * 70)
print("カテゴリ別統計")
print("=" * 70)
for cat in ['A', 'B', 'C', 'D']:
    cat_paths = [pid for pid, p in paths.items() if p['category'] == cat]
    print(f"  {cat}系列: {len(cat_paths)}経路 = {cat_paths}")

# JSON出力
result = {pid: {**p, 'zeta': Q_to_zeta(p['Q']), 'wn': fhz_to_wn(p['fn_hz'])} 
          for pid, p in paths.items()}
with open('/home/claude/sysid/identification_results.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# pickle で伝達関数群を保存 (Phase B以降で使う)
import pickle
with open('/home/claude/sysid/tfs.pkl', 'wb') as f:
    pickle.dump((paths, tfs), f)

print("\nPhase A 完了: 22経路の伝達関数モデル構築完了")
