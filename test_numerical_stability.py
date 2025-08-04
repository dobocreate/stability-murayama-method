"""
数値的安定性のテスト（分岐なし実装）
"""

import numpy as np
from murayama_calculator_revised import MurayamaCalculatorRevised

def test_numerical_stability():
    """様々なパラメータで数値的安定性をテスト"""
    
    print("=== 数値的安定性テスト（分岐なし実装） ===\n")
    
    # テストケース
    test_cases = [
        # 通常の範囲
        {
            'name': '通常ケース1',
            'H': 30, 'gamma': 20, 'c': 30, 'phi_deg': 35,
            'H_f': 8, 'theta_d_deg': 60
        },
        {
            'name': '通常ケース2', 
            'H': 40, 'gamma': 22, 'c': 40, 'phi_deg': 40,
            'H_f': 12, 'theta_d_deg': 55
        },
        # 極端なケース
        {
            'name': '小さいφ',
            'H': 20, 'gamma': 18, 'c': 100, 'phi_deg': 10,
            'H_f': 5, 'theta_d_deg': 70
        },
        {
            'name': '大きいφ',
            'H': 50, 'gamma': 24, 'c': 10, 'phi_deg': 50,
            'H_f': 15, 'theta_d_deg': 45
        },
        # 元のテストケース1（問題のあるケース）
        {
            'name': 'Excel元データ',
            'H': 9.9, 'gamma': 25.5, 'c': 253, 'phi_deg': 21,
            'H_f': 5.2, 'theta_d_deg': 75
        }
    ]
    
    for case in test_cases:
        print(f"【{case['name']}】")
        print(f"パラメータ: H={case['H']}, γ={case['gamma']}, c={case['c']}, φ={case['phi_deg']}°, H_f={case['H_f']}, θ_d={case['theta_d_deg']}°")
        
        try:
            calculator = MurayamaCalculatorRevised(
                H_f=case['H_f'],
                gamma=case['gamma'],
                phi=case['phi_deg'],
                coh=case['c'],
                H=case['H'],
                alpha=1.8,
                K=1.0,
                force_finite_cover=True
            )
            
            theta_d_rad = np.radians(case['theta_d_deg'])
            result = calculator.calculate_support_pressure(theta_d_rad)
            
            # 中間変数の確認
            geom = calculator.calculate_geometry(theta_d_rad)
            
            # 曲線部分の計算過程を再現
            O = np.hypot(geom['B'], case['H_f'])
            P_angle = np.arctan2(case['H_f'], geom['B'])
            
            S = np.sqrt((O**2)/4.0 + geom['r0']**2 - O*geom['r0']*np.cos(P_angle + np.radians(case['phi_deg'])))
            
            R = geom['r0'] * np.sin(P_angle + np.radians(case['phi_deg']))
            cos_arg = np.clip(R / S, -1.0, 1.0) if S > 0.0 else 1.0
            T = np.arccos(cos_arg) - (P_angle + np.radians(case['phi_deg']) - np.pi/2.0)
            
            U = (geom['r0']*np.exp(T*np.tan(np.radians(case['phi_deg']))) - S) * (geom['r0']*np.sin(P_angle + np.radians(case['phi_deg']))) / (S if S != 0.0 else 1.0)
            
            if abs(U) > 1e-12:
                V = np.pi - 2*np.arctan(O/(2*U))
            else:
                V = np.pi
            
            print(f"\n  中間変数:")
            print(f"    O = {O:.6f}, P = {np.degrees(P_angle):.2f}°")
            print(f"    S = {S:.6f}, T = {np.degrees(T):.2f}°")
            print(f"    U = {U:.6f}, V = {np.degrees(V):.2f}°")
            print(f"    1 - cos(V) = {1 - np.cos(V):.6e}")
            print(f"    V - sin(V)*cos(V) = {V - np.sin(V)*np.cos(V):.6e}")
            
            print(f"\n  計算結果:")
            print(f"    B = {result['geometry']['B']:.6f}")
            print(f"    q = {result['q']:.4f}")
            print(f"    lw2 = {result['lw2']:.6f}")
            print(f"    P = {result['P']:.2f}")
            
        except Exception as e:
            print(f"  エラー: {type(e).__name__}: {e}")
        
        print("-" * 80)

if __name__ == "__main__":
    test_numerical_stability()