"""
安全率計算のデバッグテスト - 詳細版
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

print(f"初期パラメータ:")
print(f"  H_f = {H_f} m")
print(f"  γ = {gamma} kN/m³")
print(f"  φ = {phi}°")
print(f"  coh = {coh} kPa")
print(f"  H = {H} m")

# 計算機インスタンス
calculator = MurayamaCalculatorRevised(H_f, gamma, phi, coh, H, alpha, K, force_finite_cover=True)

# 臨界角度（53度）での直接計算
theta_d_rad = np.radians(53.0)
result = calculator.calculate_support_pressure(theta_d_rad)
print(f"\nθ_d = 53°での必要支保圧: P = {result['P']:.3f} kN/m²")

# 安全率計算の詳細確認
print(f"\n安全率計算のテスト:")
print(f"{'Factor':>8} {'coh':>8} {'phi':>8} {'P':>12}")
print("-" * 40)

# 手動で異なる係数での計算
for factor in [0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0, 5.0]:
    # 一時的に強度を変更
    temp_coh = coh * factor
    temp_phi = phi * factor
    
    temp_calculator = MurayamaCalculatorRevised(
        H_f, gamma, temp_phi, temp_coh, H, alpha, K, force_finite_cover=True
    )
    
    try:
        temp_result = temp_calculator.calculate_support_pressure(theta_d_rad)
        print(f"{factor:>8.1f} {temp_coh:>8.1f} {temp_phi:>8.1f} {temp_result['P']:>12.2f}")
    except Exception as e:
        print(f"{factor:>8.1f} {temp_coh:>8.1f} {temp_phi:>8.1f} {'Error':>12}")

print(f"\n期待される動作:")
print(f"- 係数 < 1.0: 強度が低下 → Pが増加（より不安定）")
print(f"- 係数 > 1.0: 強度が増加 → Pが減少（より安定）")
print(f"- ある係数でP = 0になる → それが安全率")