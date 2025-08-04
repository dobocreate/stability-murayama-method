"""
新しい実装（分岐なし）のテスト
"""

import numpy as np
from murayama_calculator_revised import MurayamaCalculatorRevised

def test_new_implementation():
    """新しい実装のテスト"""
    
    # テストケース2のパラメータ
    params = {
        'H': 50,
        'gamma': 20,
        'c': 20,
        'phi_deg': 30,
        'H_f': 10,
        'alpha': 1.8,
        'K': 1.0,
        'theta_d_deg': 60
    }
    
    print("=== 新しい実装（分岐なし）のテスト ===\n")
    
    try:
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
        
        theta_d_rad = np.radians(params['theta_d_deg'])
        result = calculator.calculate_support_pressure(theta_d_rad)
        
        print("【計算結果】")
        print(f"  B = {result['geometry']['B']:.6f}")
        print(f"  q = {result['q']:.4f}")
        print(f"  w1 = {result['w1']:.4f}")
        print(f"  lw1 = {result['lw1']:.6f}")
        print(f"  w2 = {result['w2']:.4f}")
        print(f"  lw2 = {result['lw2']:.6f}")
        print(f"  lw = {result['lw']:.6f}")
        print(f"  Mc = {result['Mc']:.4f}")
        print(f"  P = {result['P']:.2f}")
        
        print("\n【期待値との比較】")
        print("  期待されるP値: 411.932")
        print(f"  差: {abs(result['P'] - 411.932):.3f}")
        
    except Exception as e:
        print(f"エラーが発生しました: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_new_implementation()