"""
村山の式を用いたトンネル切羽安定性評価計算モジュール（修正版）
murayama_stability_design_revised.mdに基づく実装
"""

import numpy as np
from typing import Dict, Any, Optional, List
import warnings


class MurayamaCalculatorRevised:
    """村山の式による切羽安定性計算クラス（修正版）"""
    
    def __init__(self, H_f: float, gamma: float, phi: float, c: float, 
                 C: Optional[float] = None, alpha: float = 1.8, K: float = 1.0):
        """
        パラメータの初期化
        
        Args:
            H_f: 切羽高さ [m]
            gamma: 地山単位体積重量 [kN/m³]
            phi: 地山内部摩擦角 [度]
            c: 地山粘着力 [kPa]
            C: 土被り [m] (Noneの場合は深部前提)
            alpha: 影響幅係数 (標準: 1.8)
            K: 経験係数 (標準: 1.0, Terzaghi実験では1～1.5)
        """
        self.H_f = H_f
        self.gamma = gamma
        self.phi_deg = phi
        self.phi = np.radians(phi)  # ラジアンに変換
        self.c = c
        self.C = C
        self.alpha = alpha
        self.K = K
        
        # 深部条件の判定（土被りが幅の1.5倍以上）
        self.is_deep = C is None or C > 1.5 * H_f
        
        # 入力値の妥当性チェック
        self._validate_inputs()
    
    def _validate_inputs(self):
        """入力値の妥当性をチェック"""
        errors = []
        
        if self.H_f <= 0:
            errors.append("切羽高さH_fは正の値である必要があります")
        if self.H_f > 50:
            errors.append("切羽高さH_fが大きすぎます（通常50m以下）")
            
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
            
        if self.C is not None and self.C < 0:
            errors.append("土被りCは負の値にはなりません")
            
        if self.alpha <= 0:
            errors.append("影響幅係数αは正の値である必要があります")
            
        if self.K <= 0:
            errors.append("経験係数Kは正の値である必要があります")
            
        if errors:
            raise ValueError("\n".join(errors))
    
    def calculate_geometry(self, theta_d: float) -> Dict[str, float]:
        """
        幾何の閉合計算
        
        Args:
            theta_d: 探索角度 [ラジアン]
            
        Returns:
            幾何パラメータの辞書 (r0, rd, la, B, lp)
        """
        # r0の計算（幾何の閉合式）
        denominator = np.exp(theta_d * np.tan(self.phi)) * np.sin(self.phi + theta_d) - np.sin(self.phi)
        if abs(denominator) < 1e-10:
            raise ValueError(f"幾何的に不適切な角度: theta_d = {np.degrees(theta_d):.1f}°")
        
        r0 = self.H_f / denominator
        
        # その他の幾何パラメータ
        rd = r0 * np.exp(theta_d * np.tan(self.phi))
        la = rd * np.cos(self.phi + theta_d)
        B = r0 * np.cos(self.phi) - la
        lp = r0 * np.sin(self.phi) + self.H_f / 2
        
        return {
            'r0': r0,
            'rd': rd,
            'la': la,
            'B': B,
            'lp': lp
        }
    
    def calculate_equivalent_surcharge(self, B: float) -> float:
        """
        上載荷重の等価合力qの計算
        
        Args:
            B: 滑り面の水平投影幅 [m]
            
        Returns:
            等価合力 q [kN/m²]
        """
        # 有効幅
        B_eff = (self.alpha / 2) * B
        
        # 深部条件または土被りが与えられていない場合
        if self.is_deep:
            # 深部前提：角括弧を1とみなす
            q = (self.alpha * B * (self.gamma - 2 * self.c / (self.alpha * B))) / (2 * self.K * np.tan(self.phi))
        else:
            # 有限土被りの場合
            H = self.C  # 土被り
            exp_term = 1 - np.exp(-2 * self.K * H * np.tan(self.phi) / (self.alpha * B))
            q = (self.alpha * B * (self.gamma - 2 * self.c / (self.alpha * B))) / (2 * self.K * np.tan(self.phi)) * exp_term
        
        return max(0, q)  # 負の値を防ぐ
    
    def calculate_self_weight(self, r0: float, rd: float, theta_d: float, B: float) -> Dict[str, float]:
        """
        自重の等価合力と作用点の計算
        
        Args:
            r0: 初期半径 [m]
            rd: 終端半径 [m]
            theta_d: 探索角度 [ラジアン]
            B: 滑り面の水平投影幅 [m]
            
        Returns:
            自重関連のパラメータ (Wf, lw)
        """
        # 自重の等価合力（1m幅当たり）
        term1 = self.H_f * B / 2  # 三角形部分
        term2 = (rd**2 - r0**2) / (4 * np.tan(self.phi))  # 曲線領域
        term3 = r0 * rd * np.sin(theta_d) / 2
        
        Wf = self.gamma * (term1 + term2 - term3)
        
        # 作用点の計算（より正確な計算）
        # 三角形部分
        w1 = self.gamma * self.H_f * B / 2
        lw1 = B / 3  # 三角形の重心は底辺から1/3
        
        # 曲線領域の重心計算（より正確な式）
        w2 = self.gamma * (term2 - term3)
        
        # 曲線領域の重心位置（対数らせんの重心）
        if abs(theta_d) > 1e-10 and abs(np.tan(self.phi)) > 1e-10:
            # 対数らせん領域の重心x座標の解析的計算
            k = np.tan(self.phi)
            factor1 = (r0**3 / (9 * k**2 + 1)) * (np.exp(3 * k * theta_d) - 1)
            factor2 = (3 * k * np.cos(theta_d) + np.sin(theta_d)) * np.exp(3 * k * theta_d)
            factor3 = 3 * k
            x_centroid_curve = (factor1 / (3 * k)) * (factor2 - factor3) / (term2 - term3) if abs(w2) > 1e-10 else B * 0.6
            
            # 座標変換して切羽からの距離に
            lw2 = min(B * 0.8, max(B * 0.4, x_centroid_curve))  # 安全のため範囲制限
        else:
            lw2 = B * 0.6  # デフォルト近似値
        
        # 合成重心
        if abs(w1 + w2) > 1e-10:
            lw = (w1 * lw1 + w2 * lw2) / (w1 + w2)
        else:
            lw = B / 2
        
        return {
            'Wf': Wf,
            'lw': lw
        }
    
    def calculate_cohesion_moment(self, r0: float, rd: float) -> float:
        """
        粘着の抵抗モーメント（閉形式）
        
        Args:
            r0: 初期半径 [m]
            rd: 終端半径 [m]
            
        Returns:
            粘着抵抗モーメント Mc [kN·m]
        """
        Mc = self.c * (rd**2 - r0**2) / (2 * np.tan(self.phi))
        return Mc
    
    def calculate_support_pressure(self, theta_d: float) -> Dict[str, Any]:
        """
        指定角度での必要支保圧の計算
        
        Args:
            theta_d: 探索角度 [ラジアン]
            
        Returns:
            計算結果の辞書
        """
        # 幾何の計算
        geom = self.calculate_geometry(theta_d)
        r0, rd, la, B, lp = geom['r0'], geom['rd'], geom['la'], geom['B'], geom['lp']
        
        # B が負または極小の場合はスキップ
        if B <= 0.1:
            return {
                'theta_d': theta_d,
                'P': -float('inf'),
                'valid': False
            }
        
        # 等価合力の計算
        q = self.calculate_equivalent_surcharge(B)
        
        # 自重の計算
        weight_params = self.calculate_self_weight(r0, rd, theta_d, B)
        Wf = weight_params['Wf']
        lw = weight_params['lw']
        
        # 粘着抵抗モーメント
        Mc = self.calculate_cohesion_moment(r0, rd)
        
        # 支保圧の算定（モーメント釣合い）
        numerator = Wf * lw + q * B * (la + B/2) - Mc
        P = numerator / lp
        
        return {
            'theta_d': theta_d,
            'theta_d_deg': np.degrees(theta_d),
            'P': P,
            'valid': True,
            'geometry': geom,
            'q': q,
            'Wf': Wf,
            'lw': lw,
            'Mc': Mc,
            'numerator': numerator
        }
    
    def find_critical_pressure(self, theta_range: tuple = (20, 80), 
                             theta_step: float = 1.0) -> Dict[str, Any]:
        """
        臨界支保圧の探索
        
        Args:
            theta_range: 探索角度範囲 [度] (min, max)
            theta_step: 角度刻み [度]
            
        Returns:
            臨界条件での計算結果
        """
        # 角度範囲をラジアンに変換
        theta_min_rad = np.radians(theta_range[0])
        theta_max_rad = np.radians(theta_range[1])
        theta_step_rad = np.radians(theta_step)
        
        # 探索角度の配列
        theta_values = np.arange(theta_min_rad, theta_max_rad + theta_step_rad, theta_step_rad)
        
        # 結果保存用
        results = []
        max_P = -float('inf')
        critical_result = None
        
        for theta_d in theta_values:
            try:
                result = self.calculate_support_pressure(theta_d)
                if result['valid']:
                    results.append(result)
                    if result['P'] > max_P:
                        max_P = result['P']
                        critical_result = result
            except Exception as e:
                # エラーが発生した角度はスキップ
                warnings.warn(f"計算エラー at θ = {np.degrees(theta_d):.1f}°: {str(e)}")
                continue
        
        if critical_result is None:
            raise ValueError("有効な解が見つかりませんでした")
        
        # 安定性の評価
        if max_P <= 0:
            stability = "安定（自立）"
            safety_factor = float('inf')
        else:
            # 仮定：既存支保圧100 kN/m²に対する比
            assumed_pressure = 100.0
            safety_factor = assumed_pressure / max_P
            
            if safety_factor >= 1.5:
                stability = "安定"
            elif safety_factor >= 1.0:
                stability = "要注意"
            else:
                stability = "不安定"
        
        return {
            'max_P': max_P,
            'critical_theta_d': critical_result['theta_d'],
            'critical_theta_d_deg': critical_result['theta_d_deg'],
            'critical_geometry': critical_result['geometry'],
            'critical_params': critical_result,
            'stability': stability,
            'safety_factor': safety_factor,
            'all_results': results
        }
    
    def parametric_study(self, theta_range: tuple = (20, 80), 
                        n_points: int = 20) -> Dict[str, Any]:
        """
        パラメトリックスタディ（Streamlit互換性のため）
        
        Args:
            theta_range: θの範囲 (最小値, 最大値) [度]
            n_points: 計算点数
            
        Returns:
            解析結果の辞書（旧インターフェース互換）
        """
        theta_step = (theta_range[1] - theta_range[0]) / (n_points - 1)
        
        # 臨界圧の探索
        critical = self.find_critical_pressure(theta_range, theta_step)
        
        # 旧インターフェース用のデータ整形
        theta_degrees = np.linspace(theta_range[0], theta_range[1], n_points)
        P_values = []
        detailed_results = []
        
        for result in critical['all_results']:
            theta_deg = result['theta_d_deg']
            P = result['P']
            P_values.append(P)
            
            # 詳細結果（CSV出力用）
            geom = result['geometry']
            detailed_results.append({
                'theta_deg': theta_deg,
                'theta_rad': result['theta_d'],
                'r0_m': geom['r0'],
                'rd_m': geom['rd'],
                'B_m': geom['B'],
                'la_m': geom['la'],
                'lp_m': geom['lp'],
                'q_kN_m2': result['q'],
                'Wf_kN': result['Wf'],
                'lw_m': result['lw'],
                'Mc_kNm': result['Mc'],
                'P_kN_m2': P
            })
        
        # ダミーのr0値（互換性のため）
        r0_values = np.ones(n_points) * critical['critical_geometry']['r0']
        
        # P_matrixの作成（1D配列を2Dに拡張）
        P_matrix = np.array(P_values).reshape(1, -1)
        
        return {
            'r0_values': r0_values,
            'theta_values': np.radians(theta_degrees),
            'theta_degrees': theta_degrees,
            'P_matrix': P_matrix,
            'detailed_results': detailed_results,
            'max_P': critical['max_P'],
            'critical_r0': critical['critical_geometry']['r0'],
            'critical_theta': critical['critical_theta_d'],
            'critical_theta_deg': critical['critical_theta_d_deg'],
            'critical_moments': {
                'area': 0,  # ダミー値
                'centroid_x': critical['critical_params']['lw'],
                'M_W': critical['critical_params']['Wf'] * critical['critical_params']['lw'],
                'M_Q': critical['critical_params']['q'] * critical['critical_geometry']['B'] * (critical['critical_geometry']['la'] + critical['critical_geometry']['B']/2),
                'M_tau': critical['critical_params']['Mc']
            },
            'safety_factor': critical['safety_factor'],
            'stability': critical['stability'],
            'stability_percentage': min(100, critical['safety_factor'] * 50) if critical['safety_factor'] != float('inf') else 100
        }