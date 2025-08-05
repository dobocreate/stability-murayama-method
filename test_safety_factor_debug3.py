"""
安全率の定義を確認するテスト
"""
import numpy as np
from murayama_calculator_revised import MurayamaCalculatorRevised

# テストパラメータ
H_f = 10.0
gamma = 20.0
phi = 30.0
coh = 20.0
H = 50.0
alpha = 1.8
K = 1.0

print("強度低減法の確認:")
print("F > 1: 強度低下（c' = c/F, tan(φ') = tan(φ)/F）")
print("F < 1: 強度増加（実際には使わない）")
print()

# 異なるFでの計算
print(f"{'F':>6} {'c (kPa)':>10} {'φ (deg)':>10} {'説明':>20}")
print("-" * 50)

for F in [0.5, 0.8, 1.0, 1.2, 1.5, 2.0]:
    c_reduced = coh / F
    tan_phi_reduced = np.tan(np.radians(phi)) / F
    phi_reduced_deg = np.degrees(np.arctan(tan_phi_reduced))
    
    if F < 1:
        desc = "強度増加"
    elif F == 1:
        desc = "元の強度"
    else:
        desc = "強度低下"
    
    print(f"{F:>6.1f} {c_reduced:>10.1f} {phi_reduced_deg:>10.1f} {desc:>20}")

print("\n実際の計算結果:")
# 計算機インスタンス
calculator = MurayamaCalculatorRevised(H_f, gamma, phi, coh, H, alpha, K, force_finite_cover=True)

# 臨界角度での計算
theta_d_rad = np.radians(53.0)

print(f"\n{'F':>6} {'c\' (kPa)':>10} {'φ\' (deg)':>10} {'P (kN/m²)':>12}")
print("-" * 40)

for F in [0.5, 0.8, 1.0, 1.2, 1.5, 2.0]:
    # 強度低減
    calculator.coh = coh / F
    calculator.phi = np.arctan(np.tan(np.radians(phi)) / F)
    calculator.phi_deg = np.degrees(calculator.phi)
    
    try:
        result = calculator.calculate_support_pressure(theta_d_rad)
        print(f"{F:>6.1f} {calculator.coh:>10.1f} {calculator.phi_deg:>10.1f} {result['P']:>12.2f}")
    except:
        print(f"{F:>6.1f} {calculator.coh:>10.1f} {calculator.phi_deg:>10.1f} {'Error':>12}")

print("\n結論:")
print("F < 1でP = 0になっている → 強度を増加させている")
print("正しい安全率 = 1/F = 1/0.718 = 1.39")