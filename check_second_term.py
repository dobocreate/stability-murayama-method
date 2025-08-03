"""
ExcelのP計算式の第2項の確認
"""

def check_second_term():
    """第2項の確認"""
    
    # テストケース2のExcel値
    q = 167.06849770684155
    B = 6.508926968399547
    la = 8.427753792796626e-16  # ≈ 0
    
    print("=== ExcelのP計算式の第2項の確認 ===\n")
    
    print("Excel式: P = (W・lw + q・B(la+B/2) - (c(rc^2-r0^2))/2tanφ) / lp")
    print("\n第2項: q・B(la+B/2)")
    
    print(f"\n値:")
    print(f"  q = {q}")
    print(f"  B = {B}")
    print(f"  la = {la} ≈ 0")
    
    print(f"\n計算:")
    print(f"  la + B/2 = {la} + {B}/2 = {la + B/2}")
    print(f"  q・B = {q} × {B} = {q * B}")
    print(f"  q・B・(la+B/2) = {q * B} × {la + B/2} = {q * B * (la + B/2)}")
    
    # 別の解釈の可能性
    print(f"\n\n別の解釈の可能性:")
    
    # 1. q・B・la + B/2 （括弧の位置が違う？）
    alt1 = q * B * la + B/2
    print(f"1. q・B・la + B/2 = {q * B * la} + {B/2} = {alt1}")
    
    # 2. q・(B・la + B/2) （Bが括弧内？）
    alt2 = q * (B * la + B/2)
    print(f"2. q・(B・la + B/2) = {q} × ({B * la} + {B/2}) = {alt2}")
    
    # 3. q・B・(la + B)/2 （全体を2で割る？）
    alt3 = q * B * (la + B) / 2
    print(f"3. q・B・(la + B)/2 = {q * B} × ({la} + {B})/2 = {alt3}")
    
    # 標準的な解釈
    standard = q * B * (la + B/2)
    print(f"\n標準的な解釈: q・B・(la+B/2) = {standard}")

if __name__ == "__main__":
    check_second_term()