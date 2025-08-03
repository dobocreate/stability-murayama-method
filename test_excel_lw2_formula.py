"""
Excel M9（lw2）式の詳細解析
"""

import numpy as np

def test_excel_lw2_formula():
    """Excel M9式の分解検証"""
    
    # パラメータ（θ_d = 75°）
    phi_deg = 21
    phi_rad = np.radians(phi_deg)
    H_f = 5.2
    theta_d_deg = 75
    theta_d_rad = np.radians(theta_d_deg)
    
    # 計算済みの値
    r0 = 4.045471892076640
    rd = 6.686396245146751
    B = 4.475692098691150
    la = -0.698918724303799
    
    # 中間計算値
    O = 6.860890595417361
    P_rad = 0.860117311833133
    P_deg = 49.281091854176267
    S = 4.332310451453791
    R = 3.808242381949599
    T_rad = 0.841126789009281
    T_deg = 48.193015045622666
    U = 1.103080354051159
    V_rad = np.pi - 2*np.arctan(O/2/U)
    V_deg = np.degrees(V_rad)
    
    print("=== Excel M9式の詳細解析 ===")
    print("\nExcel M9式:")
    print("M9: =S9*COS(($D$5+T9)*PI()/180)+(2/3*(U9/(1-COS(V9*PI()/180)))*((1-(COS(V9*PI()/180))^2)/(V9*PI()/180-2*(SIN(V9*PI()/180))*(COS(V9*PI()/180))/2))*SIN(V9*PI()/180)-((U9*COS(V9*PI()/180))/(1-COS(V9*PI()/180))))*COS(ATAN(C9/$D$6))")
    
    print(f"\n基本値:")
    print(f"S = {S}")
    print(f"T = {T_deg}° = {T_rad} rad")
    print(f"U = {U}")
    print(f"V = {V_deg}° = {V_rad} rad")
    print(f"φ = {phi_deg}° = {phi_rad} rad")
    print(f"B = {B}, H_f = {H_f}")
    
    # Excel式の第1項
    term1 = S * np.cos((phi_deg + T_deg) * np.pi / 180)
    print(f"\n第1項: S*cos((φ+T)*π/180)")
    print(f"      = {S} * cos(({phi_deg} + {T_deg}) * π/180)")
    print(f"      = {S} * cos({(phi_deg + T_deg) * np.pi / 180})")
    print(f"      = {term1}")
    
    # Python版の第1項
    term1_python = S * np.cos(phi_rad + T_rad)
    print(f"\nPython版: S*cos(φ+T)")
    print(f"        = {S} * cos({phi_rad} + {T_rad})")
    print(f"        = {S} * cos({phi_rad + T_rad})")
    print(f"        = {term1_python}")
    print(f"差: {abs(term1 - term1_python):.2e}")
    
    # Excel式の第2項の分解
    print(f"\n第2項の分解:")
    
    # V関連の計算
    cos_V = np.cos(V_rad)
    sin_V = np.sin(V_rad)
    print(f"cos(V) = {cos_V}")
    print(f"sin(V) = {sin_V}")
    print(f"1 - cos(V) = {1 - cos_V}")
    
    # 第2項の各要素
    factor1 = U / (1 - cos_V)
    print(f"\nU/(1-cos(V)) = {U} / {1 - cos_V} = {factor1}")
    
    numerator = 1 - cos_V**2
    denominator = V_rad - 2 * sin_V * cos_V / 2
    factor2 = numerator / denominator
    print(f"\n(1-cos²(V))/(V-sin(V)*cos(V)) = {numerator} / {denominator} = {factor2}")
    
    factor3 = sin_V
    print(f"\nsin(V) = {factor3}")
    
    factor4 = U * cos_V / (1 - cos_V)
    print(f"\nU*cos(V)/(1-cos(V)) = {U} * {cos_V} / {1 - cos_V} = {factor4}")
    
    factor5 = np.cos(np.arctan(B / H_f))
    print(f"\ncos(arctan(B/H_f)) = cos(arctan({B}/{H_f})) = {factor5}")
    
    # 第2項全体
    term2_part1 = factor1 * factor2 * factor3
    term2_part2 = factor4
    term2 = (2/3) * (term2_part1 - term2_part2) * factor5
    
    print(f"\n第2項 = (2/3) * ({term2_part1} - {term2_part2}) * {factor5}")
    print(f"      = (2/3) * {term2_part1 - term2_part2} * {factor5}")
    print(f"      = {term2}")
    
    # 全体
    lw2_excel_formula = term1 + term2
    print(f"\nlw2 (Excel式) = {term1} + {term2} = {lw2_excel_formula}")
    
    # Python版の第2項
    term2_python = (2/3) * U * np.cos(np.arctan2(B, H_f))
    lw2_python = term1_python + term2_python
    print(f"\nlw2 (Python) = {term1_python} + {term2_python} = {lw2_python}")
    
    # 逆算値との比較
    lw2_excel_reverse = 1.876186174801123
    print(f"\nlw2 (Excel逆算) = {lw2_excel_reverse}")
    print(f"Excel式との差: {abs(lw2_excel_formula - lw2_excel_reverse)}")
    print(f"Python式との差: {abs(lw2_python - lw2_excel_reverse)}")
    
    # 簡略化された式の可能性
    print(f"\n--- 簡略化の可能性 ---")
    # Excelが実際に使っている可能性のある式
    lw2_simple = la + (2/3) * B
    print(f"lw2 = la + (2/3)*B = {la} + (2/3)*{B} = {lw2_simple}")
    print(f"Excel逆算値との差: {abs(lw2_simple - lw2_excel_reverse)}")
    
    # 別の可能性
    lw2_alt = S * np.cos(phi_rad + T_rad) + (2/3) * (B - la)
    print(f"\nlw2 = S*cos(φ+T) + (2/3)*(B-la)")
    print(f"    = {S * np.cos(phi_rad + T_rad)} + (2/3)*({B} - ({la}))")
    print(f"    = {lw2_alt}")
    print(f"Excel逆算値との差: {abs(lw2_alt - lw2_excel_reverse)}")

if __name__ == "__main__":
    test_excel_lw2_formula()