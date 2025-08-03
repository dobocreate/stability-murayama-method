"""
Excelの式の詳細検証
"""

import numpy as np

def verify_excel_formula():
    """Excel式の検証"""
    
    # テストケース2のExcel値
    excel = {
        'W': 905.41568258,  # Wf
        'lw': 2.61615258,
        'q': 167.06849771,
        'B': 6.508926968399547,
        'la': 8.427753792796626e-16,
        'c': 20,
        'rc': 13.757930737341093,  # rd
        'r0': 7.515861474682187,
        'phi_deg': 30,
        'lp': 8.757930737341093,
        'P': 322.93447293
    }
    
    phi_rad = np.radians(excel['phi_deg'])
    
    print("=== Excelの式の詳細検証 ===\n")
    
    print("Excel値:")
    for key, value in excel.items():
        print(f"  {key}: {value}")
    
    print("\nExcelの式:")
    print("P = (W・lw + q・B(la+B/2) - (c(rc^2-r0^2))/2tanφ) / lp")
    
    # 各項の計算
    print("\n各項の計算:")
    
    # W・lw
    W_lw = excel['W'] * excel['lw']
    print(f"  W・lw = {excel['W']} * {excel['lw']} = {W_lw}")
    
    # q・B(la+B/2)
    la_plus_B_half = excel['la'] + excel['B'] / 2
    q_B_term = excel['q'] * excel['B'] * la_plus_B_half
    print(f"  la + B/2 = {excel['la']} + {excel['B']}/2 = {la_plus_B_half}")
    print(f"  q・B(la+B/2) = {excel['q']} * {excel['B']} * {la_plus_B_half} = {q_B_term}")
    
    # Mc = c(rc^2-r0^2)/(2tanφ)
    rc_squared = excel['rc']**2
    r0_squared = excel['r0']**2
    diff_squared = rc_squared - r0_squared
    tan_phi = np.tan(phi_rad)
    Mc = excel['c'] * diff_squared / (2 * tan_phi)
    
    print(f"\n粘着抵抗モーメントMc:")
    print(f"  rc^2 = {rc_squared}")
    print(f"  r0^2 = {r0_squared}")
    print(f"  rc^2 - r0^2 = {diff_squared}")
    print(f"  tan(φ) = tan({excel['phi_deg']}°) = {tan_phi}")
    print(f"  2*tan(φ) = {2 * tan_phi}")
    print(f"  Mc = c(rc^2-r0^2)/(2tanφ) = {excel['c']} * {diff_squared} / {2 * tan_phi} = {Mc}")
    
    # 分子の計算
    numerator = W_lw + q_B_term - Mc
    print(f"\n分子の計算:")
    print(f"  分子 = W・lw + q・B(la+B/2) - Mc")
    print(f"       = {W_lw} + {q_B_term} - {Mc}")
    print(f"       = {numerator}")
    
    # P の計算
    P_calc = numerator / excel['lp']
    print(f"\nPの計算:")
    print(f"  P = 分子 / lp = {numerator} / {excel['lp']} = {P_calc}")
    
    print(f"\n比較:")
    print(f"  計算されたP: {P_calc}")
    print(f"  ExcelのP: {excel['P']}")
    print(f"  差: {P_calc - excel['P']}")
    
    # もしかして、Wfではなく別の値？
    print(f"\n\nもしかして、WはWfではない？")
    
    # P値から逆算してWを求める
    # P * lp = W・lw + q・B(la+B/2) - Mc
    # W・lw = P * lp + Mc - q・B(la+B/2)
    W_lw_from_P = excel['P'] * excel['lp'] + Mc - q_B_term
    W_from_P = W_lw_from_P / excel['lw']
    
    print(f"  P値から逆算したW・lw = {W_lw_from_P}")
    print(f"  P値から逆算したW = {W_from_P}")
    print(f"  元のW(Wf) = {excel['W']}")
    print(f"  差 = {W_from_P - excel['W']}")

if __name__ == "__main__":
    verify_excel_formula()