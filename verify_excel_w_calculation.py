"""
ExcelのW計算の検証
"""

import numpy as np

def verify_excel_w_calculation():
    """ExcelのW計算を検証"""
    
    print("=== ExcelのW計算の検証 ===\n")
    
    # テストケース2
    print("【テストケース2】")
    
    # Excel値
    w1 = 650.8926968399547
    w2 = 254.52298574301267
    Wf = 905.4156825829673
    
    print(f"Excel値:")
    print(f"  w1 = {w1}")
    print(f"  w2 = {w2}")
    print(f"  Wf = {Wf}")
    print(f"  w1 + w2 = {w1 + w2}")
    print(f"  確認: Wf = w1 + w2 ? {abs(Wf - (w1 + w2)) < 0.001}")
    
    # もしかして、Excelでは総自重Wfではなく、有効自重を使用？
    # 有効自重 = 自重 - 浮力？
    
    # または、安全率を考慮？
    safety_factors = [0.9, 0.8, 0.7, 0.67]
    print(f"\n安全率を考慮した場合:")
    for sf in safety_factors:
        W_sf = Wf * sf
        print(f"  W = {sf} * Wf = {sf} * {Wf} = {W_sf:.2f}")
    
    # P値から逆算したW
    W_from_P = 607.4753387685497
    ratio = W_from_P / Wf
    print(f"\nP値から逆算したW:")
    print(f"  W = {W_from_P}")
    print(f"  W / Wf = {ratio:.4f}")
    
    # テストケース1も確認
    print("\n\n【テストケース1】")
    
    w1_1 = 296.7383861432232
    w2_1 = 137.55784282036365
    Wf_1 = 434.29622896358677
    
    print(f"Excel値:")
    print(f"  w1 = {w1_1}")
    print(f"  w2 = {w2_1}")
    print(f"  Wf = {Wf_1}")
    print(f"  w1 + w2 = {w1_1 + w2_1}")
    print(f"  確認: Wf = w1 + w2 ? {abs(Wf_1 - (w1_1 + w2_1)) < 0.001}")
    
    # 両ケースでWf = w1 + w2が成立していることを確認
    print("\n結論:")
    print("  両ケースでWf = w1 + w2が正確に成立")
    print("  ExcelのWfは正しく総自重を表している")
    
    # では、なぜP計算が異なるのか？
    print("\n\nP計算の差異の原因:")
    print("1. Mcの計算方法が異なる可能性")
    print("2. P計算式の解釈が異なる可能性")
    print("3. 他の要因（単位、係数など）の可能性")
    
    # 単位の確認
    print("\n単位の確認:")
    print("  c: kPa")
    print("  γ: kN/m³")
    print("  W: kN (1m幅当たり)")
    print("  q: kN/m²")
    print("  Mc: kN·m (モーメント)")
    print("  P: kN/m²")

if __name__ == "__main__":
    verify_excel_w_calculation()