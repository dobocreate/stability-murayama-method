"""
計算フローの詳細を可視化するためのスクリプト
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Arc
import matplotlib.font_manager as fm

# 日本語フォントの設定
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def create_calculation_flow_diagram():
    """計算フローの詳細図を作成"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 10))
    
    # 左側：概念図
    ax1.set_xlim(-2, 6)
    ax1.set_ylim(-1, 6)
    ax1.set_aspect('equal')
    ax1.set_title('Logarithmic Spiral Slip Surface', fontsize=14, fontweight='bold')
    
    # 座標軸
    ax1.axhline(y=0, color='k', linewidth=0.5)
    ax1.axvline(x=0, color='k', linewidth=0.5)
    
    # トンネル断面
    tunnel = patches.Rectangle((0, 0), 1, 3, linewidth=2, 
                              edgecolor='black', facecolor='white')
    ax1.add_patch(tunnel)
    ax1.text(0.5, 1.5, 'Tunnel\nFace', ha='center', va='center')
    
    # 対数らせん滑り面
    phi = np.radians(30)
    theta = np.linspace(0, np.radians(60), 100)
    r0 = 1.5
    r = r0 * np.exp(theta * np.tan(phi))
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    ax1.plot(x, y, 'r-', linewidth=2, label='Slip surface')
    ax1.fill_between(x, 0, y, alpha=0.3, color='brown', label='Sliding mass')
    
    # 力の表示
    # 重量
    ax1.arrow(2, 2, 0, -0.8, head_width=0.1, head_length=0.1, 
              fc='blue', ec='blue', linewidth=2)
    ax1.text(2.2, 1.5, 'W', fontsize=12, color='blue')
    
    # 支保圧
    ax1.arrow(0.2, 0.5, 0.3, 0, head_width=0.1, head_length=0.05, 
              fc='green', ec='green', linewidth=2)
    ax1.text(0.35, 0.7, 'P', fontsize=12, color='green')
    
    # せん断抵抗
    arc = Arc((0, 0), 3, 3, angle=0, theta1=0, theta2=60, 
              color='orange', linewidth=2)
    ax1.add_patch(arc)
    ax1.text(2.5, 1, 'τ', fontsize=12, color='orange')
    
    # 寸法線
    ax1.plot([0, 0], [0, 3], 'k-', linewidth=0.5)
    ax1.plot([-0.1, 0.1], [0, 0], 'k-', linewidth=1)
    ax1.plot([-0.1, 0.1], [3, 3], 'k-', linewidth=1)
    ax1.text(-0.3, 1.5, 'H', fontsize=12, va='center')
    
    ax1.set_xlabel('x [m]')
    ax1.set_ylabel('y [m]')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 右側：計算フロー
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 12)
    ax2.axis('off')
    ax2.set_title('Calculation Flow', fontsize=14, fontweight='bold')
    
    # フローチャートのボックス
    boxes = [
        (5, 11, 'Input Parameters\nH, γ, φ, c, q', 'lightblue'),
        (5, 9.5, 'Set Analysis Range\nr₀: [r₀_min, r₀_max]\nθ: [θ_min, θ_max]', 'lightgreen'),
        (5, 8, 'For each (r₀, θ)', 'yellow'),
        (2.5, 6.5, 'Calculate Area\nA = ∫(1/2)r²dθ', 'lightyellow'),
        (7.5, 6.5, 'Calculate Centroid\nx̄ = (1/A)∫r³cosθdθ', 'lightyellow'),
        (2.5, 5, 'Weight Moment\nM_W = γ·A·x̄', 'lightcoral'),
        (5, 5, 'Surcharge Moment\nM_Q = q·b_q·x_q', 'lightcoral'),
        (7.5, 5, 'Resistance Moment\nM_τ = ∫c·r·ds', 'lightcoral'),
        (5, 3.5, 'Equilibrium\nM_W + M_Q = M_τ + M_P', 'lightgray'),
        (5, 2, 'Support Pressure\nP = 2(M_W+M_Q-M_τ)/H²', 'lightblue'),
        (5, 0.5, 'Find Maximum P\nP_max = max(P)', 'salmon')
    ]
    
    for x, y, text, color in boxes:
        box = FancyBboxPatch((x-1.2, y-0.4), 2.4, 0.8,
                            boxstyle="round,pad=0.1",
                            facecolor=color, edgecolor='black')
        ax2.add_patch(box)
        ax2.text(x, y, text, ha='center', va='center', fontsize=10)
    
    # 矢印
    arrows = [
        (5, 10.7, 5, 9.9),      # Input -> Range
        (5, 9.1, 5, 8.4),       # Range -> Loop
        (5, 7.6, 2.5, 6.9),     # Loop -> Area
        (5, 7.6, 7.5, 6.9),     # Loop -> Centroid
        (2.5, 6.1, 2.5, 5.4),   # Area -> M_W
        (7.5, 6.1, 7.5, 5.4),   # Centroid -> M_τ
        (2.5, 4.6, 4.2, 3.8),   # M_W -> Equilibrium
        (5, 4.6, 5, 3.9),       # M_Q -> Equilibrium
        (7.5, 4.6, 5.8, 3.8),   # M_τ -> Equilibrium
        (5, 3.1, 5, 2.4),       # Equilibrium -> P
        (5, 1.6, 5, 0.9)        # P -> P_max
    ]
    
    for x1, y1, x2, y2 in arrows:
        ax2.arrow(x1, y1, x2-x1, y2-y1, head_width=0.15, head_length=0.1,
                 fc='black', ec='black')
    
    # ループの矢印
    ax2.annotate('', xy=(3, 7.5), xytext=(3, 4),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='blue'))
    ax2.annotate('', xy=(3, 4), xytext=(1, 4),
                arrowprops=dict(arrowstyle='-', lw=1.5, color='blue'))
    ax2.annotate('', xy=(1, 4), xytext=(1, 7.5),
                arrowprops=dict(arrowstyle='-', lw=1.5, color='blue'))
    ax2.annotate('', xy=(1, 7.5), xytext=(3, 7.5),
                arrowprops=dict(arrowstyle='-', lw=1.5, color='blue'))
    ax2.text(0.5, 5.75, 'Loop', fontsize=10, color='blue', rotation=90, va='center')
    
    plt.tight_layout()
    return fig

