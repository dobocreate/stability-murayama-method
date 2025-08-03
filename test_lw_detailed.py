"""
lw計算の詳細な分解検証
"""

import numpy as np
from murayama_calculator_revised import MurayamaCalculatorRevised

def test_lw_detailed():
    """lw計算の詳細な分解"""
    
    # パラメータ
    H = 9.9
    gamma = 25.5
    c = 253
    phi_deg = 21
    phi_rad = np.radians(phi_deg)
    H_f = 5.2
    alpha = 1.8
    K = 1.0
    
    # θ_d = 75°での計算（Excelデータが詳しい）
    theta_d_deg = 75
    theta_d_rad = np.radians(theta_d_deg)
    
    # 計算機インスタンス
    calculator = MurayamaCalculatorRevised(H_f, gamma, phi_deg, c, H, alpha, K, True)
    
    # 内部計算メソッドを直接呼び出し
    geom = calculator.calculate_geometry(theta_d_rad)
    r0 = geom['r0']
    rd = geom['rd'] 
    la = geom['la']
    B = geom['B']
    
    print("=== lw計算の詳細分解（θ_d = 75°）===")
    print(f"\n基本幾何パラメータ:")
    print(f"r0 = {r0:.15f}")
    print(f"rd = {rd:.15f}")
    print(f"la = {la:.15f}")
    print(f"B  = {B:.15f}")
    print(f"H_f = {H_f}")
    print(f"φ = {phi_deg}° = {phi_rad:.15f} rad")
    print(f"θ_d = {theta_d_deg}° = {theta_d_rad:.15f} rad")
    
    # 三角形部分（w1, lw1）
    print(f"\n--- 三角形部分の計算 ---")
    w1 = gamma * H_f * B / 2
    lw1 = la + B / 3
    print(f"w1 = γ * H_f * B / 2")
    print(f"   = {gamma} * {H_f} * {B} / 2")
    print(f"   = {w1:.15f}")
    print(f"\nlw1 = la + B / 3")
    print(f"    = {la} + {B} / 3")
    print(f"    = {lw1:.15f}")
    
    # Excel値との比較
    print(f"\nExcel値:")
    print(f"w1 (L9)  = 296.7383861432232")
    print(f"lw1 (K9) = 0.7929786419265843")
    print(f"差: w1  = {abs(w1 - 296.7383861432232):.2e}")
    print(f"差: lw1 = {abs(lw1 - 0.7929786419265843):.2e}")
    
    # 曲線部分（w2）
    print(f"\n--- 曲線部分の重量（w2）計算 ---")
    term2 = (rd**2 - r0**2) / (4 * np.tan(phi_rad))
    term3 = r0 * rd * np.sin(theta_d_rad) / 2
    w2 = gamma * (term2 - term3)
    
    print(f"term2 = (rd² - r0²) / (4 * tan(φ))")
    print(f"      = ({rd}² - {r0}²) / (4 * {np.tan(phi_rad)})")
    print(f"      = {rd**2 - r0**2} / {4 * np.tan(phi_rad)}")
    print(f"      = {term2:.15f}")
    
    print(f"\nterm3 = r0 * rd * sin(θ_d) / 2")
    print(f"      = {r0} * {rd} * {np.sin(theta_d_rad)} / 2")
    print(f"      = {term3:.15f}")
    
    print(f"\nw2 = γ * (term2 - term3)")
    print(f"   = {gamma} * ({term2} - {term3})")
    print(f"   = {w2:.15f}")
    
    print(f"\nExcel w2 (N9) = 137.55784282036365")
    print(f"差: {abs(w2 - 137.55784282036365):.2e}")
    
    # 曲線部分の重心（lw2）の詳細計算
    print(f"\n--- 曲線部分の重心（lw2）詳細計算 ---")
    
    # Step 1: O, P の計算
    O = np.hypot(B, H_f)
    P = np.arctan2(H_f, B)
    print(f"\nStep 1: 切羽の対角線")
    print(f"O = √(B² + H_f²) = √({B}² + {H_f}²)")
    print(f"  = {O:.15f}")
    print(f"P = arctan(H_f/B) = arctan({H_f}/{B})")
    print(f"  = {P:.15f} rad = {np.degrees(P):.15f}°")
    
    # Excel値
    print(f"\nExcel O (O9) = 6.86089059541736")
    print(f"Excel P (P9) = 49.28109185417627°")
    print(f"差: O = {abs(O - 6.86089059541736):.2e}")
    print(f"差: P = {abs(np.degrees(P) - 49.28109185417627):.2e}°")
    
    # Step 2: S の計算
    S = np.sqrt((O**2)/4.0 + r0**2 - O*r0*np.cos(P + phi_rad))
    print(f"\nStep 2: パラメータS")
    print(f"S = √(O²/4 + r0² - O*r0*cos(P + φ))")
    print(f"  = √({O}²/4 + {r0}² - {O}*{r0}*cos({P} + {phi_rad}))")
    print(f"  = √({O**2/4} + {r0**2} - {O*r0*np.cos(P + phi_rad)})")
    print(f"  = {S:.15f}")
    
    print(f"\nExcel S (S9) = 4.332310451453791")
    print(f"差: {abs(S - 4.332310451453791):.2e}")
    
    # Step 3: R, T の計算
    R = r0 * np.sin(P + phi_rad)
    print(f"\nStep 3: パラメータR, T")
    print(f"R = r0 * sin(P + φ)")
    print(f"  = {r0} * sin({P} + {phi_rad})")
    print(f"  = {r0} * sin({P + phi_rad})")
    print(f"  = {R:.15f}")
    
    print(f"\nExcel R (R9) = 3.808242381949598")
    print(f"差: {abs(R - 3.808242381949598):.2e}")
    
    T = np.arccos(np.clip(R/S, -1.0, 1.0)) - (P + phi_rad - np.pi/2.0)
    print(f"\nT = arccos(R/S) - (P + φ - π/2)")
    print(f"  = arccos({R}/{S}) - ({P} + {phi_rad} - {np.pi/2})")
    print(f"  = {np.arccos(R/S)} - {P + phi_rad - np.pi/2}")
    print(f"  = {T:.15f} rad = {np.degrees(T):.15f}°")
    
    print(f"\nExcel T (T9) = 48.19301504562269°")
    print(f"差: {abs(np.degrees(T) - 48.19301504562269):.2e}°")
    
    # Step 4: U の計算
    U = (r0*np.exp(T*np.tan(phi_rad)) - S) * (r0*np.sin(P + phi_rad)) / S
    print(f"\nStep 4: パラメータU")
    print(f"U = (r0*exp(T*tan(φ)) - S) * (r0*sin(P + φ)) / S")
    print(f"  = ({r0}*exp({T}*{np.tan(phi_rad)}) - {S}) * ({r0}*sin({P + phi_rad})) / {S}")
    print(f"  = ({r0*np.exp(T*np.tan(phi_rad))} - {S}) * {r0*np.sin(P + phi_rad)} / {S}")
    print(f"  = {U:.15f}")
    
    print(f"\nExcel U (U9) = 1.103080354051158")
    print(f"差: {abs(U - 1.103080354051158):.2e}")
    
    # Step 5: lw2 の計算
    lw2 = S*np.cos(phi_rad + T) + (2.0/3.0)*U*np.cos(np.arctan2(B, H_f))
    print(f"\nStep 5: lw2の計算")
    print(f"lw2 = S*cos(φ + T) + (2/3)*U*cos(arctan(B/H_f))")
    print(f"    = {S}*cos({phi_rad} + {T}) + (2/3)*{U}*cos(arctan({B}/{H_f}))")
    print(f"    = {S}*cos({phi_rad + T}) + {2/3*U}*cos({np.arctan2(B, H_f)})")
    print(f"    = {S*np.cos(phi_rad + T)} + {(2/3)*U*np.cos(np.arctan2(B, H_f))}")
    print(f"    = {lw2:.15f}")
    
    # 最終的なlw
    lw = (w1 * lw1 + w2 * lw2) / (w1 + w2)
    print(f"\n--- 最終的なlw計算 ---")
    print(f"lw = (w1 * lw1 + w2 * lw2) / (w1 + w2)")
    print(f"   = ({w1} * {lw1} + {w2} * {lw2}) / ({w1} + {w2})")
    print(f"   = ({w1 * lw1} + {w2 * lw2}) / {w1 + w2}")
    print(f"   = {lw:.15f}")
    
    print(f"\nExcel lw (J9) = 1.136070940712082")
    print(f"差: {abs(lw - 1.136070940712082):.2e}")
    
    # lw2をExcel値から逆算
    lw_excel = 1.136070940712082
    lw2_excel = (lw_excel * (w1 + w2) - w1 * lw1) / w2
    print(f"\n--- Excel lw2の逆算 ---")
    print(f"lw2_excel = (lw_excel * (w1 + w2) - w1 * lw1) / w2")
    print(f"          = ({lw_excel} * {w1 + w2} - {w1} * {lw1}) / {w2}")
    print(f"          = {lw2_excel:.15f}")
    print(f"\nPython lw2: {lw2:.15f}")
    print(f"差: {abs(lw2 - lw2_excel):.2e}")

if __name__ == "__main__":
    test_lw_detailed()