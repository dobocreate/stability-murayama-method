"""
計算モジュールのテストスクリプト
"""

import numpy as np
from murayama_calculator import MurayamaCalculator


def test_basic_calculation():
    """基本的な計算のテスト"""
    print("=== 基本計算テスト ===")
    
    # テストケース1: 標準的な地盤条件
    calculator = MurayamaCalculator(
        H=10.0,      # 切羽高さ 10m
        gamma=20.0,  # 単位体積重量 20 kN/m³
        phi=30.0,    # 内部摩擦角 30度
        c=20.0,      # 粘着力 20 kN/m²
        q=0.0        # 上載荷重なし
    )
    
    # 単一条件での計算
    r0 = 2.0
    theta = np.radians(30)
    P = calculator.calculate_required_pressure(r0, theta)
    print(f"r₀={r0}m, θ=30°での必要支保圧: {P:.2f} kN/m²")
    
    # パラメトリックスタディ
    results = calculator.parametric_study(
        r0_range=(0.5, 5.0),
        theta_range=(10, 60),
        n_points=10
    )
    
    print(f"\n最大必要支保圧: {results['max_P']:.2f} kN/m²")
    print(f"臨界条件: r₀={results['critical_r0']:.2f}m, θ={results['critical_theta_deg']:.1f}°")
    print(f"安全率: {results['safety_factor']:.2f}")
    print(f"安定性評価: {results['stability']}")
    

def test_with_surcharge():
    """上載荷重ありのテスト"""
    print("\n=== 上載荷重ありのテスト ===")
    
    calculator = MurayamaCalculator(
        H=10.0,
        gamma=20.0,
        phi=30.0,
        c=20.0,
        q=10.0  # 上載荷重 10 kN/m²
    )
    
    results = calculator.parametric_study(
        r0_range=(0.5, 5.0),
        theta_range=(10, 60),
        n_points=10
    )
    
    print(f"最大必要支保圧: {results['max_P']:.2f} kN/m²")
    print(f"安定性評価: {results['stability']}")


def test_soft_ground():
    """軟弱地盤のテスト"""
    print("\n=== 軟弱地盤のテスト ===")
    
    calculator = MurayamaCalculator(
        H=8.0,
        gamma=18.0,
        phi=20.0,
        c=10.0,
        q=0.0
    )
    
    results = calculator.parametric_study(
        r0_range=(0.5, 4.0),
        theta_range=(10, 50),
        n_points=10
    )
    
    print(f"最大必要支保圧: {results['max_P']:.2f} kN/m²")
    print(f"安定性評価: {results['stability']}")


def test_invalid_inputs():
    """不正な入力値のテスト"""
    print("\n=== 入力値検証テスト ===")
    
    # 負の切羽高さ
    try:
        calculator = MurayamaCalculator(H=-10.0, gamma=20.0, phi=30.0, c=20.0)
    except ValueError as e:
        print(f"期待通りのエラー: {e}")
    
    # 範囲外の内部摩擦角
    try:
        calculator = MurayamaCalculator(H=10.0, gamma=20.0, phi=95.0, c=20.0)
    except ValueError as e:
        print(f"期待通りのエラー: {e}")


if __name__ == "__main__":
    test_basic_calculation()
    test_with_surcharge()
    test_soft_ground()
    test_invalid_inputs()
    
    print("\n全てのテストが完了しました。")