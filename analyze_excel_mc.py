"""
ExcelのMc計算方法の精査
"""

import numpy as np

def analyze_excel_mc():
    """ExcelのMc計算を精査"""
    
    print("=== ExcelのMc計算方法の精査 ===\n")
    
    # テストケース2のパラメータとExcel値
    params = {
        'c': 20,  # kPa
        'phi_deg': 30,
        'r0': 7.515861474682187,
        'rd': 13.757930737341093,  # Excel記載ではrc
    }
    
    excel_values = {
        'W': 905.4156825829673,  # Wf
        'lw': 2.6161525827276515,
        'q': 167.06849770684155,
        'B': 6.508926968399547,
        'la': 8.427753792796626e-16,
        'lp': 8.757930737341093,
        'P': 322.93447293062375
    }
    
    phi_rad = np.radians(params['phi_deg'])
    
    print("パラメータ:")
    print(f"  c = {params['c']} kPa")
    print(f"  φ = {params['phi_deg']}°")
    print(f"  r0 = {params['r0']} m")
    print(f"  rd (rc) = {params['rd']} m")
    
    # 理論的なMc計算
    print("\n1. 理論的なMc計算:")
    print("  Mc = c(rd² - r0²)/(2tanφ)")
    
    rd_squared = params['rd']**2
    r0_squared = params['r0']**2
    diff_squared = rd_squared - r0_squared
    tan_phi = np.tan(phi_rad)
    
    Mc_theory = params['c'] * diff_squared / (2 * tan_phi)
    
    print(f"  rd² = {rd_squared}")
    print(f"  r0² = {r0_squared}")
    print(f"  rd² - r0² = {diff_squared}")
    print(f"  tan(φ) = {tan_phi}")
    print(f"  Mc = {params['c']} * {diff_squared} / (2 * {tan_phi})")
    print(f"     = {Mc_theory}")
    
    # ExcelのP式から逆算
    print("\n2. ExcelのP値から逆算:")
    print("  P = (W・lw + q・B(la+B/2) - Mc) / lp")
    
    # 分子の各項を計算
    W_lw = excel_values['W'] * excel_values['lw']
    la_plus_B_half = excel_values['la'] + excel_values['B'] / 2
    q_B_term = excel_values['q'] * excel_values['B'] * la_plus_B_half
    
    print(f"\n  W・lw = {excel_values['W']} * {excel_values['lw']} = {W_lw}")
    print(f"  q・B(la+B/2) = {excel_values['q']} * {excel_values['B']} * {la_plus_B_half}")
    print(f"              = {q_B_term}")
    
    # P * lp = W・lw + q・B(la+B/2) - Mc
    # Mc = W・lw + q・B(la+B/2) - P * lp
    numerator_without_mc = W_lw + q_B_term
    Mc_from_P = numerator_without_mc - excel_values['P'] * excel_values['lp']
    
    print(f"\n  Mc = W・lw + q・B(la+B/2) - P * lp")
    print(f"     = {numerator_without_mc} - {excel_values['P']} * {excel_values['lp']}")
    print(f"     = {numerator_without_mc} - {excel_values['P'] * excel_values['lp']}")
    print(f"     = {Mc_from_P}")
    
    # 比較
    print("\n3. 比較:")
    print(f"  理論的Mc = {Mc_theory}")
    print(f"  Excel逆算Mc = {Mc_from_P}")
    print(f"  差 = {Mc_theory - Mc_from_P}")
    print(f"  比率 = {Mc_from_P / Mc_theory}")
    
    # もしMcが理論値なら、Wはどうなるか？
    print("\n4. Mcが理論値の場合、Wはどうなるか:")
    # P = (W・lw + q・B(la+B/2) - Mc) / lp
    # W・lw = P * lp + Mc - q・B(la+B/2)
    W_lw_with_theory_Mc = excel_values['P'] * excel_values['lp'] + Mc_theory - q_B_term
    W_with_theory_Mc = W_lw_with_theory_Mc / excel_values['lw']
    
    print(f"  必要なW・lw = {W_lw_with_theory_Mc}")
    print(f"  必要なW = {W_with_theory_Mc}")
    print(f"  実際のW = {excel_values['W']}")
    print(f"  差 = {W_with_theory_Mc - excel_values['W']}")
    
    # テストケース1も確認
    print("\n\n=== テストケース1の確認 ===")
    
    params1 = {
        'c': 253,  # kPa
        'phi_deg': 21,
        'r0': 4.045471892076639,
        'rd': 6.686396245146749,
    }
    
    excel1 = {
        'W': 434.29622896358677,
        'lw': 1.136070940712082,
        'q': -239.0930847591986,
        'B': 4.475692098691149,
        'la': -0.6989187243037986,
        'lp': 4.049767466906651,
        'P': -2434.7018976765366
    }
    
    phi_rad1 = np.radians(params1['phi_deg'])
    
    # Mc計算
    Mc_theory1 = params1['c'] * (params1['rd']**2 - params1['r0']**2) / (2 * np.tan(phi_rad1))
    
    # P値から逆算
    W_lw1 = excel1['W'] * excel1['lw']
    q_B_term1 = excel1['q'] * excel1['B'] * (excel1['la'] + excel1['B'] / 2)
    Mc_from_P1 = W_lw1 + q_B_term1 - excel1['P'] * excel1['lp']
    
    print(f"理論的Mc = {Mc_theory1}")
    print(f"Excel逆算Mc = {Mc_from_P1}")
    print(f"比率 = {Mc_from_P1 / Mc_theory1}")

if __name__ == "__main__":
    analyze_excel_mc()