"""
W値の差異分析
"""

import numpy as np

def analyze_w_difference():
    """W値の差異を分析"""
    
    # Excel値
    Wf = 905.41568258
    w1 = 650.89269684
    w2 = 254.52298574
    W_calc_from_P = 607.4753393742527
    
    print("=== W値の差異分析 ===\n")
    
    print(f"Excel値:")
    print(f"  Wf = {Wf}")
    print(f"  w1 = {w1}")
    print(f"  w2 = {w2}")
    print(f"  w1 + w2 = {w1 + w2}")
    
    print(f"\n確認:")
    print(f"  Wf = w1 + w2 ? {Wf} = {w1 + w2} ? {abs(Wf - (w1 + w2)) < 0.01}")
    
    print(f"\nP値から逆算したW:")
    print(f"  W = {W_calc_from_P}")
    print(f"  差 = {Wf} - {W_calc_from_P} = {Wf - W_calc_from_P}")
    
    # 比率を確認
    ratio = W_calc_from_P / Wf
    print(f"\n比率:")
    print(f"  W_逆算 / Wf = {W_calc_from_P} / {Wf} = {ratio}")
    
    # w1とw2の比率も確認
    print(f"\n各成分との比較:")
    print(f"  W_逆算 / w1 = {W_calc_from_P} / {w1} = {W_calc_from_P / w1}")
    print(f"  W_逆算 / w2 = {W_calc_from_P} / {w2} = {W_calc_from_P / w2}")
    
    # もしかして、w1だけ？w2だけ？
    print(f"\n可能性:")
    print(f"  もしW = w1なら: P計算でのW = {w1}")
    print(f"  もしW = w2なら: P計算でのW = {w2}")
    
    # w1とw2に係数をかけた場合
    factor1 = W_calc_from_P / w1
    factor2 = W_calc_from_P / w2
    print(f"\n係数の可能性:")
    print(f"  W = {factor1:.4f} * w1")
    print(f"  W = {factor2:.4f} * w2")
    
    # 別の解釈：γの違い？
    gamma = 20  # kN/m³
    print(f"\n単位の問題？")
    print(f"  γ = {gamma} kN/m³")
    
    # H_fの違い？
    H_f = 10
    B = 6.508926968399547
    
    # 三角形部分の体積
    V_triangle = H_f * B / 2
    print(f"\n三角形部分:")
    print(f"  体積 = H_f * B / 2 = {H_f} * {B} / 2 = {V_triangle}")
    print(f"  重量 = γ * 体積 = {gamma} * {V_triangle} = {gamma * V_triangle}")
    print(f"  計算されたw1 = {w1}")

if __name__ == "__main__":
    analyze_w_difference()