def create_moment_distribution_diagram():
    """モーメント分布の概念図を作成"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    # パラメータ設定
    r0_values = np.linspace(0.5, 5, 20)
    theta_values = np.linspace(10, 60, 20)
    
    # 仮想的なモーメント分布
    R0, THETA = np.meshgrid(r0_values, theta_values)
    P = 50 + 30*np.sin(R0/2) * np.cos(np.radians(THETA))
    
    # コンター図
    contour = ax.contourf(R0, THETA, P, levels=20, cmap='RdYlBu_r')
    ax.contour(R0, THETA, P, levels=10, colors='black', alpha=0.3, linewidths=0.5)
    
    # 最大値の位置
    max_idx = np.unravel_index(P.argmax(), P.shape)
    ax.plot(R0[max_idx], THETA[max_idx], 'rx', markersize=15, markeredgewidth=3)
    ax.text(R0[max_idx]+0.2, THETA[max_idx], 'Critical\nCondition', 
            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))
    
    # カラーバー
    cbar = plt.colorbar(contour, ax=ax)
    cbar.set_label('Required Support Pressure P [kN/m²]', fontsize=12)
    
    ax.set_xlabel('Initial Radius r₀ [m]', fontsize=12)
    ax.set_ylabel('Angle θ [degrees]', fontsize=12)
    ax.set_title('Parametric Study Results - Support Pressure Distribution', 
                 fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    return fig

def create_force_equilibrium_diagram():
    """力とモーメントのつり合い図"""
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    
    ax.set_xlim(-3, 5)
    ax.set_ylim(-2, 5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title('Force and Moment Equilibrium', fontsize=14, fontweight='bold')
    
    # 回転中心
    ax.plot(0, 0, 'ko', markersize=10)
    ax.text(0.1, -0.3, 'O', fontsize=12)
    
    # 滑り土塊（簡略化）
    vertices = [(0, 0), (3, 0), (4, 2), (2, 3), (0, 0)]
    polygon = patches.Polygon(vertices, facecolor='brown', alpha=0.3, 
                             edgecolor='black', linewidth=2)
    ax.add_patch(polygon)
    
    # 重心
    cx, cy = 2, 1.5
    ax.plot(cx, cy, 'bo', markersize=8)
    ax.text(cx+0.1, cy+0.1, 'G', fontsize=10)
    
    # 力ベクトル
    # 重量
    ax.arrow(cx, cy, 0, -1.2, head_width=0.15, head_length=0.1,
             fc='blue', ec='blue', linewidth=2)
    ax.text(cx+0.2, cy-0.6, 'W = γ·A', fontsize=11, color='blue')
    
    # モーメントアーム
    ax.plot([0, cx], [0, cy], 'k--', alpha=0.5)
    ax.text(1, 0.8, 'x̄', fontsize=11)
    
    # 支保圧
    for i in range(3):
        y = i * 0.8 + 0.3
        ax.arrow(-0.5, y, 0.4, 0, head_width=0.08, head_length=0.05,
                fc='green', ec='green', linewidth=1.5)
    ax.text(-0.8, 1.5, 'P', fontsize=11, color='green')
    
    # モーメントの表示
    ax.text(-2, 4, 'Moment Equilibrium:', fontsize=12, fontweight='bold')
    ax.text(-2, 3.5, 'ΣM_O = 0', fontsize=11)
    ax.text(-2, 3, 'M_W + M_Q = M_τ + M_P', fontsize=11)
    ax.text(-2, 2.5, 'Where:', fontsize=10)
    ax.text(-2, 2.2, '  M_W: Weight moment', fontsize=9)
    ax.text(-2, 1.9, '  M_Q: Surcharge moment', fontsize=9)
    ax.text(-2, 1.6, '  M_τ: Shear resistance moment', fontsize=9)
    ax.text(-2, 1.3, '  M_P: Support pressure moment', fontsize=9)
    
    # 寸法
    ax.plot([3.5, 3.5], [0, 3], 'k-', linewidth=0.5)
    ax.plot([3.4, 3.6], [0, 0], 'k-', linewidth=1)
    ax.plot([3.4, 3.6], [3, 3], 'k-', linewidth=1)
    ax.text(3.7, 1.5, 'H', fontsize=11)
    
    return fig

if __name__ == "__main__":
    # 図の生成と保存
    fig1 = create_calculation_flow_diagram()
    fig1.savefig('calculation_flow_diagram.png', dpi=300, bbox_inches='tight')
    
    fig2 = create_moment_distribution_diagram()
    fig2.savefig('moment_distribution_diagram.png', dpi=300, bbox_inches='tight')
    
    fig3 = create_force_equilibrium_diagram()
    fig3.savefig('force_equilibrium_diagram.png', dpi=300, bbox_inches='tight')
    
    plt.close('all')
    print("Diagrams created successfully!")