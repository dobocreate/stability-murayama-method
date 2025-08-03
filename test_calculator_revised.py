"""
修正版村山計算機のテストスクリプト
"""

import numpy as np
from murayama_calculator_revised import MurayamaCalculatorRevised


def test_basic_calculation():
    """基本的な計算のテスト"""
    print("=== 基本計算テスト ===")
    
    # テストパラメータ
    H_f = 10.0  # 切羽高さ [m]
    gamma = 20.0  # 単位体積重量 [kN/m³]
    phi = 30.0  # 内部摩擦角 [度]
    c = 20.0  # 粘着力 [kPa]
    
    # 深部前提（土被りなし）
    calculator = MurayamaCalculatorRevised(H_f, gamma, phi, c)
    
    # 特定角度での計算
    theta_d_deg = 45.0
    theta_d = np.radians(theta_d_deg)
    
    result = calculator.calculate_support_pressure(theta_d)
    
    print(f"入力パラメータ:")
    print(f"  H_f = {H_f} m")
    print(f"  γ = {gamma} kN/m³")
    print(f"  φ = {phi}°")
    print(f"  c = {c} kPa")
    print(f"  θ_d = {theta_d_deg}°")
    print()
    print(f"幾何パラメータ:")
    print(f"  r₀ = {result['geometry']['r0']:.3f} m")
    print(f"  r_d = {result['geometry']['rd']:.3f} m")
    print(f"  B = {result['geometry']['B']:.3f} m")
    print(f"  l_a = {result['geometry']['la']:.3f} m")
    print(f"  l_p = {result['geometry']['lp']:.3f} m")
    print()
    print(f"荷重パラメータ:")
    print(f"  q = {result['q']:.3f} kN/m²")
    print(f"  W_f = {result['Wf']:.3f} kN")
    print(f"  l_w = {result['lw']:.3f} m")
    print()
    print(f"抵抗パラメータ:")
    print(f"  M_c = {result['Mc']:.3f} kN·m")
    print()
    print(f"必要支保圧:")
    print(f"  P = {result['P']:.3f} kN/m²")
    print()


def test_critical_pressure():
    """臨界支保圧の探索テスト"""
    print("=== 臨界圧探索テスト ===")
    
    # テストパラメータ
    H_f = 10.0
    gamma = 20.0
    phi = 30.0
    c = 20.0
    
    calculator = MurayamaCalculatorRevised(H_f, gamma, phi, c)
    
    # 臨界圧の探索
    critical = calculator.find_critical_pressure(theta_range=(20, 80), theta_step=1.0)
    
    print(f"臨界条件:")
    print(f"  最大必要支保圧: P_max = {critical['max_P']:.3f} kN/m²")
    print(f"  臨界角度: θ_d* = {critical['critical_theta_d_deg']:.1f}°")
    print(f"  対応する r₀ = {critical['critical_geometry']['r0']:.3f} m")
    print(f"  安全率: {critical['safety_factor']:.2f}")
    print(f"  安定性評価: {critical['stability']}")
    print()


def test_finite_cover():
    """有限土被りの比較テスト"""
    print("=== 有限土被りテスト ===")
    
    H_f = 10.0
    gamma = 20.0
    phi = 30.0
    c = 20.0
    
    # 深部前提
    calc_deep = MurayamaCalculatorRevised(H_f, gamma, phi, c, C=None)
    critical_deep = calc_deep.find_critical_pressure()
    
    # 有限土被り（浅い）
    calc_shallow = MurayamaCalculatorRevised(H_f, gamma, phi, c, C=15.0)  # 1.5*H_f
    critical_shallow = calc_shallow.find_critical_pressure()
    
    # 有限土被り（深い）
    calc_medium = MurayamaCalculatorRevised(H_f, gamma, phi, c, C=50.0)
    critical_medium = calc_medium.find_critical_pressure()
    
    print(f"深部前提（C = ∞）:")
    print(f"  P_max = {critical_deep['max_P']:.3f} kN/m²")
    print(f"  θ_d* = {critical_deep['critical_theta_d_deg']:.1f}°")
    print()
    print(f"有限土被り（C = {15.0} m）:")
    print(f"  P_max = {critical_shallow['max_P']:.3f} kN/m²")
    print(f"  θ_d* = {critical_shallow['critical_theta_d_deg']:.1f}°")
    print()
    print(f"有限土被り（C = {50.0} m）:")
    print(f"  P_max = {critical_medium['max_P']:.3f} kN/m²")
    print(f"  θ_d* = {critical_medium['critical_theta_d_deg']:.1f}°")
    print()


