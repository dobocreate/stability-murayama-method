"""
安全率計算のデバッグテスト
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

# 計算機インスタンス
calculator = MurayamaCalculatorRevised(H_f, gamma, phi, coh, H, alpha, K, force_finite_cover=True)

# 臨界角度での計算
critical_result = calculator.find_critical_pressure()
print(f"臨界条件:")
print(f"  最大必要支保圧: P_max = {critical_result['max_P']:.3f} kN/m²")
print(f"  臨界角度: θ_d* = {critical_result['critical_theta_d_deg']:.1f}°")

# 安全率計算の詳細
sf_result = critical_result['true_safety_factor_result']
print(f"\n安全率計算詳細:")
print(f"  元の必要支保圧: {sf_result['original_P']:.3f} kN/m²")
print(f"  臨界低減係数: {sf_result['critical_reduction_factor']:.6f}")
print(f"  安全率: {sf_result['safety_factor']:.3f}")

# 低減履歴を表示
print(f"\n強度低減履歴:")
print(f"{'Factor':>10} {'coh (kPa)':>12} {'phi (deg)':>12} {'P (kN/m²)':>12}")
print("-" * 50)
for h in sf_result['reduction_history'][-5:]:  # 最後の5点を表示
    print(f"{h['factor']:>10.6f} {h['coh']:>12.2f} {h['phi_deg']:>12.2f} {h['P']:>12.2f}")

# 手動で安全率を確認
print(f"\n検証:")
print(f"  元のP > 0なので、強度を低減してP=0になる点を探す")
print(f"  低減係数 = {sf_result['critical_reduction_factor']:.6f}")
print(f"  安全率 = 1 / 低減係数 = 1 / {sf_result['critical_reduction_factor']:.6f} = {1.0/sf_result['critical_reduction_factor']:.3f}")