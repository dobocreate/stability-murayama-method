"""
lw（重心位置）計算の詳細比較
"""

import numpy as np
from murayama_calculator_revised import MurayamaCalculatorRevised

def test_lw_calculation():
    """lw計算の詳細比較"""
    
    # パラメータ
    H = 9.9
    gamma = 25.5
    c = 253
    phi_deg = 21
    phi_rad = np.radians(phi_deg)
    H_f = 5.2
    alpha = 1.8
    K = 1.0
    
    # θ_d = 75°での計算
    theta_d_deg = 75
    theta_d_rad = np.radians(theta_d_deg)
    
    # 計算機インスタンス
    calculator = MurayamaCalculatorRevised(H_f, gamma, phi_deg, c, H, alpha, K, True)
    result = calculator.calculate_support_pressure(theta_d_rad)
    
    # 幾何パラメータ
    r0 = result['geometry']['r0']
    rd = result['geometry']['rd']
    la = result['geometry']['la']
    B = result['geometry']['B']
    
    print("=== lw計算の詳細比較 ===")
    print(f"\n幾何パラメータ:")
    print(f"r0 = {r0}")
    print(f"rd = {rd}")
    print(f"la = {la}")
    print(f"B = {B}")
    print(f"θ_d = {theta_d_deg}°")
    
    # Excel計算の再現
    print(f"\n--- Excel計算の再現 ---")
    
    # w1, lw1の計算
    w1 = gamma * H_f * B / 2
    lw1 = la + B / 3
    print(f"w1 (三角形部分の重量) = {w1}")
    print(f"lw1 (三角形重心) = la + B/3 = {la} + {B}/3 = {lw1}")
    
    # w2の計算
    term2 = (rd**2 - r0**2) / (4 * np.tan(phi_rad))
    term3 = r0 * rd * np.sin(theta_d_rad) / 2
    w2 = gamma * (term2 - term3)
    print(f"\nw2 (曲線部分の重量) = {w2}")
    
    # 曲線領域の重心計算用パラメータ
    O = np.hypot(B, H_f)
    P = np.arctan2(H_f, B)
    S = np.sqrt((O**2)/4.0 + r0**2 - O*r0*np.cos(P + phi_rad))
    R = r0 * np.sin(P + phi_rad)
    T = np.arccos(R / S) - (P + phi_rad - np.pi/2.0)
    U = (r0*np.exp(T*np.tan(phi_rad)) - S) * (r0*np.sin(P + phi_rad)) / S
    
    print(f"\n曲線領域の重心計算パラメータ:")
    print(f"O = {O}")
    print(f"P = {P} rad = {np.degrees(P)}°")
    print(f"S = {S}")
    print(f"R = {R}")
    print(f"T = {T} rad = {np.degrees(T)}°")
    print(f"U = {U}")
    
    # lw2の計算（Python実装）
    lw2_python = S*np.cos(phi_rad + T) + (2.0/3.0)*U*np.cos(np.arctan2(B, H_f))
    print(f"\nlw2 (Python) = {lw2_python}")
    
    # Excel計算結果
    lw_excel = 1.136070940712082
    lw1_excel = 0.7929786419265843  # K9の値
    
    # 重み付き平均からlw2を逆算
    lw2_excel_calc = (lw_excel * (w1 + w2) - w1 * lw1) / w2
    print(f"lw2 (Excelから逆算) = {lw2_excel_calc}")
    
    # 最終的なlw
    lw_python = (w1 * lw1 + w2 * lw2_python) / (w1 + w2)
    print(f"\n最終的なlw:")
    print(f"Python: {lw_python}")
    print(f"Excel: {lw_excel}")
    print(f"差: {abs(lw_python - lw_excel)}")
    
    # 支保圧への影響
    print(f"\n--- 支保圧への影響 ---")
    q = result['q']
    Mc = result['Mc']
    lp = result['geometry']['lp']
    Wf = result['Wf']
    
    # Pythonのlwを使った場合
    P_python = (Wf * lw_python + q * B * (la + B/2) - Mc) / lp
    
    # ExcelのlwlExcel = 1.136070940712082を使った場合
    P_excel_lw = (Wf * lw_excel + q * B * (la + B/2) - Mc) / lp
    
    print(f"P (Python lw使用): {P_python}")
    print(f"P (Excel lw使用): {P_excel_lw}")
    print(f"Excel記載のP値: -2434.7018976765366")
    print(f"\nPythonでExcelのlwを使った場合の差: {abs(P_excel_lw - (-2434.7018976765366))}")

if __name__ == "__main__":
    test_lw_calculation()