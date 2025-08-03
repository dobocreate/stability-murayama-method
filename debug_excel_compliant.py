"""
Excel準拠実装のデバッグ
"""

import numpy as np
from murayama_calculator_revised import MurayamaCalculatorRevised

def debug_excel_compliant():
    """Excel準拠実装のデバッグ"""
    
    # テストケース2のパラメータ
    H = 50
    gamma = 20
    c = 20
    phi_deg = 30
    H_f = 10
    theta_d_deg = 60
    
    print("=== Excel準拠実装のデバッグ ===\n")
    
    # 計算機インスタンス
    calculator = MurayamaCalculatorRevised(H_f, gamma, phi_deg, c, H, 1.8, 1.0, True)
    
    # 手動計算
    theta_d_rad = np.radians(theta_d_deg)
    phi_rad = np.radians(phi_deg)
    
    # 幾何計算
    geom = calculator.calculate_geometry(theta_d_rad)
    B = geom['B']
    r0 = geom['r0']
    la = geom['la']
    
    print(f"基本パラメータ:")
    print(f"H (土被り) = {H}")
    print(f"H_f (切羽高さ) = {H_f}")
    print(f"B = {B}")
    print(f"r0 = {r0}")
    print(f"la = {la}")
    print(f"φ = {phi_deg}° = {phi_rad} rad")
    
    # Excel準拠の計算
    # l, αの定義
    l = np.sqrt(B**2 + H**2)
    alpha = np.arctan2(H, B)
    
    print(f"\n中間計算:")
    print(f"l = √(B² + H²) = √({B}² + {H}²) = {l}")
    print(f"α = arctan(H/B) = arctan({H}/{B}) = {alpha} rad = {np.degrees(alpha)}°")
    
    # xの計算
    cos_term = np.cos(alpha + phi_rad - np.pi/2)
    x = np.sqrt(l**2 + r0**2 - l*r0*cos_term)
    
    print(f"\nx の計算:")
    print(f"α + φ - π/2 = {alpha} + {phi_rad} - {np.pi/2} = {alpha + phi_rad - np.pi/2}")
    print(f"cos(α + φ - π/2) = {cos_term}")
    print(f"x = √(l² + r0² - l*r0*cos(α+φ-π/2))")
    print(f"  = √({l}² + {r0}² - {l}*{r0}*{cos_term})")
    print(f"  = {x}")
    
    # Excel値との比較
    print(f"\nExcel値:")
    print(f"x (S9) = 9.343066058315848")
    print(f"差: {abs(x - 9.343066058315848)}")
    
    # θcの計算
    sin_term = r0*np.sin(alpha + phi_rad) / x
    theta_c = np.arccos(np.clip(sin_term, -1, 1)) - (alpha + phi_rad - np.pi/2)
    
    print(f"\nθc の計算:")
    print(f"sin項 = r0*sin(α+φ)/x = {r0}*sin({alpha + phi_rad})/{x} = {sin_term}")
    print(f"θc = arccos(sin項) - (α+φ-π/2)")
    print(f"   = {np.arccos(np.clip(sin_term, -1, 1))} - {alpha + phi_rad - np.pi/2}")
    print(f"   = {theta_c} rad = {np.degrees(theta_c)}°")
    
    print(f"\nExcel θc (T9) = 39.614839509609574°")
    print(f"差: {abs(np.degrees(theta_c) - 39.614839509609574)}°")
    
    # デバッグ: 符号の問題を確認
    print(f"\n符号の確認:")
    print(f"α + φ = {np.degrees(alpha + phi_rad)}°")
    print(f"α + φ - 90° = {np.degrees(alpha + phi_rad - np.pi/2)}°")
    
    # 別の計算方法を試す
    print(f"\n別の解釈:")
    # Excelがsin(α+φ-π/2)を使っている可能性
    sin_alt = r0*np.sin(alpha + phi_rad - np.pi/2) / x
    print(f"sin(α+φ-π/2)/x = {sin_alt}")

if __name__ == "__main__":
    debug_excel_compliant()