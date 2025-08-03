"""
Excel M9値の直接確認とPython実装の比較
"""

import numpy as np
from murayama_calculator_revised import MurayamaCalculatorRevised

# テストケース2のパラメータ（新Excel）
params = {
    'H': 50,
    'gamma': 20,
    'c': 20,
    'phi_deg': 30,
    'H_f': 10,
    'theta_d_deg': 60
}

print("=== Excel値との直接比較 ===\n")

# 計算機インスタンス
calculator = MurayamaCalculatorRevised(
    H_f=params['H_f'],
    gamma=params['gamma'],
    phi=params['phi_deg'],
    coh=params['c'],
    H=params['H'],
    alpha=1.8,
    K=1.0,
    force_finite_cover=True
)

# θ_d = 60°での内部計算
theta_d_rad = np.radians(params['theta_d_deg'])
geom = calculator.calculate_geometry(theta_d_rad)
weight_params = calculator.calculate_self_weight(
    geom['r0'], geom['rd'], theta_d_rad, geom['B'], geom['la']
)

print("Python内部計算の値:")
print(f"B = {geom['B']}")
print(f"r0 = {geom['r0']}")
print(f"la = {geom['la']}")
print(f"w1 = {weight_params['w1']}")
print(f"lw1 = {weight_params['lw1']}")
print(f"w2 = {weight_params['w2']}")
print(f"lw2 = {weight_params['lw2']}")
print(f"lw = {weight_params['lw']}")

# Excel M9式が実際は異なる可能性を検証
print("\n=== 可能性のある別解釈 ===")

# 可能性1: Excelの実装にバグがある？
# 可能性2: Excel式の括弧の解釈が異なる？
# 可能性3: 単純な近似式を使っている？

# 近似式の可能性
phi_rad = np.radians(params['phi_deg'])
B = geom['B']
la = geom['la']
r0 = geom['r0']
rd = geom['rd']

# いくつかの近似式を試す
lw2_approx1 = la + B * 0.577  # 最適係数（テストケース1から）
lw2_approx2 = la + B * (1/np.sqrt(3))  # 1/√3 ≈ 0.577
lw2_approx3 = (la + B) * 0.577  # 別の形

print(f"近似式1: la + B * 0.577 = {lw2_approx1}")
print(f"近似式2: la + B * (1/√3) = {lw2_approx2}")
print(f"近似式3: (la + B) * 0.577 = {lw2_approx3}")

# 実際のExcel値
print(f"\nExcel lw2 = 3.758015139473548")

# 別の可能性：切羽中心からの相対位置
lw2_center = B/2 + la
print(f"\n切羽中心基準: B/2 + la = {lw2_center}")

# さらなる可能性：第1項のみ使用？
O = np.hypot(B, params['H_f'])
P = np.arctan2(params['H_f'], B)
S = np.sqrt((O**2)/4.0 + r0**2 - O*r0*np.cos(P + phi_rad))
R = r0 * np.sin(P + phi_rad)
T = np.arccos(R/S) - (P + phi_rad - np.pi/2)

lw2_term1_only = S * np.cos(phi_rad + T)
print(f"\n第1項のみ: S*cos(φ+T) = {lw2_term1_only}")

# 差の確認
print(f"\nExcel値との差:")
print(f"Python計算値 - Excel値 = {weight_params['lw2']} - 3.758 = {weight_params['lw2'] - 3.758}")