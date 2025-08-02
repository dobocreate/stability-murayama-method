"""
村山の式を用いたトンネル切羽安定性評価計算モジュール
"""

import numpy as np
from scipy import integrate
from typing import Tuple, Dict, Any
import warnings


class MurayamaCalculator:
    """村山の式による切羽安定性計算クラス"""
    
    def __init__(self, H: float, gamma: float, phi: float, c: float, q: float = 0):
        """
        パラメータの初期化
        
        Args:
            H: 切羽高さ [m]
            gamma: 地山単位体積重量 [kN/m³]
            phi: 地山内部摩擦角 [度]
            c: 地山粘着力 [kN/m²]
            q: 上載荷重 [kN/m²] (デフォルト: 0)
        """
        self.H = H
        self.gamma = gamma
        self.phi_deg = phi
        self.phi = np.radians(phi)  # ラジアンに変換
        self.c = c
        self.q = q
        
        # 入力値の妥当性チェック
        self._validate_inputs()
    
    def _validate_inputs(self):
        """入力値の妥当性をチェック"""
        errors = []
        
        if self.H <= 0:
            errors.append("切羽高さHは正の値である必要があります")
        if self.H > 50:
            errors.append("切羽高さHが大きすぎます（通常50m以下）")
            
        if self.gamma <= 0:
            errors.append("単位体積重量γは正の値である必要があります")
        if self.gamma < 10 or self.gamma > 30:
            errors.append("単位体積重量γが通常範囲外です（通常10-30 kN/m³）")
            
        if self.phi_deg < 0 or self.phi_deg > 90:
            errors.append("内部摩擦角φは0-90度の範囲である必要があります")
        if self.phi_deg > 60:
            warnings.warn("内部摩擦角φが大きすぎる可能性があります（通常60度以下）")
            
        if self.c < 0:
            errors.append("粘着力cは負の値にはなりません")
        if self.c > 200:
            warnings.warn("粘着力cが大きすぎる可能性があります（通常200 kN/m²以下）")
            
        if self.q < 0:
            errors.append("上載荷重qは負の値にはなりません")
            
        if errors:
            raise ValueError("\n".join(errors))
    
    def logarithmic_spiral(self, theta: float, r0: float) -> float:
        """
        対数らせん曲線の半径を計算
        
        Args:
            theta: 角度 [ラジアン]
            r0: 初期半径 [m]
            
        Returns:
            半径 r [m]
        """
        return r0 * np.exp(theta * np.tan(self.phi))
    
    def calculate_moments(self, r0: float, theta_max: float) -> Dict[str, float]:
        """
        各種モーメントを計算
        
        Args:
            r0: 対数らせんの初期半径 [m]
            theta_max: 滑り面の最大角度 [ラジアン]
            
        Returns:
            各種モーメントの辞書
        """
        # 土塊の面積と重心位置を計算
        area, centroid_x = self._calculate_area_and_centroid(r0, theta_max)
        
        # 土塊重量によるモーメント
        M_W = self.gamma * area * centroid_x
        
        # 上載荷重によるモーメント
        M_Q = 0
        if self.q > 0:
            # 上載荷重の作用幅と重心位置を計算
            b_q = r0 * (np.exp(theta_max * np.tan(self.phi)) - 1) / np.tan(self.phi)
            x_q = b_q / 2
            M_Q = self.q * b_q * x_q
        
        # せん断抵抗力によるモーメント
        M_tau = self._calculate_shear_resistance_moment(r0, theta_max)
        
        return {
            'M_W': M_W,
            'M_Q': M_Q,
            'M_tau': M_tau,
            'area': area,
            'centroid_x': centroid_x
        }
    
    def _calculate_area_and_centroid(self, r0: float, theta_max: float) -> Tuple[float, float]:
        """
        滑り土塊の面積と重心位置を計算
        
        Args:
            r0: 初期半径 [m]
            theta_max: 最大角度 [ラジアン]
            
        Returns:
            面積 [m²], 重心のx座標 [m]
        """
        def integrand_area(theta):
            r = self.logarithmic_spiral(theta, r0)
            return 0.5 * r**2
        
        def integrand_centroid_x(theta):
            r = self.logarithmic_spiral(theta, r0)
            return (2/3) * r**3 * np.cos(theta)
        
        # 数値積分
        area, _ = integrate.quad(integrand_area, 0, theta_max)
        moment_x, _ = integrate.quad(integrand_centroid_x, 0, theta_max)
        
        centroid_x = moment_x / area if area > 0 else 0
        
        return area, centroid_x
    
    def _calculate_shear_resistance_moment(self, r0: float, theta_max: float) -> float:
        """
        せん断抵抗力によるモーメントを計算
        
        Args:
            r0: 初期半径 [m]
            theta_max: 最大角度 [ラジアン]
            
        Returns:
            せん断抵抗力モーメント [kN·m]
        """
        def integrand(theta):
            r = self.logarithmic_spiral(theta, r0)
            # 微小要素の長さ
            dr_dtheta = r0 * np.tan(self.phi) * np.exp(theta * np.tan(self.phi))
            ds = np.sqrt(r**2 + dr_dtheta**2)
            
            # せん断抵抗力（粘着力成分のみ、簡略化）
            tau = self.c
            
            return tau * r * ds
        
        M_tau, _ = integrate.quad(integrand, 0, theta_max)
        
        # 内部摩擦角の効果を考慮（簡略化）
        M_tau *= (1 + np.tan(self.phi))
        
        return M_tau
    
    def calculate_required_pressure(self, r0: float, theta_max: float) -> float:
        """
        必要支保圧を計算
        
        Args:
            r0: 初期半径 [m]
            theta_max: 最大角度 [ラジアン]
            
        Returns:
            必要支保圧 P [kN/m²]
        """
        moments = self.calculate_moments(r0, theta_max)
        
        # モーメントつり合いから支保圧を計算
        # M_W + M_Q = M_tau + M_P
        # M_P = P * H * (H/2) = P * H²/2
        M_P_required = moments['M_W'] + moments['M_Q'] - moments['M_tau']
        
        # 必要支保圧
        P = 2 * M_P_required / (self.H ** 2)
        
        return max(0, P)  # 負の値にならないようにする
    
    def parametric_study(self, r0_range: Tuple[float, float], theta_range: Tuple[float, float], 
                        n_points: int = 20) -> Dict[str, Any]:
        """
        パラメトリックスタディを実行
        
        Args:
            r0_range: r0の範囲 (最小値, 最大値) [m]
            theta_range: θの範囲 (最小値, 最大値) [度]
            n_points: 各パラメータの分割数
            
        Returns:
            解析結果の辞書
        """
        r0_values = np.linspace(r0_range[0], r0_range[1], n_points)
        theta_values = np.linspace(np.radians(theta_range[0]), np.radians(theta_range[1]), n_points)
        
        # 結果格納用の配列
        P_matrix = np.zeros((n_points, n_points))
        detailed_results = []  # 詳細な計算結果を格納
        max_P = 0
        critical_r0 = 0
        critical_theta = 0
        critical_moments = None
        
        # 全組み合わせで計算
        for i, r0 in enumerate(r0_values):
            for j, theta in enumerate(theta_values):
                # モーメント計算
                moments = self.calculate_moments(r0, theta)
                
                # 必要支保圧の計算
                M_P_required = moments['M_W'] + moments['M_Q'] - moments['M_tau']
                P = 2 * M_P_required / (self.H ** 2)
                P = max(0, P)
                
                P_matrix[i, j] = P
                
                # 詳細結果の保存
                detailed_results.append({
                    'r0_m': r0,
                    'theta_rad': theta,
                    'theta_deg': np.degrees(theta),
                    'r_end_m': self.logarithmic_spiral(theta, r0),
                    'area_m2': moments['area'],
                    'centroid_x_m': moments['centroid_x'],
                    'M_W_kNm': moments['M_W'],
                    'M_Q_kNm': moments['M_Q'],
                    'M_tau_kNm': moments['M_tau'],
                    'M_P_required_kNm': M_P_required,
                    'P_kN_m2': P
                })
                
                if P > max_P:
                    max_P = P
                    critical_r0 = r0
                    critical_theta = theta
                    critical_moments = moments.copy()
        
        # 安全率の計算（仮定：既存支保圧100 kN/m²に対する比）
        assumed_support_pressure = 100.0
        safety_factor = assumed_support_pressure / max_P if max_P > 0 else float('inf')
        
        # 安定度の評価
        if safety_factor >= 1.5:
            stability = "安定"
            stability_percentage = min(100, safety_factor * 50)
        elif safety_factor >= 1.0:
            stability = "要注意"
            stability_percentage = 50 + (safety_factor - 1.0) * 100
        else:
            stability = "不安定"
            stability_percentage = max(0, safety_factor * 50)
        
        return {
            'r0_values': r0_values,
            'theta_values': theta_values,
            'theta_degrees': np.degrees(theta_values),
            'P_matrix': P_matrix,
            'detailed_results': detailed_results,
            'max_P': max_P,
            'critical_r0': critical_r0,
            'critical_theta': critical_theta,
            'critical_theta_deg': np.degrees(critical_theta),
            'critical_moments': critical_moments,
            'safety_factor': safety_factor,
            'stability': stability,
            'stability_percentage': stability_percentage
        }