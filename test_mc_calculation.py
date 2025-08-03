"""
粘着抵抗モーメントMcの計算検証
"""

import numpy as np

def test_mc_calculation():
    """Mc計算の検証"""
    
    # パラメータ
    c = 20  # kPa
    phi_deg = 30
    phi_rad = np.radians(phi_deg)
    r0 = 7.515861474682187
    rd = 13.757930737341093
    
    print("=== 粘着抵抗モーメントMcの計算検証 ===\n")
    
    print(f"パラメータ:")
    print(f"  c = {c} kPa")
    print(f"  φ = {phi_deg}°")
    print(f"  r0 = {r0} m")
    print(f"  rd = {rd} m")
    
    # 標準的な計算
    Mc_standard = c * (rd**2 - r0**2) / (2 * np.tan(phi_rad))
    
    print(f"\n標準的な計算:")
    print(f"  Mc = c * (rd² - r0²) / (2*tan(φ))")
    print(f"     = {c} * ({rd}² - {r0}²) / (2*tan({phi_deg}°))")
    print(f"     = {c} * ({rd**2} - {r0**2}) / {2 * np.tan(phi_rad)}")
    print(f"     = {c} * {rd**2 - r0**2} / {2 * np.tan(phi_rad)}")
    print(f"     = {Mc_standard}")
    
    # P計算から逆算
    # Excel値
    Wf = 905.41568258
    lw = 2.61615258
    q = 167.06849771
    B = 6.508926968399547
    la = 8.427753792796626e-16
    lp = 8.757930737341093
    P_excel = 322.93447293
    
    print(f"\nExcelのP値から逆算:")
    print(f"  P = (Wf*lw + q*B*(la+B/2) - Mc) / lp")
    print(f"  {P_excel} = ({Wf}*{lw} + {q}*{B}*({la}+{B/2}) - Mc) / {lp}")
    
    numerator_without_mc = Wf * lw + q * B * (la + B/2)
    print(f"  {P_excel} = ({numerator_without_mc} - Mc) / {lp}")
    print(f"  {P_excel} * {lp} = {numerator_without_mc} - Mc")
    print(f"  {P_excel * lp} = {numerator_without_mc} - Mc")
    
    Mc_from_excel = numerator_without_mc - P_excel * lp
    print(f"  Mc = {numerator_without_mc} - {P_excel * lp}")
    print(f"  Mc = {Mc_from_excel}")
    
    print(f"\n差異:")
    print(f"  標準的なMc = {Mc_standard}")
    print(f"  Excel逆算Mc = {Mc_from_excel}")
    print(f"  差 = {Mc_standard - Mc_from_excel}")
    print(f"  比率 = {Mc_from_excel / Mc_standard}")
    
    # 可能性のある計算方法
    print(f"\n他の可能性:")
    
    # 単位の問題？
    Mc_kN = Mc_standard / 1000  # kPaからkN/m²への変換を忘れている？
    print(f"  Mc (kN単位?) = {Mc_kN}")
    
    # 係数の違い？
    Mc_half = Mc_standard / 2
    print(f"  Mc / 2 = {Mc_half}")
    
    # 異なる式？
    Mc_simple = c * (rd - r0)**2 / (2 * np.tan(phi_rad))
    print(f"  c * (rd - r0)² / (2*tan(φ)) = {Mc_simple}")

if __name__ == "__main__":
    test_mc_calculation()