def test_parameter_sensitivity():
    """パラメータ感度分析"""
    print("=== パラメータ感度分析 ===")
    
    # 基準パラメータ
    base_params = {
        'H_f': 10.0,
        'gamma': 20.0,
        'phi': 30.0,
        'c': 20.0
    }
    
    # 基準計算
    calc_base = MurayamaCalculatorRevised(**base_params)
    result_base = calc_base.find_critical_pressure()
    P_base = result_base['max_P']
    
    print(f"基準条件: P_max = {P_base:.3f} kN/m²")
    print()
    
    # 各パラメータの感度
    sensitivities = {
        'phi': [20, 25, 30, 35, 40],
        'c': [10, 15, 20, 25, 30],
        'gamma': [18, 19, 20, 21, 22]
    }
    
    for param, values in sensitivities.items():
        print(f"{param} の感度:")
        for value in values:
            params = base_params.copy()
            params[param] = value
            calc = MurayamaCalculatorRevised(**params)
            result = calc.find_critical_pressure()
            P = result['max_P']
            ratio = (P / P_base - 1) * 100 if P_base != 0 else 0
            print(f"  {param} = {value}: P = {P:.3f} kN/m² ({ratio:+.1f}%)")
        print()


def test_coefficient_effects():
    """係数α、Kの影響テスト"""
    print("=== 係数の影響テスト ===")
    
    H_f = 10.0
    gamma = 20.0
    phi = 30.0
    c = 20.0
    
    # 標準係数
    calc_standard = MurayamaCalculatorRevised(H_f, gamma, phi, c, alpha=1.8, K=1.0)
    result_standard = calc_standard.find_critical_pressure()
    
    # α の影響
    calc_alpha_low = MurayamaCalculatorRevised(H_f, gamma, phi, c, alpha=1.5, K=1.0)
    result_alpha_low = calc_alpha_low.find_critical_pressure()
    
    calc_alpha_high = MurayamaCalculatorRevised(H_f, gamma, phi, c, alpha=2.0, K=1.0)
    result_alpha_high = calc_alpha_high.find_critical_pressure()
    
    # K の影響
    calc_K_low = MurayamaCalculatorRevised(H_f, gamma, phi, c, alpha=1.8, K=0.8)
    result_K_low = calc_K_low.find_critical_pressure()
    
    calc_K_high = MurayamaCalculatorRevised(H_f, gamma, phi, c, alpha=1.8, K=1.2)
    result_K_high = calc_K_high.find_critical_pressure()
    
    print(f"標準係数（α=1.8, K=1.0）:")
    print(f"  P_max = {result_standard['max_P']:.3f} kN/m²")
    print()
    print(f"影響幅係数 α の影響:")
    print(f"  α = 1.5: P_max = {result_alpha_low['max_P']:.3f} kN/m²")
    print(f"  α = 1.8: P_max = {result_standard['max_P']:.3f} kN/m²")
    print(f"  α = 2.0: P_max = {result_alpha_high['max_P']:.3f} kN/m²")
    print()
    print(f"経験係数 K の影響:")
    print(f"  K = 0.8: P_max = {result_K_low['max_P']:.3f} kN/m²")
    print(f"  K = 1.0: P_max = {result_standard['max_P']:.3f} kN/m²")
    print(f"  K = 1.2: P_max = {result_K_high['max_P']:.3f} kN/m²")
    print()


if __name__ == "__main__":
    # 全テストの実行
    test_basic_calculation()
    print("\n" + "="*50 + "\n")
    
    test_critical_pressure()
    print("\n" + "="*50 + "\n")
    
    test_finite_cover()
    print("\n" + "="*50 + "\n")
    
    test_parameter_sensitivity()
    print("\n" + "="*50 + "\n")
    
    test_coefficient_effects()