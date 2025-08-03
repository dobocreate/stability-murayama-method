"""
Excel x計算の詳細確認
"""

import numpy as np

def debug_x_calculation():
    """x計算の詳細確認"""
    
    # パラメータ
    B = 6.508926968399547
    H = 50
    H_f = 10
    r0 = 7.515861474682187
    phi_deg = 30
    phi_rad = np.radians(phi_deg)
    
    print("=== x計算の詳細確認 ===\n")
    
    # 方法1: l²を使用（元の解釈）
    l = np.sqrt(B**2 + H**2)
    alpha = np.arctan2(H, B)
    x1 = np.sqrt(l**2 + r0**2 - l*r0*np.cos(alpha + phi_rad - np.pi/2))
    
    print(f"方法1: l²を使用")
    print(f"l = {l}")
    print(f"x = {x1}")
    
    # 方法2: O²/4を使用（Pythonの元の実装と同じ）
    O = np.sqrt(B**2 + H_f**2)
    P = np.arctan2(H_f, B)
    x2 = np.sqrt((O**2)/4.0 + r0**2 - O*r0*np.cos(P + phi_rad))
    
    print(f"\n方法2: O²/4を使用（H_f使用）")
    print(f"O = √(B² + H_f²) = {O}")
    print(f"x (S) = {x2}")
    
    # 方法3: 混合（OはH_fから、αはHから）
    O_Hf = np.sqrt(B**2 + H_f**2)
    alpha_H = np.arctan2(H, B)
    x3 = np.sqrt((O_Hf**2)/4.0 + r0**2 - O_Hf*r0*np.cos(alpha_H + phi_rad - np.pi/2))
    
    print(f"\n方法3: 混合アプローチ")
    print(f"O (H_fから) = {O_Hf}")
    print(f"α (Hから) = {np.degrees(alpha_H)}°")
    print(f"x = {x3}")
    
    # Excel値
    print(f"\nExcel x (S9) = 9.343066058315848")
    
    # 方法4: Excel実際の計算を推測
    # Excelの値に最も近いのは方法2
    print(f"\n最も近い値: 方法2 = {x2}")
    print(f"差: {abs(x2 - 9.343066058315848)}")
    
    # 詳細確認
    print(f"\n詳細確認（方法2）:")
    print(f"P = arctan(H_f/B) = arctan({H_f}/{B}) = {P} rad = {np.degrees(P)}°")
    print(f"P + φ = {np.degrees(P + phi_rad)}°")
    print(f"cos(P + φ) = {np.cos(P + phi_rad)}")
    
    # θcの計算（方法2ベース）
    if x2 > 0:
        sin_term = r0 * np.sin(P + phi_rad) / x2
        theta_c = np.arccos(np.clip(sin_term, -1, 1)) - (P + phi_rad - np.pi/2)
        print(f"\nθc計算（方法2）:")
        print(f"θc = {np.degrees(theta_c)}°")
        print(f"Excel θc (T9) = 39.614839509609574°")
        print(f"差: {abs(np.degrees(theta_c) - 39.614839509609574)}°")

if __name__ == "__main__":
    debug_x_calculation()