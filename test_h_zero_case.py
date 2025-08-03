"""
H=0の場合のテスト（提案に基づく）
"""

import numpy as np
from murayama_calculator_revised import MurayamaCalculatorRevised

def test_h_zero_case():
    """H=0の場合のテスト"""
    
    # テストケース2のパラメータでH=0に設定
    params = {
        'H': 0,  # 土被りを0に設定
        'gamma': 20,
        'c': 20,
        'phi_deg': 30,
        'H_f': 10,
        'alpha': 1.8,
        'K': 1.0,
        'theta_d_deg': 60
    }
    
    print("=== H=0の場合のテスト ===")
    print(f"パラメータ: H={params['H']}, γ={params['gamma']}, c={params['c']}, φ={params['phi_deg']}°, H_f={params['H_f']}")
    
    # 計算機インスタンス
    calculator = MurayamaCalculatorRevised(
        H_f=params['H_f'],
        gamma=params['gamma'],
        phi=params['phi_deg'],
        coh=params['c'],
        H=params['H'],
        alpha=params['alpha'],
        K=params['K'],
        force_finite_cover=True
    )
    
    # 計算実行
    theta_d_rad = np.radians(params['theta_d_deg'])
    result = calculator.calculate_support_pressure(theta_d_rad)
    
    print("\n【計算結果】")
    print(f"B = {result['geometry']['B']:.10f}")
    print(f"q = {result['q']:.10f}")
    print(f"w1 = {result['w1']:.10f}")
    print(f"lw1 = {result['lw1']:.10f}")
    print(f"w2 = {result['w2']:.10f}")
    print(f"lw2 = {result['lw2']:.10f}")
    print(f"lw = {result['lw']:.10f}")
    
    # cos方向の確認
    B = result['geometry']['B']
    H_f = params['H_f']
    print(f"\n【cos方向の確認】")
    print(f"arctan2(B, H_f) = arctan2({B}, {H_f}) = {np.arctan2(B, H_f)} rad")
    print(f"arctan(B/H_f) = arctan({B}/{H_f}) = {np.arctan(B/H_f)} rad")
    print(f"cos(arctan2(B, H_f)) = {np.cos(np.arctan2(B, H_f))}")
    print(f"cos(arctan(B/H_f)) = {np.cos(np.arctan(B/H_f))}")
    
    # 深部判定の確認
    print(f"\n【深部判定の確認】")
    print(f"force_finite_cover = {calculator.force_finite_cover}")
    if params['H'] is None:
        print("H is None → 深部前提")
    else:
        print(f"H = {params['H']} → 有限土被り")
        print(f"1.5 * B = 1.5 * {B} = {1.5 * B}")
        print(f"H > 1.5 * B ? {params['H']} > {1.5 * B} ? {params['H'] > 1.5 * B}")

if __name__ == "__main__":
    test_h_zero_case()