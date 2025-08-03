"""
Excelの実際の計算式を検証
"""

import numpy as np

def verify_excel_actual_formula():
    """Excelの実際の計算式を検証"""
    
    # テストケース2（新Excel）のパラメータ
    B = 6.508926968399547
    la = 8.424302920187878e-16  # ≈ 0
    excel_lw2 = 3.758015139473548
    
    print("=== Excelの実際の計算式の検証 ===")
    print(f"B = {B}")
    print(f"la = {la}")
    print(f"Excel lw2 = {excel_lw2}")
    
    # 各種近似式のテスト
    print("\n【各種近似式との比較】")
    
    # 1. la + B/√3
    lw2_sqrt3 = la + B / np.sqrt(3)
    print(f"la + B/√3 = {lw2_sqrt3:.10f}")
    print(f"差 = {abs(lw2_sqrt3 - excel_lw2):.10f}")
    print(f"相対誤差 = {abs(lw2_sqrt3 - excel_lw2) / excel_lw2 * 100:.4f}%")
    
    # 2. la + B * 0.577
    lw2_577 = la + B * 0.577
    print(f"\nla + B * 0.577 = {lw2_577:.10f}")
    print(f"差 = {abs(lw2_577 - excel_lw2):.10f}")
    
    # 3. la + B * 0.5773502692（1/√3の精密値）
    factor_precise = 1 / np.sqrt(3)
    lw2_precise = la + B * factor_precise
    print(f"\nla + B * {factor_precise:.10f} = {lw2_precise:.10f}")
    print(f"差 = {abs(lw2_precise - excel_lw2):.10f}")
    
    # テストケース1も確認
    print("\n\n=== テストケース1（元Excel）の確認 ===")
    B1 = 4.475692098691149
    la1 = -0.6989187243037986
    excel_lw2_1 = 1.876186174801123
    
    print(f"B = {B1}")
    print(f"la = {la1}")
    print(f"Excel lw2 = {excel_lw2_1}")
    
    lw2_sqrt3_1 = la1 + B1 / np.sqrt(3)
    print(f"\nla + B/√3 = {lw2_sqrt3_1:.10f}")
    print(f"差 = {abs(lw2_sqrt3_1 - excel_lw2_1):.10f}")
    print(f"相対誤差 = {abs(lw2_sqrt3_1 - excel_lw2_1) / excel_lw2_1 * 100:.4f}%")
    
    # 逆算
    factor_1 = (excel_lw2_1 - la1) / B1
    print(f"\n逆算係数 = (lw2 - la) / B = {factor_1:.10f}")
    print(f"1/√3 = {1/np.sqrt(3):.10f}")
    print(f"差 = {abs(factor_1 - 1/np.sqrt(3)):.10f}")

if __name__ == "__main__":
    verify_excel_actual_formula()