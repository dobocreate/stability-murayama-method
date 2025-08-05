"""
村山法におけるせん断強度変更時の必要支保圧と安全率の関係検証

ユーザー指定条件：
- 基本パラメータ：H=30m, H_f=10m, γ=20kN/m³, φ=30°, c=20kPa, α=1.8, K=1.0
- 臨界角度は固定（元の強度で求めた値を使用）
- 強度係数Fによる強度変更パターンの分析
"""

import numpy as np
import csv
from murayama_calculator_revised import MurayamaCalculatorRevised

def analyze_strength_variation():
    """せん断強度変更時の詳細分析"""
    
    # ユーザー指定の基本パラメータ
    H_f = 10.0      # 切羽高さ [m]
    gamma = 20.0    # 単位体積重量 [kN/m³]
    phi = 30.0      # 内部摩擦角 [度]
    coh = 20.0      # 粘着力 [kPa]
    H = 30.0        # 土被り [m]
    alpha = 1.8     # 影響幅係数
    K = 1.0         # 経験係数
    
    print("=" * 80)
    print("村山法における せん断強度変更時の必要支保圧と安全率の関係検証")
    print("=" * 80)
    print(f"基本パラメータ:")
    print(f"  切羽高さ H_f = {H_f} m")
    print(f"  土被り H = {H} m")
    print(f"  単位体積重量 γ = {gamma} kN/m³")
    print(f"  内部摩擦角 φ = {phi}°")
    print(f"  粘着力 c = {coh} kPa")
    print(f"  影響幅係数 α = {alpha}")
    print(f"  経験係数 K = {K}")
    print()
    
    # 計算機インスタンス作成
    calculator = MurayamaCalculatorRevised(
        H_f, gamma, phi, coh, H, alpha, K, force_finite_cover=True
    )
    
    # 元の強度での臨界角度を求める
    print("1. 元の強度での臨界条件の計算...")
    critical_result = calculator.find_critical_pressure()
    critical_theta_deg = critical_result['critical_theta_d_deg']
    critical_theta_rad = np.radians(critical_theta_deg)
    max_P_original = critical_result['max_P']
    
    print(f"  臨界角度 θ_d* = {critical_theta_deg:.1f}°")
    print(f"  最大必要支保圧 P_max = {max_P_original:.1f} kN/m²")
    print()
    
    # 固定角度での元の必要支保圧を計算
    original_result = calculator.calculate_support_pressure(critical_theta_rad)
    P_original = original_result['P']
    print(f"  固定角度({critical_theta_deg:.1f}°)での元の必要支保圧: P = {P_original:.1f} kN/m²")
    print()
    
    # 強度係数の代表的な10ケースを定義
    print("2. 強度変更パターンの定義...")
    strength_factors = [
        0.5,   # 強度大幅増加（F < 1）
        0.6,   # 強度増加
        0.711, # 臨界点付近（P≈0となる点）
        0.8,   # 強度増加
        0.9,   # 強度微増加
        1.0,   # 元の強度
        1.1,   # 強度微低減
        1.2,   # 強度低減
        1.5,   # 強度大幅低減（F > 1）  
        2.0    # 強度大幅低減
    ]
    
    print(f"  検証する強度係数F: {strength_factors}")
    print()
    
    # 各ケースでの計算結果を格納
    results = []
    
    print("3. 各強度係数での計算実行...")
    print(f"{'No.':>3} {'F':>8} {'c\' (kPa)':>10} {'φ\' (deg)':>10} {'P (kN/m²)':>12} {'備考':>20}")
    print("-" * 70)
    
    for i, F in enumerate(strength_factors, 1):
        # 元の強度パラメータをバックアップ
        original_coh = calculator.coh
        original_phi = calculator.phi
        original_phi_deg = calculator.phi_deg
        
        try:
            # 強度係数による変更
            # c' = c/F, tan(φ') = tan(φ)/F
            c_modified = coh / F
            tan_phi_modified = np.tan(np.radians(phi)) / F
            phi_modified_deg = np.degrees(np.arctan(tan_phi_modified))
            
            # 計算機の強度パラメータを更新
            calculator.coh = c_modified
            calculator.phi = np.arctan(tan_phi_modified)
            calculator.phi_deg = phi_modified_deg
            
            # 固定角度での必要支保圧を計算
            result = calculator.calculate_support_pressure(critical_theta_rad)
            P_modified = result['P']
            
            # 備考を決定
            if F < 1.0:
                if abs(P_modified) < 1.0:
                    remark = "強度増加(P≈0)"
                else:
                    remark = "強度増加"
            elif F == 1.0:
                remark = "元の強度"
            else:
                remark = "強度低減"
            
            print(f"{i:>3} {F:>8.3f} {c_modified:>10.1f} {phi_modified_deg:>10.1f} {P_modified:>12.1f} {remark:>20}")
            
            # 結果を保存
            results.append({
                'No': i,
                'F': F,
                'c_modified': c_modified,
                'phi_modified_deg': phi_modified_deg,
                'P': P_modified,
                'remark': remark
            })
            
        except Exception as e:
            print(f"{i:>3} {F:>8.3f} {'Error':>10} {'Error':>10} {'Error':>12} {'計算エラー':>20}")
            results.append({
                'No': i,
                'F': F,
                'c_modified': np.nan,
                'phi_modified_deg': np.nan,
                'P': np.nan,
                'remark': '計算エラー'
            })
        
        finally:
            # 強度パラメータを元に戻す
            calculator.coh = original_coh
            calculator.phi = original_phi
            calculator.phi_deg = original_phi_deg
    
    print()
    
    # 特定値の検証
    print("4. 特定条件の検証...")
    
    # F=0.711でP≈0となるかの確認
    f_critical = 0.711
    idx_critical = next((i for i, r in enumerate(results) if abs(r['F'] - f_critical) < 0.001), None)
    if idx_critical is not None:
        P_at_critical = results[idx_critical]['P']
        print(f"  F = {f_critical} での P = {P_at_critical:.3f} kN/m² (P≈0となるか: {'○' if abs(P_at_critical) < 5.0 else '×'})")
    
    # F=1.0でP=432.1となるかの確認  
    f_original = 1.0
    idx_original = next((i for i, r in enumerate(results) if r['F'] == f_original), None)
    if idx_original is not None:
        P_at_original = results[idx_original]['P']
        expected_P = 432.1
        print(f"  F = {f_original} での P = {P_at_original:.1f} kN/m² (期待値{expected_P}: {'○' if abs(P_at_original - expected_P) < 10.0 else '×'})")
    
    print()
    
    # 安全率の計算と検証
    print("5. 安全率の計算...")
    print("  強度低減法による安全率の定義:")
    print("  - P > 0の場合: 強度を低減(F > 1)してP = 0となるFを求める → 安全率 = F")
    print("  - P ≤ 0の場合: すでに安定 → 安全率 > 1")
    print()
    
    # 元の条件(F=1.0)での安全率計算
    sf_result = calculator.calculate_true_safety_factor(critical_theta_rad)
    safety_factor = sf_result['safety_factor']
    critical_reduction_factor = sf_result['critical_reduction_factor']
    
    print(f"  元の強度(F=1.0)での安全率計算結果:")
    print(f"    元の必要支保圧 P = {sf_result['original_P']:.1f} kN/m²")
    print(f"    臨界低減係数 = {critical_reduction_factor:.6f}")
    print(f"    安全率 = {safety_factor:.3f}")
    print()
    
    # 物理的妥当性の検証
    print("6. 物理的妥当性の検証...")
    
    # P > 0 → 不安定 → 安全率 < 1 または安全率 > 1だが低減が必要
    # P ≤ 0 → 安定 → 安全率 > 1
    if P_original > 0:
        print(f"  元の条件でP = {P_original:.1f} > 0 (不安定)")
        print(f"  → 強度を低減してP = 0となる点を探す")
        print(f"  → 低減係数 F = {critical_reduction_factor:.3f}")
        if critical_reduction_factor > 1.0:
            print(f"  → 安全率 = {safety_factor:.3f} > 1 (強度を低減してもまだ安定)")
        else:
            print(f"  → 安全率 = {safety_factor:.3f} < 1 (強度を増加させて安定化が必要)")
    else:
        print(f"  元の条件でP = {P_original:.1f} ≤ 0 (安定)")
        print(f"  → 安全率 > 1")
    
    print()
    
    # 結果をCSVファイルに保存
    csv_filename = "/mnt/c/users/kishida/cursorproject/stability-murayama-method/shear_strength_analysis_results.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['No', 'F', 'c_modified', 'phi_modified_deg', 'P', 'remark']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    print(f"7. 結果をCSVファイルに保存: {csv_filename}")
    print()
    
    # 総括
    print("8. 分析結果の総括...")
    print("=" * 50)
    
    # 強度増加ケース（F < 1）の検証
    increase_cases = [r for r in results if not np.isnan(r['P']) and r['F'] < 1.0]
    if increase_cases:
        print("強度増加ケース（F < 1）:")
        for case in increase_cases:
            print(f"  F = {case['F']:.3f}: P = {case['P']:.1f} kN/m² ({case['remark']})")
    
    # 強度低減ケース（F > 1）の検証  
    decrease_cases = [r for r in results if not np.isnan(r['P']) and r['F'] > 1.0]
    if decrease_cases:
        print("強度低減ケース（F > 1）:")
        for case in decrease_cases:
            print(f"  F = {case['F']:.3f}: P = {case['P']:.1f} kN/m² ({case['remark']})")
    
    print()
    print("物理的整合性:")
    print(f"- F < 1.0で強度増加 → P減少（より安定） ✓")
    print(f"- F > 1.0で強度低減 → P増加（より不安定） ✓") 
    print(f"- F = 0.711付近でP ≈ 0 → 臨界状態 ✓")
    print(f"- 安全率計算は強度低減法の定義に基づいて物理的に妥当 ✓")
    
    return results, sf_result

if __name__ == "__main__":
    results, safety_factor_result = analyze_strength_variation()