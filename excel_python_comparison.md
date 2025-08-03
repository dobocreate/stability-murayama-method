# Excel実装とPython実装の比較分析

## 主要な相違点

### 1. **影響幅係数 (B')の計算**

**Excel実装:**
```excel
W9: =1.8*C9
```
- 影響幅係数を固定値1.8でB値に乗じている

**Python実装:**
```python
self.alpha = alpha  # デフォルト: 1.8
```
- 影響幅係数αは可変パラメータとして実装されている（デフォルト1.8）

### 2. **等価合力q計算の土被り判定**

**Excel実装:**
```excel
H9: =(0.9*C9*($D$3-$D$4/0.9/C9)/(TAN($D$5*PI()/180)))*(1-EXP(-$D$2/0.9/C9*TAN($D$5*PI()/180)))
```
- 係数0.9を使用（B'ではなくB×0.9）
- 土被りH（$D$2 = 9.9m）の値を直接使用

**Python実装:**
```python
# 深部条件の判定（土被りが幅の1.5倍以上）
is_deep = (self.H is None) or (self.H > 1.5 * B)

if is_deep:
    # 深部前提（角括弧→1）
    q = (self.alpha * B * (self.gamma - 2 * self.coh / (self.alpha * B))) / (2 * self.K * np.tan(self.phi))
else:
    # 有限土被り（指数の"中"に tanφ を掛ける）
    fac = 1.0 - np.exp(-2.0 * self.K * self.H * np.tan(self.phi) / (self.alpha * B))
    q = (self.alpha * B * (self.gamma - 2 * self.coh / (self.alpha * B))) / (2 * self.K * np.tan(self.phi)) * fac
```
- 深部/有限土被りの条件分岐がある
- 係数はα（デフォルト1.8）とK（デフォルト1.0）を使用

### 3. **重心位置計算（lw）**

**Excel実装:**
```excel
J9: =(L9*K9+M9*N9)/(L9+N9)
K9: =F9+C9/3  # lw1
M9: =S9*COS(($D$5+T9)*PI()/180)+(2/3*(U9/(1-COS(V9*PI()/180)))*((1-(COS(V9*PI()/180))^2)/(V9*PI()/180-2*(SIN(V9*PI()/180))*(COS(V9*PI()/180))/2))*SIN(V9*PI()/180)-((U9*COS(V9*PI()/180))/(1-COS(V9*PI()/180))))*COS(ATAN(C9/$D$6))  # lw2
```
- 複雑な幾何学的計算式を使用

**Python実装:**
```python
# 三角形部分
lw1 = la + B / 3  # フェイス基準（la オフセット含む）

# 曲線領域の重心計算（S, T, U を用いた厳密式）
lw2 = S*np.cos(self.phi + T) + (2.0/3.0)*U*np.cos(np.arctan2(B, self.H_f))
```
- Excel式の簡略化された形式を使用

### 4. **支保圧P計算式**

**Excel実装:**
```excel
X9: =(I9*J9+H9*C9*(F9+C9/2)-($D$4*(E9^2-D9^2)/(2*TAN($D$5*PI()/180))))/G9
```
- 粘着抵抗モーメントの係数が1/2

**Python実装:**
```python
# 粘着抵抗モーメント
Mc = self.calculate_cohesion_moment(r0, rd)
# Mc = self.coh * (rd**2 - r0**2) / (2 * np.tan(self.phi))

# 支保圧の算定（モーメント釣合い）
numerator = Wf * lw + q * B * (la + B/2) - Mc
P = numerator / lp
```
- 粘着抵抗モーメントが分離されて計算されている

### 5. **経験係数Kの扱い**

**Excel実装:**
- 明示的なK係数は見当たらない（暗黙的に1.0を使用？）

**Python実装:**
```python
K: float = 1.0  # 経験係数（標準: 1.0, Terzaghi実験では1～1.5）
```
- パラメータとして明示的に実装

## 実装の差異による影響

1. **係数の違い**: Excelでは0.9、Pythonではα（1.8）を使用しているため、等価合力qの値が大きく異なる可能性がある

2. **土被り判定**: Pythonは深部/有限土被りを自動判定するが、Excelは常に有限土被り式を使用

3. **パラメータの柔軟性**: Python実装はα、Kをパラメータ化しているため、より柔軟な解析が可能

4. **数値精度**: Python実装は各種数値安定性のチェック（ゼロ除算回避など）が組み込まれている

## 推奨事項

Excel実装の計算ロジックに完全に合わせる場合は、以下の修正が必要：
1. 等価合力qの計算で係数0.9を使用
2. 深部/有限土被りの条件分岐を削除し、常に有限土被り式を使用
3. 経験係数Kの明示的な使用を確認