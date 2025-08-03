"""
Excel M9式の第2項のデバッグ
"""

import numpy as np

# パラメータ（θ_d = 60°）
phi_deg = 30
B = 6.508926968399547
H_f = 10
V_deg = 28.122492057242425
U = 1.4942323635855088

print("=== Excel M9式の第2項デバッグ ===\n")

# ラジアンに変換
V_rad = np.radians(V_deg)

# 各要素の計算
cos_V = np.cos(V_rad)
sin_V = np.sin(V_rad)

print(f"V = {V_deg}° = {V_rad} rad")
print(f"cos(V) = {cos_V}")
print(f"sin(V) = {sin_V}")
print(f"1 - cos(V) = {1 - cos_V}")

# A = U/(1-cos(V))
A = U / (1 - cos_V)
print(f"\nA = U/(1-cos(V)) = {U}/(1-{cos_V}) = {A}")

# B項の計算
B_num = 1 - cos_V**2
B_den = V_rad - sin_V * cos_V
B_frac = B_num / B_den
print(f"\nB項の計算:")
print(f"分子 = 1 - cos²(V) = {B_num}")
print(f"分母 = V - sin(V)*cos(V) = {V_rad} - {sin_V}*{cos_V} = {B_den}")
print(f"B = {B_frac}")

# C = sin(V)
C = sin_V
print(f"\nC = sin(V) = {C}")

# D = U*cos(V)/(1-cos(V))
D = U * cos_V / (1 - cos_V)
print(f"\nD = U*cos(V)/(1-cos(V)) = {U}*{cos_V}/(1-{cos_V}) = {D}")

# cos(arctan(B/H_f))
atan_val = np.arctan(B/H_f)
cos_atan = np.cos(atan_val)
print(f"\narctan(B/H_f) = arctan({B}/{H_f}) = {atan_val}")
print(f"cos(arctan(B/H_f)) = {cos_atan}")

# 第2項の計算
print(f"\n第2項の内部計算:")
print(f"A * B * C = {A} * {B_frac} * {C} = {A * B_frac * C}")
print(f"A * B * C - D = {A * B_frac * C} - {D} = {A * B_frac * C - D}")

term2_inner = A * B_frac * C - D
term2 = (2/3) * term2_inner * cos_atan
print(f"\n第2項 = (2/3) * {term2_inner} * {cos_atan}")
print(f"      = {term2}")

# 最終的なlw2
S = 9.343066058315848
term1 = S * np.cos(np.radians(phi_deg + 39.614839509609574))
lw2_calc = term1 + term2

print(f"\n最終結果:")
print(f"第1項 = {term1}")
print(f"第2項 = {term2}")
print(f"lw2 = {lw2_calc}")
print(f"\nExcel lw2 = 3.758015139473548")
print(f"差 = {abs(lw2_calc - 3.758015139473548)}")

# デバッグ: Excel式の別の解釈
print("\n=== デバッグ: 式の分母の確認 ===")
# Excel式: V9*PI()/180-2*(SIN(V9*PI()/180))*(COS(V9*PI()/180))/2
# = V_rad - 2*sin(V)*cos(V)/2
# = V_rad - sin(V)*cos(V)
print(f"V_rad = {V_rad}")
print(f"sin(V)*cos(V) = {sin_V * cos_V}")
print(f"V_rad - sin(V)*cos(V) = {B_den}")

# 2*sin*cos/2 の部分の確認
print(f"\n2*sin(V)*cos(V)/2 = {2 * sin_V * cos_V / 2}")
print(f"これは sin(V)*cos(V) = {sin_V * cos_V} と同じ")