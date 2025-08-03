"""
Excel M9式（lw2）の完全解析
"""

import numpy as np

def analyze_excel_m9():
    """Excel M9式の完全な解析"""
    
    # パラメータ（θ_d = 75°）
    phi_deg = 21  # $D$5
    phi_rad = np.radians(phi_deg)
    H_f = 5.2     # $D$6
    B = 4.475692098691150  # C9
    
    # 計算済みの値（Excel row 9）
    S = 4.332310451453791  # S9
    T_deg = 48.19301504562269  # T9
    U = 1.103080354051158  # U9
    V_deg = 35.651014799651634  # V9
    
    print("=== Excel M9式の完全解析 ===")
    print("\nExcel M9式:")
    print("M9: =S9*COS(($D$5+T9)*PI()/180)+(2/3*(U9/(1-COS(V9*PI()/180)))*((1-(COS(V9*PI()/180))^2)/(V9*PI()/180-2*(SIN(V9*PI()/180))*(COS(V9*PI()/180))/2))*SIN(V9*PI()/180)-((U9*COS(V9*PI()/180))/(1-COS(V9*PI()/180))))*COS(ATAN(C9/$D$6))")
    
    print(f"\n使用する値:")
    print(f"S (S9) = {S}")
    print(f"φ ($D$5) = {phi_deg}°")
    print(f"T (T9) = {T_deg}°")
    print(f"U (U9) = {U}")
    print(f"V (V9) = {V_deg}°")
    print(f"B (C9) = {B}")
    print(f"H_f ($D$6) = {H_f}")
    
    # ラジアンに変換
    T_rad = np.radians(T_deg)
    V_rad = np.radians(V_deg)
    
    # 第1項: S*cos((φ+T)*π/180)
    term1 = S * np.cos(np.radians(phi_deg + T_deg))
    print(f"\n第1項: S*cos((φ+T)*π/180)")
    print(f"      = {S} * cos(({phi_deg} + {T_deg})*π/180)")
    print(f"      = {S} * cos({np.radians(phi_deg + T_deg)})")
    print(f"      = {term1}")
    
    # 第2項の準備
    cos_V_rad = np.cos(V_rad)
    sin_V_rad = np.sin(V_rad)
    atan_B_Hf = np.arctan(B / H_f)
    cos_atan = np.cos(atan_B_Hf)
    
    print(f"\n第2項の準備:")
    print(f"cos(V*π/180) = cos({V_rad}) = {cos_V_rad}")
    print(f"sin(V*π/180) = sin({V_rad}) = {sin_V_rad}")
    print(f"atan(B/H_f) = atan({B}/{H_f}) = {atan_B_Hf}")
    print(f"cos(atan(B/H_f)) = {cos_atan}")
    
    # 第2項の各部分を分解
    # (2/3*(U9/(1-COS(V9*PI()/180)))*((1-(COS(V9*PI()/180))^2)/(V9*PI()/180-2*(SIN(V9*PI()/180))*(COS(V9*PI()/180))/2))*SIN(V9*PI()/180)-((U9*COS(V9*PI()/180))/(1-COS(V9*PI()/180))))*COS(ATAN(C9/$D$6))
    
    # A = U/(1-cos(V))
    A = U / (1 - cos_V_rad)
    print(f"\nA = U/(1-cos(V)) = {U}/(1-{cos_V_rad}) = {A}")
    
    # B_num = 1 - cos²(V)
    B_num = 1 - cos_V_rad**2
    print(f"\nB_num = 1 - cos²(V) = 1 - {cos_V_rad}² = {B_num}")
    
    # B_den = V*π/180 - 2*sin(V)*cos(V)/2 = V*π/180 - sin(V)*cos(V)
    B_den = V_rad - sin_V_rad * cos_V_rad
    print(f"B_den = V*π/180 - sin(V)*cos(V) = {V_rad} - {sin_V_rad}*{cos_V_rad} = {B_den}")
    
    # B = B_num / B_den
    B_frac = B_num / B_den
    print(f"B = B_num/B_den = {B_num}/{B_den} = {B_frac}")
    
    # C = sin(V)
    C = sin_V_rad
    print(f"\nC = sin(V) = {C}")
    
    # D = U*cos(V)/(1-cos(V))
    D = U * cos_V_rad / (1 - cos_V_rad)
    print(f"\nD = U*cos(V)/(1-cos(V)) = {U}*{cos_V_rad}/(1-{cos_V_rad}) = {D}")
    
    # 第2項 = (2/3) * (A * B * C - D) * cos(atan(B/H_f))
    term2_inner = A * B_frac * C - D
    term2 = (2/3) * term2_inner * cos_atan
    
    print(f"\n第2項の計算:")
    print(f"A * B * C = {A} * {B_frac} * {C} = {A * B_frac * C}")
    print(f"A * B * C - D = {A * B_frac * C} - {D} = {term2_inner}")
    print(f"第2項 = (2/3) * {term2_inner} * {cos_atan} = {term2}")
    
    # 最終結果
    lw2_excel = term1 + term2
    print(f"\n最終結果:")
    print(f"lw2 (M9) = 第1項 + 第2項 = {term1} + {term2} = {lw2_excel}")
    
    # Excel逆算値との比較
    lw2_reverse = 1.876186174801123
    print(f"\nExcel逆算値: {lw2_reverse}")
    print(f"計算値との差: {abs(lw2_excel - lw2_reverse)}")
    
    # デバッグ: Excelの実際の値を使って検証
    print("\n=== Excelの実際の値で検証 ===")
    # V_deg が度単位なので、Excel式でも度単位で計算する必要がある
    V_deg_rad = V_deg * np.pi / 180  # これがExcelでのV9*PI()/180
    
    # Excel式を正確に再現
    excel_cos_V = np.cos(V_deg_rad)
    excel_sin_V = np.sin(V_deg_rad)
    
    # Excel式の分母の計算に注意
    # V9*PI()/180-2*(SIN(V9*PI()/180))*(COS(V9*PI()/180))/2
    # = V_deg_rad - 2 * sin_V * cos_V / 2
    # = V_deg_rad - sin_V * cos_V
    excel_B_den = V_deg_rad - excel_sin_V * excel_cos_V
    
    print(f"Excel方式での計算:")
    print(f"V_deg_rad = {V_deg} * π/180 = {V_deg_rad}")
    print(f"cos(V_deg_rad) = {excel_cos_V}")
    print(f"sin(V_deg_rad) = {excel_sin_V}")
    print(f"分母 = {V_deg_rad} - {excel_sin_V} * {excel_cos_V} = {excel_B_den}")

if __name__ == "__main__":
    analyze_excel_m9()