"""
旧版と修正版の計算結果比較
"""

import numpy as np
from murayama_calculator import MurayamaCalculator  # 旧版
from murayama_calculator_revised import MurayamaCalculatorRevised  # 修正版


def compare_results():
    """同一条件での計算結果比較"""
    print("=== 旧版と修正版の比較 ===")
    
    # パラメータ（同一条件）
    H = 10.0  # 切羽高さ
    gamma = 20.0  # 単位体積重量
    phi = 30.0  # 内部摩擦角
    c_old = 20.0  # 粘着力（旧版: kN/m²）
    c_new = 20.0  # 粘着力（修正版: kPa = kN/m²なので同じ値）
    
    print(f"入力条件:")
    print(f"  H = {H} m")
    print(f"  γ = {gamma} kN/m³")
    print(f"  φ = {phi}°")
    print(f"  c = {c_old} kN/m² (旧版) / {c_new} kPa (修正版)")
    print()
    
    # 旧版の計算
    print("【旧版】")
    calc_old = MurayamaCalculator(H, gamma, phi, c_old, q=0)
    
    # r0とθの範囲を設定（旧版はr0も探索）
    results_old = calc_old.parametric_study(
        r0_range=(0.5, 5.0),
        theta_range=(20, 80),
        n_points=20
    )
    
    print(f"  最大必要支保圧: {results_old['max_P']:.3f} kN/m²")
    print(f"  臨界 r₀: {results_old['critical_r0']:.3f} m")
    print(f"  臨界 θ: {results_old['critical_theta_deg']:.1f}°")
    print(f"  安全率: {results_old['safety_factor']:.2f}")
    print(f"  安定性: {results_old['stability']}")
    print()
    
    # 修正版の計算
    print("【修正版】")
    calc_new = MurayamaCalculatorRevised(H, gamma, phi, c_new)
    
    # θのみ探索（r0は内部決定）
    critical_new = calc_new.find_critical_pressure(theta_range=(20, 80))
    
    print(f"  最大必要支保圧: {critical_new['max_P']:.3f} kN/m²")
    print(f"  臨界 θ_d: {critical_new['critical_theta_d_deg']:.1f}°")
    print(f"  対応する r₀: {critical_new['critical_geometry']['r0']:.3f} m")
    print(f"  安全率: {critical_new['safety_factor']:.2f}")
    print(f"  安定性: {critical_new['stability']}")
    print()
    
    # 差異の分析
    print("【差異分析】")
    p_ratio = critical_new['max_P'] / results_old['max_P'] if results_old['max_P'] != 0 else 0
    print(f"  支保圧比（修正版/旧版）: {p_ratio:.2f}")
    print(f"  θの差: {critical_new['critical_theta_d_deg'] - results_old['critical_theta_deg']:.1f}°")
    print(f"  r₀の差: {critical_new['critical_geometry']['r0'] - results_old['critical_r0']:.3f} m")
    print()
    
    # 特定条件での詳細比較
    print("【特定角度での詳細比較】")
    theta_test = 45.0
    theta_rad = np.radians(theta_test)
    
    # 旧版での計算（特定のr0を使用）
    r0_test = 2.0
    P_old = calc_old.calculate_required_pressure(r0_test, theta_rad)
    
    # 修正版での計算
    result_new = calc_new.calculate_support_pressure(theta_rad)
    P_new = result_new['P']
    r0_new = result_new['geometry']['r0']
    
    print(f"  θ = {theta_test}° での比較:")
    print(f"    旧版: r₀ = {r0_test} m → P = {P_old:.3f} kN/m²")
    print(f"    修正版: r₀ = {r0_new:.3f} m (自動決定) → P = {P_new:.3f} kN/m²")
    print()


def analyze_formula_differences():
    """計算式の違いを分析"""
    print("=== 計算式の主な違い ===")
    
    print("1. 初期半径 r₀:")
    print("   旧版: 入力パラメータとして与える（パラメトリックスタディで探索）")
    print("   修正版: 幾何の閉合条件から自動決定")
    print("      r₀ = H_f / [exp(θ_d·tanφ)·sin(φ+θ_d) - sinφ]")
    print()
    
    print("2. 支保圧の作用腕:")
    print("   旧版: H/2 （単純化）")
    print("   修正版: l_p = r₀·sinφ + H_f/2 （より正確）")
    print()
    
    print("3. 粘着抵抗モーメント:")
    print("   旧版: 数値積分による計算")
    print("   修正版: 閉形式 M_c = c(r_d² - r₀²)/(2tanφ)")
    print()
    
    print("4. 上載荷重:")
    print("   旧版: 入力値として直接指定")
    print("   修正版: 等価合力として内部計算")
    print("      q = (αB(γ - 2c/(αB)))/(2K·tanφ) × [1 - exp(-2KH/(αB)·tanφ)]")
    print()
    
    print("5. 自重の作用点:")
    print("   旧版: 数値積分による重心計算")
    print("   修正版: 三角形部分と曲線領域の合成重心（改良版）")
    print()


def sensitivity_comparison():
    """パラメータ感度の比較"""
    print("=== パラメータ感度の比較 ===")
    
    # 基準条件
    H = 10.0
    gamma = 20.0
    phi_base = 30.0
    c = 20.0
    
    # φの感度比較
    print("内部摩擦角 φ の感度:")
    phi_values = [20, 25, 30, 35, 40]
    
    for phi in phi_values:
        # 旧版
        calc_old = MurayamaCalculator(H, gamma, phi, c, q=0)
        results_old = calc_old.parametric_study((0.5, 5.0), (20, 80), 10)
        P_old = results_old['max_P']
        
        # 修正版
        calc_new = MurayamaCalculatorRevised(H, gamma, phi, c)
        critical_new = calc_new.find_critical_pressure()
        P_new = critical_new['max_P']
        
        print(f"  φ = {phi}°: 旧版 P = {P_old:.1f} kN/m², 修正版 P = {P_new:.1f} kN/m²")
    print()


if __name__ == "__main__":
    compare_results()
    print("\n" + "="*60 + "\n")
    
    analyze_formula_differences()
    print("\n" + "="*60 + "\n")
    
    sensitivity_comparison()