"""
P計算の詳細検証
"""

import numpy as np
from murayama_calculator_revised import MurayamaCalculatorRevised

def test_p_calculation_detail():
    """P計算の詳細検証"""
    
    # テストケース2のパラメータ
    params = {
        'H': 50,
        'gamma': 20,
        'c': 20,
        'phi_deg': 30,
        'H_f': 10,
        'alpha': 1.8,
        'K': 1.0,
        'theta_d_deg': 60
    }
    
    # Excel値
    excel_values = {
        'B': 6.508926968399547,
        'r0': 7.515861474682187,
        'rd': 13.757930737341093,
        'la': 8.427753792796626e-16,
        'lp': 8.757930737341093,
        'q': 167.06849771,
        'Wf': 905.41568258,
        'w1': 650.89269684,
        'lw1': 2.16964232,
        'w2': 254.52298574,
        'lw2': 3.75801514,
        'lw': 2.61615258,
        'P': 322.93447293
    }
    
    print("=== P計算の詳細検証 ===\n")
    
    # 計算機インスタンス
    calculator = MurayamaCalculatorRevised(
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
    
    theta_d_rad = np.radians(params['theta_d_deg'])
    phi_rad = np.radians(params['phi_deg'])
    result = calculator.calculate_support_pressure(theta_d_rad)
    
    print("【Python計算結果】")
    for key in ['B', 'q', 'Wf', 'lw', 'P']:
        if key == 'B':
            value = result['geometry']['B']
        else:
            value = result[key]
        print(f"{key}: {value}")
    
    print("\n【Excel値】")
    for key in ['B', 'q', 'Wf', 'lw', 'P']:
        print(f"{key}: {excel_values[key]}")
    
    # P計算の詳細
    print("\n【P計算の詳細】")
    
    # Pythonの計算
    B = result['geometry']['B']
    la = result['geometry']['la']
    lp = result['geometry']['lp']
    r0 = result['geometry']['r0']
    rd = result['geometry']['rd']
    
    q = result['q']
    Wf = result['Wf']
    lw = result['lw']
    
    # 粘着抵抗モーメント
    Mc = params['c'] * (rd**2 - r0**2) / (2 * np.tan(phi_rad))
    
    # P計算
    numerator = Wf * lw + q * B * (la + B/2) - Mc
    P_calc = numerator / lp
    
    print(f"\nPython計算詳細:")
    print(f"  Wf * lw = {Wf} * {lw} = {Wf * lw}")
    print(f"  q * B * (la + B/2) = {q} * {B} * ({la} + {B/2}) = {q * B * (la + B/2)}")
    print(f"  Mc = c * (rd² - r0²) / (2*tan(φ)) = {params['c']} * ({rd}² - {r0}²) / (2*tan({params['phi_deg']}°)")
    print(f"     = {Mc}")
    print(f"  分子 = {Wf * lw} + {q * B * (la + B/2)} - {Mc} = {numerator}")
    print(f"  P = 分子 / lp = {numerator} / {lp} = {P_calc}")
    print(f"  結果のP = {result['P']}")
    
    # Excelの値で計算
    print(f"\nExcel値での計算:")
    Wf_excel = excel_values['Wf']
    lw_excel = excel_values['lw']
    q_excel = excel_values['q']
    B_excel = excel_values['B']
    la_excel = excel_values['la']
    lp_excel = excel_values['lp']
    
    numerator_excel = Wf_excel * lw_excel + q_excel * B_excel * (la_excel + B_excel/2) - Mc
    P_excel_calc = numerator_excel / lp_excel
    
    print(f"  Wf * lw = {Wf_excel} * {lw_excel} = {Wf_excel * lw_excel}")
    print(f"  q * B * (la + B/2) = {q_excel} * {B_excel} * ({la_excel} + {B_excel/2}) = {q_excel * B_excel * (la_excel + B_excel/2)}")
    print(f"  Mc = {Mc}")
    print(f"  分子 = {Wf_excel * lw_excel} + {q_excel * B_excel * (la_excel + B_excel/2)} - {Mc} = {numerator_excel}")
    print(f"  P = 分子 / lp = {numerator_excel} / {lp_excel} = {P_excel_calc}")
    print(f"  ExcelのP = {excel_values['P']}")
    
    print(f"\n【差異の分析】")
    print(f"  lwの差: {lw} - {lw_excel} = {lw - lw_excel}")
    print(f"  この差によるWf*lwの差: {Wf * (lw - lw_excel)}")
    print(f"  Pの差: {result['P']} - {excel_values['P']} = {result['P'] - excel_values['P']}")

if __name__ == "__main__":
    test_p_calculation_detail()