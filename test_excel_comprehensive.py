"""
Excel実装とPython実装の包括的な比較テスト
w1, lw1, w2, lw2を含む詳細出力
"""

import numpy as np
from murayama_calculator_revised import MurayamaCalculatorRevised

def test_comprehensive_comparison():
    """包括的な比較テスト"""
    
    print("=== Excel実装とPython実装の包括的比較 ===\n")
    
    # テストケース1: 元のExcelファイルのパラメータ
    print("【テストケース1】元のExcelファイル（村山式_分析用.xlsx）")
    print("-" * 80)
    params1 = {
        'H': 9.9,
        'gamma': 25.5,
        'c': 253,
        'phi_deg': 21,
        'H_f': 5.2,
        'alpha': 1.8,
        'K': 1.0,
        'theta_d_deg': 75
    }
    
    excel1 = {
        'B': 4.475692098691149,
        'r0': 4.045471892076639,
        'rd': 6.686396245146749,
        'la': -0.6989187243037986,
        'lp': 4.049767466906651,
        'q': -239.0930847591986,
        'Wf': 434.29622896358677,
        'lw': 1.136070940712082,
        'P': -2434.7018976765366,
        # 詳細値（Excel計算から）
        'w1': 296.7383861432232,
        'lw1': 0.7929786419265843,
        'w2': 137.55784282036365,
        'lw2': 1.876186174801123  # Excel逆算値
    }
    
    test_case(params1, excel1, "θ_d = 75°")
    
    # テストケース2: 新しいExcelファイルのパラメータ
    print("\n【テストケース2】新Excelファイル（村山式_分析用_v2.xlsx）")
    print("-" * 80)
    params2 = {
        'H': 50,
        'gamma': 20,
        'c': 20,
        'phi_deg': 30,
        'H_f': 10,
        'alpha': 1.8,
        'K': 1.0,
        'theta_d_deg': 60
    }
    
    excel2 = {
        'B': 6.508926968399547,
        'r0': 7.515861474682187,
        'rd': 13.757930737341093,
        'la': 8.427753792796626e-16,
        'lp': 8.757930737341093,
        'q': 167.06849770684155,
        'Wf': 905.4156825829673,
        'lw': 2.6161525827276515,
        'P': 322.93447293062375,
        # 詳細値
        'w1': 650.8926968399547,
        'lw1': 2.16964232279985,
        'w2': 254.52298574301267,
        'lw2': 3.758015139473548
    }
    
    test_case(params2, excel2, "θ_d = 60°")
    
    # 複数角度でのテスト
    print("\n【テストケース3】複数角度での比較（新Excelパラメータ）")
    print("-" * 80)
    test_multiple_angles(params2)

def test_case(params, excel_values, case_name):
    """個別テストケースの実行"""
    print(f"\nケース: {case_name}")
    print(f"パラメータ: H={params['H']}, γ={params['gamma']}, c={params['c']}, φ={params['phi_deg']}°, H_f={params['H_f']}")
    
    # 計算機インスタンス（Excel互換モード）
    calculator = MurayamaCalculatorRevised(
        H_f=params['H_f'],
        gamma=params['gamma'],
        phi=params['phi_deg'],
        coh=params['c'],
        H=params['H'],
        alpha=params['alpha'],
        K=params['K'],
        force_finite_cover=True,
        excel_compatible_lw2=True  # Excel互換モードを使用
    )
    
    # 計算実行
    theta_d_rad = np.radians(params['theta_d_deg'])
    result = calculator.calculate_support_pressure(theta_d_rad)
    
    # 結果の表示
    print("\n【幾何パラメータ】")
    print(f"{'項目':<10} {'Python':>15} {'Excel':>15} {'差':>15} {'相対誤差':>10}")
    print("-" * 70)
    
    compare_value("B", result['geometry']['B'], excel_values['B'])
    compare_value("r0", result['geometry']['r0'], excel_values['r0'])
    compare_value("rd", result['geometry']['rd'], excel_values['rd'])
    compare_value("la", result['geometry']['la'], excel_values['la'])
    compare_value("lp", result['geometry']['lp'], excel_values['lp'])
    
    print("\n【荷重パラメータ】")
    print(f"{'項目':<10} {'Python':>15} {'Excel':>15} {'差':>15} {'相対誤差':>10}")
    print("-" * 70)
    
    compare_value("q", result['q'], excel_values['q'])
    compare_value("Wf", result['Wf'], excel_values['Wf'])
    
    print("\n【重心計算詳細】")
    print(f"{'項目':<10} {'Python':>15} {'Excel':>15} {'差':>15} {'相対誤差':>10}")
    print("-" * 70)
    
    compare_value("w1", result['w1'], excel_values['w1'])
    compare_value("lw1", result['lw1'], excel_values['lw1'])
    compare_value("w2", result['w2'], excel_values['w2'])
    compare_value("lw2", result['lw2'], excel_values['lw2'])
    compare_value("lw", result['lw'], excel_values['lw'])
    
    print("\n【最終結果】")
    print(f"{'項目':<10} {'Python':>15} {'Excel':>15} {'差':>15} {'相対誤差':>10}")
    print("-" * 70)
    
    compare_value("P", result['P'], excel_values['P'])
    
    # lw計算の検証
    print("\n【lw計算の検証】")
    lw_calc = (result['w1'] * result['lw1'] + result['w2'] * result['lw2']) / (result['w1'] + result['w2'])
    print(f"(w1*lw1 + w2*lw2)/(w1+w2) = {lw_calc:.10f}")
    print(f"計算されたlw = {result['lw']:.10f}")
    print(f"差 = {abs(lw_calc - result['lw']):.2e}")

def compare_value(name, python_val, excel_val):
    """値の比較と表示"""
    diff = abs(python_val - excel_val)
    if abs(excel_val) > 1e-10:
        rel_error = diff / abs(excel_val) * 100
        print(f"{name:<10} {python_val:>15.8f} {excel_val:>15.8f} {diff:>15.2e} {rel_error:>9.2f}%")
    else:
        print(f"{name:<10} {python_val:>15.8f} {excel_val:>15.8f} {diff:>15.2e} {'N/A':>10}")

def test_multiple_angles(params):
    """複数角度でのテスト"""
    print("\n角度別比較（θ_d = 50°～70°）")
    print(f"{'θ_d[°]':>8} {'B':>12} {'q':>12} {'w1':>12} {'lw1':>12} {'w2':>12} {'lw2':>12} {'lw':>12} {'P':>12}")
    print("-" * 120)
    
    calculator = MurayamaCalculatorRevised(
        H_f=params['H_f'],
        gamma=params['gamma'],
        phi=params['phi_deg'],
        coh=params['c'],
        H=params['H'],
        alpha=params['alpha'],
        K=params['K'],
        force_finite_cover=True,
        excel_compatible_lw2=True  # Excel互換モードを使用
    )
    
    for theta_deg in range(50, 71, 5):
        theta_rad = np.radians(theta_deg)
        result = calculator.calculate_support_pressure(theta_rad)
        
        print(f"{theta_deg:>8} {result['geometry']['B']:>12.6f} {result['q']:>12.4f} "
              f"{result['w1']:>12.4f} {result['lw1']:>12.6f} {result['w2']:>12.4f} "
              f"{result['lw2']:>12.6f} {result['lw']:>12.6f} {result['P']:>12.4f}")

if __name__ == "__main__":
    test_comprehensive_comparison()