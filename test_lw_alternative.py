"""
lw計算の代替式検証
"""

import numpy as np

def test_lw_alternative():
    """代替的なlw計算式の検証"""
    
    # パラメータ
    gamma = 25.5
    phi_deg = 21
    phi_rad = np.radians(phi_deg)
    H_f = 5.2
    
    # θ_d = 75°の値
    r0 = 4.045471892076640
    rd = 6.686396245146751
    B = 4.475692098691150
    la = -0.698918724303799
    theta_d_rad = np.radians(75)
    
    # 重量計算
    w1 = 296.738386143223238  # 三角形部分
    w2 = 137.557842820363845  # 曲線部分
    lw1 = 0.792978641926585   # 三角形重心
    
    # Excel逆算値
    lw_excel = 1.136070940712082
    lw2_excel_reverse = 1.876186174801123
    
    print("=== 代替的なlw2計算式の検証 ===")
    
    # 可能性1: 単純な幾何学的近似
    print("\n--- 可能性1: 単純な幾何学的近似 ---")
    lw2_approx1 = la + B * 2/3
    print(f"lw2 = la + B * 2/3")
    print(f"    = {la} + {B} * 2/3")
    print(f"    = {lw2_approx1}")
    print(f"Excel逆算値との差: {abs(lw2_approx1 - lw2_excel_reverse)}")
    
    # 可能性2: 切羽中心からの距離
    print("\n--- 可能性2: 切羽中心基準 ---")
    lw2_approx2 = B/2  # 切羽中心から
    print(f"lw2 = B/2 = {lw2_approx2}")
    print(f"Excel逆算値との差: {abs(lw2_approx2 - lw2_excel_reverse)}")
    
    # 可能性3: 係数調整
    print("\n--- 可能性3: 係数調整 ---")
    for factor in [0.4, 0.42, 0.45, 0.5, 0.55, 0.6]:
        lw2_test = la + B * factor
        lw_test = (w1 * lw1 + w2 * lw2_test) / (w1 + w2)
        diff = abs(lw_test - lw_excel)
        print(f"factor = {factor}: lw2 = {lw2_test:.6f}, lw = {lw_test:.6f}, 差 = {diff:.6f}")
    
    # 最適な係数を探索
    print("\n--- 最適係数の探索 ---")
    best_factor = 0
    min_diff = float('inf')
    for factor in np.linspace(0.3, 0.7, 1000):
        lw2_test = la + B * factor
        lw_test = (w1 * lw1 + w2 * lw2_test) / (w1 + w2)
        diff = abs(lw_test - lw_excel)
        if diff < min_diff:
            min_diff = diff
            best_factor = factor
    
    lw2_best = la + B * best_factor
    print(f"最適係数: {best_factor:.6f}")
    print(f"lw2 = la + B * {best_factor:.6f} = {lw2_best:.6f}")
    print(f"結果のlw: {(w1 * lw1 + w2 * lw2_best) / (w1 + w2):.6f}")
    print(f"Excel値との差: {min_diff:.2e}")
    
    # 可能性4: 別の基準点
    print("\n--- 可能性4: 異なる基準点 ---")
    # 切羽面からの絶対距離として
    lw2_abs = abs(la) + B * 0.55  # 推定
    print(f"lw2 = |la| + B * 0.55 = {abs(la)} + {B} * 0.55 = {lw2_abs}")
    lw_abs = (w1 * lw1 + w2 * lw2_abs) / (w1 + w2)
    print(f"結果のlw: {lw_abs}")
    print(f"Excel値との差: {abs(lw_abs - lw_excel)}")
    
    # Excel M9式の簡略化された可能性
    print("\n--- Excel M9式の簡略化の可能性 ---")
    # Sとcos項を使った簡略式
    S = 4.332310451453791
    T_rad = 0.841126789009281
    
    # 可能な簡略式1
    lw2_simp1 = S * np.cos(phi_rad + T_rad) + B/3
    print(f"lw2 = S*cos(φ+T) + B/3 = {lw2_simp1}")
    print(f"Excel逆算値との差: {abs(lw2_simp1 - lw2_excel_reverse)}")
    
    # 可能な簡略式2
    lw2_simp2 = la + S * np.sin(phi_rad + T_rad)
    print(f"lw2 = la + S*sin(φ+T) = {lw2_simp2}")
    print(f"Excel逆算値との差: {abs(lw2_simp2 - lw2_excel_reverse)}")
    
    # 実際のExcel値から係数を逆算
    print("\n--- Excel実装の推定 ---")
    # lw2_excel_reverse = 1.876186174801123
    # これが la + B * x の形だとすると
    x_factor = (lw2_excel_reverse - la) / B
    print(f"Excel lw2が la + B * x の形だとすると:")
    print(f"x = (lw2 - la) / B = ({lw2_excel_reverse} - {la}) / {B}")
    print(f"x = {x_factor:.6f}")
    print(f"これは約 {x_factor:.3f} ≈ {round(x_factor*12)/12:.3f}")

if __name__ == "__main__":
    test_lw_alternative()