"""
q計算の詳細検証
"""

import numpy as np
from murayama_calculator_revised import MurayamaCalculatorRevised

def test_q_calculation():
    """q計算の詳細検証"""
    
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
    
    print("=== q計算の詳細検証 ===\n")
    
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
    
    # 手動計算
    phi_rad = np.radians(params['phi_deg'])
    theta_d_rad = np.radians(params['theta_d_deg'])
    
    # 幾何計算
    geom = calculator.calculate_geometry(theta_d_rad)
    B = geom['B']
    
    print(f"パラメータ:")
    print(f"  H = {params['H']}")
    print(f"  γ = {params['gamma']}")
    print(f"  c = {params['c']}")
    print(f"  φ = {params['phi_deg']}° = {phi_rad} rad")
    print(f"  B = {B}")
    print(f"  α = {params['alpha']}")
    print(f"  K = {params['K']}")
    
    # q計算の詳細
    result = calculator.calculate_support_pressure(theta_d_rad)
    q_python = result['q']
    
    print(f"\nPython計算:")
    print(f"  q = {q_python}")
    
    # Excel値
    q_excel = 90.0
    print(f"\nExcel値:")
    print(f"  q = {q_excel}")
    
    # 手動計算で確認
    print(f"\n手動計算（Python式）:")
    alpha_B = params['alpha'] * B
    term1 = alpha_B * (params['gamma'] - 2 * params['c'] / alpha_B)
    term2 = 2 * params['K'] * np.tan(phi_rad)
    
    if params['H'] is not None:
        exp_term = 1 - np.exp(-2 * params['K'] * params['H'] / alpha_B * np.tan(phi_rad))
    else:
        exp_term = 1
    
    q_manual = term1 / term2 * exp_term
    
    print(f"  α*B = {alpha_B}")
    print(f"  γ - 2c/(α*B) = {params['gamma']} - 2*{params['c']}/{alpha_B} = {params['gamma'] - 2 * params['c'] / alpha_B}")
    print(f"  2*K*tan(φ) = 2*{params['K']}*tan({params['phi_deg']}°) = {term2}")
    print(f"  exp項 = {exp_term}")
    print(f"  q = {q_manual}")
    
    # Excelの解釈（α/2を使用）
    print(f"\n手動計算（Excel解釈: α/2 = 0.9）:")
    alpha_half = params['alpha'] / 2
    alpha_half_B = alpha_half * B
    term1_excel = alpha_half_B * (params['gamma'] - 2 * params['c'] / alpha_half_B)
    
    if params['H'] is not None:
        exp_term_excel = 1 - np.exp(-2 * params['K'] * params['H'] / alpha_half_B * np.tan(phi_rad))
    else:
        exp_term_excel = 1
    
    q_excel_calc = term1_excel / term2 * exp_term_excel
    
    print(f"  (α/2)*B = {alpha_half}*{B} = {alpha_half_B}")
    print(f"  γ - 2c/((α/2)*B) = {params['gamma']} - 2*{params['c']}/{alpha_half_B} = {params['gamma'] - 2 * params['c'] / alpha_half_B}")
    print(f"  exp項 = {exp_term_excel}")
    print(f"  q = {q_excel_calc}")
    
    print(f"\n差異分析:")
    print(f"  Python q = {q_python}")
    print(f"  Excel q = {q_excel}")
    print(f"  差 = {abs(q_python - q_excel)}")
    print(f"  相対誤差 = {abs(q_python - q_excel) / q_excel * 100:.1f}%")

if __name__ == "__main__":
    test_q_calculation()