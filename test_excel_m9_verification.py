"""
Excel M9式とPython実装の比較検証（新パラメータ）
"""

import numpy as np
from murayama_calculator_revised import MurayamaCalculatorRevised

def verify_excel_m9():
    """新しいExcelファイルのパラメータでM9式を検証"""
    
    # 新しいExcelファイルのパラメータ
    H = 50          # 土被り
    gamma = 20      # 単位体積重量
    coh = 20        # 粘着力
    phi_deg = 30    # 内部摩擦角
    H_f = 10        # 掘削高さ
    alpha = 1.8     # 影響幅係数（デフォルト）
    K = 1.0         # 経験係数（デフォルト）
    
    # θ_d = 60°での計算
    theta_d_deg = 60
    theta_d_rad = np.radians(theta_d_deg)
    
    print("=== 新パラメータでの検証 ===")
    print(f"パラメータ:")
    print(f"H = {H}, γ = {gamma}, c = {coh}, φ = {phi_deg}°, H_f = {H_f}")
    print(f"θ_d = {theta_d_deg}°")
    
    # Python実装での計算
    calculator = MurayamaCalculatorRevised(H_f, gamma, phi_deg, coh, H, alpha, K, force_finite_cover=True)
    result = calculator.calculate_support_pressure(theta_d_rad)
    
    # Excel値
    excel_values = {
        'B': 6.508926968399547,
        'r0': 7.515861474682187,
        'rd': 13.757930737341093,
        'la': 8.427753792796626e-16,
        'lp': 8.757930737341093,
        'q': 167.06849770684155,
        'Wf': 905.4156825829673,
        'lw': 2.6161525827276515,
        'lw1': 2.16964232279985,
        'lw2': 3.758015139473548,
        'w1': 650.8926968399547,
        'w2': 254.52298574301267
    }
    
    print("\n=== 幾何パラメータの比較 ===")
    print(f"B  : Python = {result['geometry']['B']:.10f}, Excel = {excel_values['B']}")
    print(f"r0 : Python = {result['geometry']['r0']:.10f}, Excel = {excel_values['r0']}")
    print(f"rd : Python = {result['geometry']['rd']:.10f}, Excel = {excel_values['rd']}")
    
    print("\n=== 重量計算の比較 ===")
    # Pythonの重量計算詳細
    geom = result['geometry']
    phi_rad = np.radians(phi_deg)
    
    # w1計算
    w1_python = gamma * H_f * geom['B'] / 2
    print(f"w1 : Python = {w1_python:.10f}, Excel = {excel_values['w1']}")
    
    # w2計算
    term2 = (geom['rd']**2 - geom['r0']**2) / (4 * np.tan(phi_rad))
    term3 = geom['r0'] * geom['rd'] * np.sin(theta_d_rad) / 2
    w2_python = gamma * (term2 - term3)
    print(f"w2 : Python = {w2_python:.10f}, Excel = {excel_values['w2']}")
    
    print("\n=== 重心位置の比較 ===")
    # lw1
    lw1_python = geom['la'] + geom['B'] / 3
    print(f"lw1: Python = {lw1_python:.10f}, Excel = {excel_values['lw1']}")
    
    # lw2の詳細計算（Python方式）
    weight_params = calculator.calculate_self_weight(
        geom['r0'], geom['rd'], theta_d_rad, geom['B'], geom['la']
    )
    
    # lw2をPythonの内部計算から取得
    # 重み付き平均からlw2を逆算
    lw_python = weight_params['lw']
    lw2_python_reverse = (lw_python * (w1_python + w2_python) - w1_python * lw1_python) / w2_python
    
    print(f"lw2: Python（逆算） = {lw2_python_reverse:.10f}, Excel = {excel_values['lw2']}")
    print(f"lw : Python = {lw_python:.10f}, Excel = {excel_values['lw']}")
    
    # Excel M9式の検証
    print("\n=== Excel M9式の検証 ===")
    # Excel式で使用される中間値
    phi_rad = np.radians(phi_deg)
    B = geom['B']
    r0 = geom['r0']
    
    O = np.hypot(B, H_f)
    P_rad = np.arctan2(H_f, B)
    P_deg = np.degrees(P_rad)
    S = np.sqrt((O**2)/4.0 + r0**2 - O*r0*np.cos(P_rad + phi_rad))
    R = r0 * np.sin(P_rad + phi_rad)
    T_rad = np.arccos(np.clip(R/S, -1, 1)) - (P_rad + phi_rad - np.pi/2)
    T_deg = np.degrees(T_rad)
    U = (r0*np.exp(T_rad*np.tan(phi_rad)) - S) * (r0*np.sin(P_rad + phi_rad)) / S
    V_rad = np.pi - 2*np.arctan(O/2/U)
    V_deg = np.degrees(V_rad)
    
    print(f"S = {S:.10f}")
    print(f"T = {T_deg:.10f}°")
    print(f"U = {U:.10f}")
    print(f"V = {V_deg:.10f}°")
    
    # Excel M9式の計算
    term1 = S * np.cos(np.radians(phi_deg + T_deg))
    
    cos_V_rad = np.cos(V_rad)
    sin_V_rad = np.sin(V_rad)
    
    A = U / (1 - cos_V_rad)
    B_num = 1 - cos_V_rad**2
    B_den = V_rad - sin_V_rad * cos_V_rad
    B_frac = B_num / B_den
    C = sin_V_rad
    D = U * cos_V_rad / (1 - cos_V_rad)
    
    term2 = (2/3) * (A * B_frac * C - D) * np.cos(np.arctan(B / H_f))
    
    lw2_excel_formula = term1 + term2
    print(f"\nExcel M9式による lw2 = {lw2_excel_formula:.10f}")
    print(f"Excel実際の値: {excel_values['lw2']}")
    print(f"差: {abs(lw2_excel_formula - excel_values['lw2']):.2e}")

if __name__ == "__main__":
    verify_excel_m9()