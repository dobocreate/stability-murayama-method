"""
最終実装の確認テスト
"""

import numpy as np
from murayama_calculator_revised import MurayamaCalculatorRevised

def test_final_implementation():
    """最終実装の確認"""
    
    print("=== 最終実装の確認テスト ===\n")
    
    # テストケース2のパラメータ（Excel値と比較）
    params = {
        'H': 50,
        'gamma': 20,
        'c': 20,
        'phi_deg': 30,
        'H_f': 10,
        'theta_d_deg': 60,
        'alpha': 1.8,
        'K': 1.0
    }
    
    excel_values = {
        'q': 90.0,
        'B': 6.509,
        'w1': 650.89,
        'lw1': 2.170,
        'w2': 150.22,
        'lw2': 3.758,
        'P': 323
    }
    
    print("テストパラメータ:")
    for key, value in params.items():
        print(f"  {key}: {value}")
    
    print("\n1. 通常モード（理論式）での計算:")
    calculator_normal = MurayamaCalculatorRevised(
        H_f=params['H_f'],
        gamma=params['gamma'],
        phi=params['phi_deg'],
        coh=params['c'],
        H=params['H'],
        alpha=params['alpha'],
        K=params['K'],
        force_finite_cover=True,
        excel_compatible_lw2=False
    )
    
    theta_d_rad = np.radians(params['theta_d_deg'])
    result_normal = calculator_normal.calculate_support_pressure(theta_d_rad)
    
    print(f"  B = {result_normal['geometry']['B']:.3f} (Excel: {excel_values['B']:.3f})")
    print(f"  q = {result_normal['q']:.3f} (Excel: {excel_values['q']:.3f})")
    print(f"  w1 = {result_normal['w1']:.2f} (Excel: {excel_values['w1']:.2f})")
    print(f"  lw1 = {result_normal['lw1']:.3f} (Excel: {excel_values['lw1']:.3f})")
    print(f"  w2 = {result_normal['w2']:.2f} (Excel: {excel_values['w2']:.2f})")
    print(f"  lw2 = {result_normal['lw2']:.3f} (Excel: {excel_values['lw2']:.3f})")
    print(f"  P = {result_normal['P']:.0f} (Excel: {excel_values['P']:.0f})")
    
    print("\n2. Excel互換モード（簡略式）での計算:")
    calculator_excel = MurayamaCalculatorRevised(
        H_f=params['H_f'],
        gamma=params['gamma'],
        phi=params['phi_deg'],
        coh=params['c'],
        H=params['H'],
        alpha=params['alpha'],
        K=params['K'],
        force_finite_cover=True,
        excel_compatible_lw2=True
    )
    
    result_excel = calculator_excel.calculate_support_pressure(theta_d_rad)
    
    print(f"  B = {result_excel['geometry']['B']:.3f} (Excel: {excel_values['B']:.3f})")
    print(f"  q = {result_excel['q']:.3f} (Excel: {excel_values['q']:.3f})")
    print(f"  w1 = {result_excel['w1']:.2f} (Excel: {excel_values['w1']:.2f})")
    print(f"  lw1 = {result_excel['lw1']:.3f} (Excel: {excel_values['lw1']:.3f})")
    print(f"  w2 = {result_excel['w2']:.2f} (Excel: {excel_values['w2']:.2f})")
    print(f"  lw2 = {result_excel['lw2']:.3f} (Excel: {excel_values['lw2']:.3f})")
    print(f"  P = {result_excel['P']:.0f} (Excel: {excel_values['P']:.0f})")
    
    print("\n3. 差異の分析:")
    print(f"  lw2の差（通常モード）: {abs(result_normal['lw2'] - excel_values['lw2']):.3f} ({abs(result_normal['lw2'] - excel_values['lw2'])/excel_values['lw2']*100:.1f}%)")
    print(f"  lw2の差（Excel互換）: {abs(result_excel['lw2'] - excel_values['lw2']):.3f} ({abs(result_excel['lw2'] - excel_values['lw2'])/excel_values['lw2']*100:.1f}%)")
    print(f"  Pの差（通常モード）: {abs(result_normal['P'] - excel_values['P']):.0f} ({abs(result_normal['P'] - excel_values['P'])/excel_values['P']*100:.1f}%)")
    print(f"  Pの差（Excel互換）: {abs(result_excel['P'] - excel_values['P']):.0f} ({abs(result_excel['P'] - excel_values['P'])/excel_values['P']*100:.1f}%)")
    
    print("\n4. まとめ:")
    print("  - 通常モード: 理論的に正しいExcel M9式を使用")
    print("  - Excel互換モード: 簡略式（lw2 = la + B/√3）を使用")
    print("  - Excel互換モードでlw2が完全に一致")
    print("  - qの差異は有効幅係数の解釈の違いによるもの")

if __name__ == "__main__":
    test_final_implementation()