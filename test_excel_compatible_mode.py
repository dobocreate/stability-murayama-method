"""
Excel互換モードのテスト
"""

import numpy as np
from murayama_calculator_revised import MurayamaCalculatorRevised

def test_excel_compatible_mode():
    """Excel互換モードで簡略式を使用するテスト"""
    
    # テストケース
    test_cases = [
        {
            'name': 'テストケース1（元Excel）',
            'params': {
                'H': 10,
                'gamma': 19,
                'c': 10,
                'phi_deg': 30,
                'H_f': 10,
                'theta_d_deg': 60
            },
            'excel_values': {
                'q': 18.0,
                'w1': 425.73,
                'lw1': 2.984,
                'w2': 164.96,
                'lw2': 1.876
            }
        },
        {
            'name': 'テストケース2（新Excel）',
            'params': {
                'H': 50,
                'gamma': 20,
                'c': 20,
                'phi_deg': 30,
                'H_f': 10,
                'theta_d_deg': 60
            },
            'excel_values': {
                'q': 90.0,
                'w1': 650.89,
                'lw1': 2.170,
                'w2': 150.22,
                'lw2': 3.758
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n=== {test_case['name']} ===")
        params = test_case['params']
        excel_vals = test_case['excel_values']
        
        # 通常モードでの計算
        calculator_normal = MurayamaCalculatorRevised(
            H_f=params['H_f'],
            gamma=params['gamma'],
            phi=params['phi_deg'],
            coh=params['c'],
            H=params['H'],
            alpha=1.8,
            K=1.0,
            force_finite_cover=True,
            excel_compatible_lw2=False  # 通常モード
        )
        
        # Excel互換モードでの計算
        calculator_excel = MurayamaCalculatorRevised(
            H_f=params['H_f'],
            gamma=params['gamma'],
            phi=params['phi_deg'],
            coh=params['c'],
            H=params['H'],
            alpha=1.8,
            K=1.0,
            force_finite_cover=True,
            excel_compatible_lw2=True  # Excel互換モード
        )
        
        theta_d_rad = np.radians(params['theta_d_deg'])
        
        result_normal = calculator_normal.calculate_support_pressure(theta_d_rad)
        result_excel = calculator_excel.calculate_support_pressure(theta_d_rad)
        
        print(f"\n【通常モード】")
        print(f"q = {result_normal['q']:.3f} (Excel: {excel_vals['q']:.3f})")
        print(f"w1 = {result_normal['w1']:.2f} (Excel: {excel_vals['w1']:.2f})")
        print(f"lw1 = {result_normal['lw1']:.3f} (Excel: {excel_vals['lw1']:.3f})")
        print(f"w2 = {result_normal['w2']:.2f} (Excel: {excel_vals['w2']:.2f})")
        print(f"lw2 = {result_normal['lw2']:.3f} (Excel: {excel_vals['lw2']:.3f})")
        print(f"P = {result_normal['P']:.0f}")
        
        print(f"\n【Excel互換モード（簡略式）】")
        print(f"q = {result_excel['q']:.3f} (Excel: {excel_vals['q']:.3f})")
        print(f"w1 = {result_excel['w1']:.2f} (Excel: {excel_vals['w1']:.2f})")
        print(f"lw1 = {result_excel['lw1']:.3f} (Excel: {excel_vals['lw1']:.3f})")
        print(f"w2 = {result_excel['w2']:.2f} (Excel: {excel_vals['w2']:.2f})")
        print(f"lw2 = {result_excel['lw2']:.3f} (Excel: {excel_vals['lw2']:.3f})")
        print(f"P = {result_excel['P']:.0f}")
        
        # lw2の相対誤差
        error_normal = abs(result_normal['lw2'] - excel_vals['lw2']) / excel_vals['lw2'] * 100
        error_excel = abs(result_excel['lw2'] - excel_vals['lw2']) / excel_vals['lw2'] * 100
        
        print(f"\n【lw2の相対誤差】")
        print(f"通常モード: {error_normal:.1f}%")
        print(f"Excel互換モード: {error_excel:.1f}%")
        
        # 簡略式の検証
        B = result_excel['geometry']['B']
        la = result_excel['geometry']['la']
        lw2_formula = la + B / np.sqrt(3)
        print(f"\n【簡略式の検証】")
        print(f"la + B/√3 = {la:.3f} + {B:.3f}/√3 = {lw2_formula:.3f}")
        print(f"計算値と一致: {abs(lw2_formula - result_excel['lw2']) < 1e-10}")

if __name__ == "__main__":
    test_excel_compatible_mode()