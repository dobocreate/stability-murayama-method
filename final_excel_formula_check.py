"""
ExcelのP計算式の最終確認
"""

import numpy as np

def final_excel_formula_check():
    """ExcelのP計算式を最終確認"""
    
    print("=== ExcelのP計算式の最終確認 ===\n")
    
    print("Excelの式:")
    print("P = (W・lw + q・B(la+B/2) - (c(rc^2-r0^2))/2tanφ) / lp")
    print("\nこの式の解釈:")
    print("P = (W・lw + q・B・(la+B/2) - c・(rc²-r0²)/(2・tanφ)) / lp")
    
    # テストケース2で確認
    print("\n【テストケース2での計算】")
    
    # パラメータ
    c = 20
    phi_deg = 30
    phi_rad = np.radians(phi_deg)
    
    # Excel値
    excel = {
        'W': 905.4156825829673,
        'lw': 2.6161525827276515,
        'q': 167.06849770684155,
        'B': 6.508926968399547,
        'la': 8.427753792796626e-16,
        'rc': 13.757930737341093,
        'r0': 7.515861474682187,
        'lp': 8.757930737341093,
        'P': 322.93447293062375
    }
    
    # 各項の計算
    print("\n1. W・lw:")
    W_lw = excel['W'] * excel['lw']
    print(f"   = {excel['W']} × {excel['lw']}")
    print(f"   = {W_lw}")
    
    print("\n2. q・B・(la+B/2):")
    la_B_half = excel['la'] + excel['B'] / 2
    q_B_term = excel['q'] * excel['B'] * la_B_half
    print(f"   la + B/2 = {excel['la']} + {excel['B']}/2 = {la_B_half}")
    print(f"   q・B・(la+B/2) = {excel['q']} × {excel['B']} × {la_B_half}")
    print(f"   = {q_B_term}")
    
    print("\n3. Mc = c・(rc²-r0²)/(2・tanφ):")
    rc_sq = excel['rc']**2
    r0_sq = excel['r0']**2
    diff_sq = rc_sq - r0_sq
    tan_phi = np.tan(phi_rad)
    Mc = c * diff_sq / (2 * tan_phi)
    print(f"   rc² = {rc_sq}")
    print(f"   r0² = {r0_sq}")
    print(f"   rc² - r0² = {diff_sq}")
    print(f"   2・tanφ = 2 × tan({phi_deg}°) = {2 * tan_phi}")
    print(f"   Mc = {c} × {diff_sq} / {2 * tan_phi}")
    print(f"      = {Mc}")
    
    print("\n4. 分子の計算:")
    numerator = W_lw + q_B_term - Mc
    print(f"   = W・lw + q・B・(la+B/2) - Mc")
    print(f"   = {W_lw} + {q_B_term} - {Mc}")
    print(f"   = {numerator}")
    
    print("\n5. P = 分子 / lp:")
    P_calc = numerator / excel['lp']
    print(f"   = {numerator} / {excel['lp']}")
    print(f"   = {P_calc}")
    
    print(f"\n比較:")
    print(f"  計算されたP = {P_calc}")
    print(f"  ExcelのP = {excel['P']}")
    print(f"  差 = {P_calc - excel['P']}")
    print(f"  相対誤差 = {abs(P_calc - excel['P']) / excel['P'] * 100:.1f}%")
    
    # もしかして、ExcelではMcに異なる係数を使用？
    print("\n\n【Mcに係数を適用した場合】")
    
    factors = [0.5, 0.67, 0.75, 1.5, 2.0]
    for factor in factors:
        Mc_factor = Mc * factor
        numerator_factor = W_lw + q_B_term - Mc_factor
        P_factor = numerator_factor / excel['lp']
        error = abs(P_factor - excel['P'])
        print(f"\nMc × {factor}:")
        print(f"  Mc = {Mc_factor}")
        print(f"  P = {P_factor}")
        print(f"  誤差 = {error}")
        if error < 1:
            print(f"  ★ ほぼ一致！")

if __name__ == "__main__":
    final_excel_formula_check()