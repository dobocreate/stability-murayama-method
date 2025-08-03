"""
Excel実装とPython実装の計算結果比較テストスクリプト
"""

import numpy as np
from murayama_calculator_revised import MurayamaCalculatorRevised

def test_excel_comparison():
    """Excel実装の結果と比較"""
    
    # Excelファイルのパラメータ（起点側シート）
    H = 9.9         # 土被り [m]
    gamma = 25.5    # 単位体積重量 [kN/m³]
    c = 253         # 粘着力 [kPa]
    phi_deg = 21    # 内部摩擦角 [度]
    H_f = 5.2       # 掘削高さ [m]
    
    # デフォルトパラメータ
    alpha = 1.8     # 影響幅係数
    K = 1.0         # 経験係数
    
    print("=== パラメータ ===")
    print(f"土被り H: {H} m")
    print(f"単位体積重量 γ: {gamma} kN/m³")
    print(f"粘着力 c: {c} kPa")
    print(f"内部摩擦角 φ: {phi_deg}°")
    print(f"掘削高さ H_f: {H_f} m")
    print(f"影響幅係数 α: {alpha}")
    print(f"経験係数 K: {K}")
    print()
    
    # 計算機インスタンスの作成（有限土被り式を強制使用）
    calculator = MurayamaCalculatorRevised(
        H_f=H_f, 
        gamma=gamma, 
        phi=phi_deg, 
        coh=c,
        H=H, 
        alpha=alpha, 
        K=K,
        force_finite_cover=True  # 有限土被り式を強制
    )
    
    # Excel行9のθ_d = 75°での計算
    theta_d_deg = 75
    theta_d_rad = np.radians(theta_d_deg)
    
    print(f"=== θ_d = {theta_d_deg}° での計算結果 ===")
    
    # Python計算
    result = calculator.calculate_support_pressure(theta_d_rad)
    
    # Excel値（行9）
    excel_values = {
        'B': 4.475692098691149,
        'r0': 4.045471892076639,
        'rd': 6.686396245146749,
        'la': -0.6989187243037986,
        'lp': 4.049767466906651,
        'q': -239.0930847591986,
        'Wf': 434.29622896358677,
        'lw': 1.136070940712082,
        'P': -2434.7018976765366
    }
    
    # 比較結果
    print("\n--- 幾何パラメータ ---")
    print(f"B  : Python = {result['geometry']['B']:.15f}, Excel = {excel_values['B']}, 差 = {abs(result['geometry']['B'] - excel_values['B']):.2e}")
    print(f"r0 : Python = {result['geometry']['r0']:.15f}, Excel = {excel_values['r0']}, 差 = {abs(result['geometry']['r0'] - excel_values['r0']):.2e}")
    print(f"rd : Python = {result['geometry']['rd']:.15f}, Excel = {excel_values['rd']}, 差 = {abs(result['geometry']['rd'] - excel_values['rd']):.2e}")
    print(f"la : Python = {result['geometry']['la']:.15f}, Excel = {excel_values['la']}, 差 = {abs(result['geometry']['la'] - excel_values['la']):.2e}")
    print(f"lp : Python = {result['geometry']['lp']:.15f}, Excel = {excel_values['lp']}, 差 = {abs(result['geometry']['lp'] - excel_values['lp']):.2e}")
    
    print("\n--- 荷重パラメータ ---")
    print(f"q  : Python = {result['q']:.15f}, Excel = {excel_values['q']}, 差 = {abs(result['q'] - excel_values['q']):.2e}")
    print(f"Wf : Python = {result['Wf']:.15f}, Excel = {excel_values['Wf']}, 差 = {abs(result['Wf'] - excel_values['Wf']):.2e}")
    print(f"lw : Python = {result['lw']:.15f}, Excel = {excel_values['lw']}, 差 = {abs(result['lw'] - excel_values['lw']):.2e}")
    
    print("\n--- 支保圧 ---")
    print(f"P  : Python = {result['P']:.15f}, Excel = {excel_values['P']}, 差 = {abs(result['P'] - excel_values['P']):.2e}")
    
    # q計算の詳細比較
    print("\n=== q計算の詳細比較 ===")
    phi_rad = np.radians(phi_deg)
    B = result['geometry']['B']
    
    # Python式の展開
    # q = (alpha * B * (gamma - 2 * coh / (alpha * B))) / (2 * K * np.tan(phi)) * fac
    # where fac = 1.0 - np.exp(-2.0 * K * H * np.tan(phi) / (alpha * B))
    
    print(f"\nPython計算の詳細:")
    print(f"α * B = {alpha} * {B} = {alpha * B}")
    print(f"2 * c / (α * B) = 2 * {c} / {alpha * B} = {2 * c / (alpha * B)}")
    print(f"γ - 2c/(αB) = {gamma} - {2 * c / (alpha * B)} = {gamma - 2 * c / (alpha * B)}")
    print(f"tan(φ) = tan({phi_deg}°) = {np.tan(phi_rad)}")
    print(f"2 * K * tan(φ) = 2 * {K} * {np.tan(phi_rad)} = {2 * K * np.tan(phi_rad)}")
    
    fac = 1.0 - np.exp(-2.0 * K * H * np.tan(phi_rad) / (alpha * B))
    print(f"\n指数部: -2KH*tan(φ)/(αB) = -{2 * K * H * np.tan(phi_rad) / (alpha * B)}")
    print(f"fac = 1 - exp({-2 * K * H * np.tan(phi_rad) / (alpha * B)}) = {fac}")
    
    q_python = (alpha * B * (gamma - 2 * c / (alpha * B))) / (2 * K * np.tan(phi_rad)) * fac
    print(f"\nq = {q_python}")
    
    # Excel式との比較
    print(f"\n\nExcel式との対応:")
    print(f"Excel係数0.9 = Python α/2 = {alpha}/2 = {alpha/2}")
    print(f"つまり、Excel式の0.9はPythonのα/2に相当")
    
    # より多くのθ_dでテスト
    print("\n\n=== 複数のθ_dでの比較 ===")
    test_angles = [70, 72, 74, 75, 76, 78, 80]
    excel_q_values = {
        70: -213.5516165088176,
        72: -227.0502087840598,
        74: -245.48116487493414,
        75: -239.0930847591986,
        76: -263.2050255908037,
        78: -280.3872095335259,
        80: -298.82606586456686
    }
    
    print(f"{'θ_d[°]':>8} | {'Python q':>20} | {'Excel q':>20} | {'差':>15} | {'相対誤差[%]':>12}")
    print("-" * 90)
    
    for theta_deg in test_angles:
        theta_rad = np.radians(theta_deg)
        result = calculator.calculate_support_pressure(theta_rad)
        q_python = result['q']
        
        if theta_deg in excel_q_values:
            q_excel = excel_q_values[theta_deg]
            diff = abs(q_python - q_excel)
            rel_error = diff / abs(q_excel) * 100 if q_excel != 0 else 0
            print(f"{theta_deg:8} | {q_python:20.10f} | {q_excel:20.10f} | {diff:15.2e} | {rel_error:12.2e}")

if __name__ == "__main__":
    test_excel_comparison()