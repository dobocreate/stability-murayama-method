"""
村山の式を用いたトンネル切羽安定性評価計算モジュール（修正版）
murayama_stability_design_revised.mdに基づく実装
"""

import numpy as np
from typing import Dict, Any, Optional, List
import warnings


class MurayamaCalculatorRevised:
    """村山の式による切羽安定性計算クラス（修正版）"""
    
    def __init__(self, H_f: float, gamma: float, phi: float, coh: float, 
                 H: Optional[float] = None, alpha: float = 1.8, K: float = 1.0,
                 force_finite_cover: bool = False):
        """
        パラメータの初期化
        
        Args:
            H_f: 切羽高さ [m]
            gamma: 地山単位体積重量 [kN/m³]
            phi: 地山内部摩擦角 [度]
            coh: 地山粘着力 [kPa]
            H: 土被り [m] (Noneの場合は深部前提)
            alpha: 影響幅係数 (標準: 1.8)
            K: 経験係数 (標準: 1.0, Terzaghi実験では1～1.5)
            force_finite_cover: 有限土被り式を強制的に使用するフラグ (標準: False)
        """
        self.H_f = H_f
        self.gamma = gamma
        self.phi_deg = phi
        self.phi = np.radians(phi)  # ラジアンに変換
        self.coh = coh
        self.H = H
        self.alpha = alpha
        self.K = K
        self.force_finite_cover = force_finite_cover
        
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
        if self.phi_deg < 1.0:
            errors.append("内部摩擦角φは1度以上である必要があります（数値安定性のため）")
        if self.phi_deg > 60:
            warnings.warn("内部摩擦角φが大きすぎる可能性があります（通常60度以下）")
            
        if self.coh < 0:
            errors.append("粘着力cohは負の値にはなりません")
            
        if self.H is not None and self.H < 0:
            errors.append("土被りHは負の値にはなりません")
            
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
        上載荷重の等価合力 q をユーザー式で算定（指数の"中"に tanφ）。深部/有限は B に基づき都度評価。
        
        Args:
            B: 滑り面の水平投影幅 [m]
            
        Returns:
            等価合力 q [kN/m²]
        """
        # force_finite_coverがTrueの場合は常に有限土被り式を使用
        if self.force_finite_cover:
            is_deep = False
        else:
            # 深部条件の判定（土被りが幅の1.5倍以上：便宜上の閾値）
            is_deep = (self.H is None) or (self.H > 1.5 * B)
        
        if is_deep:
            # 深部前提（角括弧→1）
            q = (self.alpha * B * (self.gamma - 2 * self.coh / (self.alpha * B))) / (2 * self.K * np.tan(self.phi))
        else:
            # 有限土被り（指数の"中"に tanφ を掛ける）
            fac = 1.0 - np.exp(-2.0 * self.K * self.H * np.tan(self.phi) / (self.alpha * B))
            q = (self.alpha * B * (self.gamma - 2 * self.coh / (self.alpha * B))) / (2 * self.K * np.tan(self.phi)) * fac
        
        return float(q)  # 丸めない（負値も許容：Excel整合）  # 丸めない（負値も許容：Excel整合）
    
    def calculate_self_weight(self, r0: float, rd: float, theta_d: float, B: float, la: float) -> Dict[str, float]:
        """
        自重の等価合力と作用点の計算（Excel M9式準拠）
        
        Args:
            r0: 初期半径 [m]
            rd: 終端半径 [m]
            theta_d: 探索角度 [ラジアン]
            B: 滑り面の水平投影幅 [m]
            la: 滑り面上端の水平位置 [m]
            
        Returns:
            自重関連のパラメータ (Wf, lw, w1, lw1, w2, lw2)
        """
        # 自重の等価合力（1m幅当たり）
        term1 = self.H_f * B / 2  # 三角形部分
        term2 = (rd**2 - r0**2) / (4 * np.tan(self.phi))  # 曲線領域
        term3 = r0 * rd * np.sin(theta_d) / 2
        
        Wf = self.gamma * (term1 + term2 - term3)
        
        # 作用点の計算（Excel M9式準拠）
        # 三角形部分
        w1 = self.gamma * self.H_f * B / 2
        lw1 = la + B / 3
        
        # 曲線部分の重量
        w2 = self.gamma * (term2 - term3)
        
        # 曲線部分の重心（Excel M9式の実装）

        # 中間パラメータの計算（ExcelのS,T,U,V）
        O = np.hypot(B, self.H_f)  # 切羽の対角線長
        P = np.arctan2(self.H_f, B)  # 方向角（rad）
        
        # S（Excelのx）の計算
        S = np.sqrt((O**2)/4.0 + r0**2 - O*r0*np.cos(P + self.phi))
        
        # T（Excelのθc）の計算
        R = r0 * np.sin(P + self.phi)
        cos_arg = np.clip(R / S, -1.0, 1.0) if S > 0.0 else 1.0
        T = np.arccos(cos_arg) - (P + self.phi - np.pi/2.0)
        
        # U（Excelのh）の計算
        U = (r0*np.exp(T*np.tan(self.phi)) - S) * (r0*np.sin(P + self.phi)) / (S if S != 0.0 else 1.0)
        
        # V（Excelのβ）の計算
        if abs(U) > 1e-12:
            V = np.pi - 2*np.arctan(O/(2*U))
        else:
            V = np.pi
        
        # Excel M9式の実装
        # 第1項
        term1_lw2 = S * np.cos(self.phi + T)
        
        # 第2項の計算
        cos_V = np.cos(V)
        sin_V = np.sin(V)
        

        # 各要素の計算
        A = U / (1 - cos_V)
        B_num = 1 - cos_V**2
        B_den = V - sin_V * cos_V
        

        B_frac = B_num / B_den
        C = sin_V
        D = U * cos_V / (1 - cos_V)
        
        # 第2項（Excel準拠：常にB/H_fを使用）
        cos_direction = np.cos(np.arctan2(B, self.H_f))
        
        term2_inner = (2.0/3.0) * A * B_frac * C - D
        term2_lw2 = term2_inner * cos_direction
        
        lw2 = term1_lw2 + term2_lw2

        
        # 合成重心（重み付き平均）
        if abs(w1 + w2) > 1e-12:
            lw = (w1 * lw1 + w2 * lw2) / (w1 + w2)
        else:
            lw = la + B / 2
        
        return {
            'Wf': Wf,
            'lw': lw,
            'w1': w1,
            'lw1': lw1,
            'w2': w2,
            'lw2': lw2
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
        Mc = self.coh * (rd**2 - r0**2) / (2 * np.tan(self.phi))
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
        weight_params = self.calculate_self_weight(r0, rd, theta_d, B, la)
        Wf = weight_params['Wf']
        lw = weight_params['lw']
        w1 = weight_params['w1']
        lw1 = weight_params['lw1']
        w2 = weight_params['w2']
        lw2 = weight_params['lw2']
        
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
            'w1': w1,
            'lw1': lw1,
            'w2': w2,
            'lw2': lw2,
            'Mc': Mc,
            'numerator': numerator
        }
    
    def calculate_true_safety_factor(self, theta_d: float) -> Dict[str, Any]:
        """
        強度定数を低減して必要支保圧が0になる低減係数を求め、真の安全率を計算
        強度低減法：c' = c/F, tan(φ') = tan(φ)/F
        
        Args:
            theta_d: 評価角度 [ラジアン]
            
        Returns:
            安全率計算結果の辞書
        """
        # 元の強度定数を保存
        original_coh = self.coh
        original_phi = self.phi
        original_phi_deg = self.phi_deg
        
        # まず現在の強度での必要支保圧を計算
        original_result = self.calculate_support_pressure(theta_d)
        original_P = original_result['P']
        
        # 強度変化履歴を記録
        reduction_history = []
        
        # 初期点を記録
        reduction_history.append({
            'factor': 1.0,
            'coh': original_coh,
            'phi_deg': original_phi_deg,
            'P': original_P
        })
        
        # 二分探索でP=0となる係数を求める
        lower = 0.1   # 最小係数
        upper = 10.0  # 最大係数
        tolerance = 0.001
        
        # P(factor)を評価する内部関数
        def evaluate_P_at_factor(factor: float) -> float:
            """指定された強度低減係数でのPを評価"""
            self.coh = original_coh / factor
            self.phi = np.arctan(np.tan(original_phi) / factor)
            self.phi_deg = np.degrees(self.phi)
            try:
                result = self.calculate_support_pressure(theta_d)
                return result['P']
            except Exception:
                return np.nan
        
        # 初期括り出し: P(lower)とP(upper)が異符号になるまで範囲を拡張
        P_lower = evaluate_P_at_factor(lower)
        P_upper = evaluate_P_at_factor(upper)
        
        expand_count = 0
        max_expand = 8
        
        while expand_count < max_expand and (
            np.isnan(P_lower) or np.isnan(P_upper) or 
            np.sign(P_lower) == np.sign(P_upper)
        ):
            # P>0（不安定）が見つからない場合はupperを拡大（強度をより低減）
            if np.isnan(P_upper) or P_upper <= 0.0:
                upper *= 2.0
                P_upper = evaluate_P_at_factor(upper)
            
            # P<=0（安定）が見つからない場合はlowerを縮小（強度をより増加）
            if np.isnan(P_lower) or P_lower > 0.0:
                lower /= 2.0
                P_lower = evaluate_P_at_factor(lower)
            
            expand_count += 1
        
        # 括り出しに失敗した場合の処理
        if np.isnan(P_lower) or np.isnan(P_upper) or np.sign(P_lower) == np.sign(P_upper):
            # 強度定数を元に戻す
            self.coh = original_coh
            self.phi = original_phi
            self.phi_deg = original_phi_deg
            
            # 常に安定（P<=0）の場合は安全率→∞、常に不安定の場合は0
            if P_lower <= 0 and P_upper <= 0:
                return {
                    'safety_factor': float('inf'),
                    'critical_reduction_factor': np.nan,
                    'original_P': original_P,
                    'reduction_history': reduction_history,
                    'evaluation_points': [],
                    'theta_d': theta_d,
                    'theta_d_deg': np.degrees(theta_d)
                }
            else:
                return {
                    'safety_factor': 0.0,
                    'critical_reduction_factor': np.nan,
                    'original_P': original_P,
                    'reduction_history': reduction_history,
                    'evaluation_points': [],
                    'theta_d': theta_d,
                    'theta_d_deg': np.degrees(theta_d)
                }
        
        iteration = 0
        max_iterations = 30
        
        while upper - lower > tolerance and iteration < max_iterations:
            factor = (upper + lower) / 2
            
            # 強度定数を変更
            # c' = c/F
            self.coh = original_coh / factor
            # tan(φ') = tan(φ)/F → φ' = arctan(tan(φ)/F)
            self.phi = np.arctan(np.tan(original_phi) / factor)
            self.phi_deg = np.degrees(self.phi)
            
            # 変更した強度で必要支保圧を計算
            try:
                result = self.calculate_support_pressure(theta_d)
                P_modified = result['P']
                
                # 履歴に追加
                reduction_history.append({
                    'factor': factor,
                    'coh': self.coh,
                    'phi_deg': self.phi_deg,
                    'P': P_modified
                })
                
                if P_modified > 0:
                    # まだ不安定なので安全率を下げる（強度を上げる）
                    upper = factor
                else:
                    # 安定しているので安全率を上げる（強度を下げる）
                    lower = factor
                    
            except Exception:
                # 計算エラーの場合は範囲を狭める
                if factor < 1.0:
                    lower = factor
                else:
                    upper = factor
            
            iteration += 1
        
        # 最終的な安全率
        final_factor = (upper + lower) / 2
        # 安全率は強度低減係数そのもの
        # P>0の場合：強度を増加（F<1）させてP=0 → 安全率<1
        # P<0の場合：強度を低減（F>1）させてP=0 → 安全率>1
        safety_factor = final_factor
        
        # 強度定数を元に戻す
        self.coh = original_coh
        self.phi = original_phi
        self.phi_deg = original_phi_deg
        
        # 追加の評価点を生成（グラフ描画用）
        # 安全率の範囲を動的に決定
        if safety_factor < 1.0:
            # P>0（不安定）の場合は0.1から1.5の範囲
            eval_min = max(0.1, safety_factor * 0.5)
            eval_max = min(1.5, safety_factor * 2.0)
        else:
            # P<0（安定）の場合は0.5から最大値の範囲
            eval_min = 0.5
            eval_max = max(2.0, safety_factor * 1.2)
        
        # 評価する強度低減係数の範囲を生成
        # 注意：これらの値は強度低減係数Fであり、そのまま安全率となる
        evaluation_factors = np.linspace(eval_min, eval_max, 20)
        # 臨界点（F=1.0、元の強度）を確実に含める
        evaluation_factors = np.append(evaluation_factors, 1.0)
        # 実際の安全率（臨界強度低減係数）も含める
        evaluation_factors = np.append(evaluation_factors, safety_factor)
        evaluation_factors = np.sort(np.unique(evaluation_factors))
        evaluation_points = []
        
        # 各強度低減係数でのP値を計算
        for eval_factor in evaluation_factors:
            # 強度低減係数から強度を計算
            # c' = c/F
            self.coh = original_coh / eval_factor
            # tan(φ') = tan(φ)/F
            self.phi = np.arctan(np.tan(original_phi) / eval_factor)
            self.phi_deg = np.degrees(self.phi)
            
            try:
                result = self.calculate_support_pressure(theta_d)
                evaluation_points.append({
                    'factor': eval_factor,
                    'safety_factor': eval_factor,
                    'coh': self.coh,
                    'phi_deg': self.phi_deg,
                    'P': result['P']
                })
            except Exception:
                pass
        
        # 強度定数を最終的に元に戻す
        self.coh = original_coh
        self.phi = original_phi
        self.phi_deg = original_phi_deg
        
        return {
            'safety_factor': safety_factor,
            'critical_reduction_factor': final_factor,
            'original_P': original_P,
            'reduction_history': reduction_history,
            'evaluation_points': sorted(evaluation_points, key=lambda x: x['safety_factor']),
            'theta_d': theta_d,
            'theta_d_deg': np.degrees(theta_d)
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
        
        # 新しい安全率計算
        true_sf_result = self.calculate_true_safety_factor(critical_result['theta_d'])
        safety_factor = true_sf_result['safety_factor']
        
        # 安定性の評価（P値と安全率の両方を考慮）
        if max_P <= 0:
            # 支保不要（自立可能）
            if safety_factor >= 1.5:
                stability = "安定（自立）"
            elif safety_factor >= 1.2:
                stability = "安定（自立・要注意）"
            else:
                stability = "要注意（自立）"
        else:
            # 支保必要（P > 0）
            if safety_factor >= 1.0:
                # 安全率が1以上は物理的にあり得ない（P>0なら安全率<1のはず）
                # 計算エラーの可能性があるため警告
                stability = "計算エラー（要確認）"
            elif safety_factor >= 0.8:
                stability = "要注意（要支保）"
            elif safety_factor >= 0.6:
                stability = "不安定（要支保）"
            else:
                stability = "危険（要支保）"
        
        return {
            'max_P': max_P,
            'critical_theta_d': critical_result['theta_d'],
            'critical_theta_d_deg': critical_result['theta_d_deg'],
            'critical_geometry': critical_result['geometry'],
            'critical_params': critical_result,
            'stability': stability,
            'safety_factor': safety_factor,
            'true_safety_factor_result': true_sf_result,
            'all_results': results
        }
    
    def parametric_study(self, theta_range: tuple = (20, 80), 
                        n_points: int = None) -> Dict[str, Any]:
        """
        パラメトリックスタディ（Streamlit互換性のため）
        
        Args:
            theta_range: θの範囲 (最小値, 最大値) [度]
            n_points: 計算点数（Noneの場合は1度刻み）
            
        Returns:
            解析結果の辞書（旧インターフェース互換）
        """
        # 1度刻みの計算
        if n_points is None:
            theta_step = 1.0
            n_points = int(theta_range[1] - theta_range[0]) + 1
        else:
            theta_step = (theta_range[1] - theta_range[0]) / (n_points - 1)
        
        # 臨界圧の探索
        critical = self.find_critical_pressure(theta_range, theta_step)
        
        # 旧インターフェース用のデータ整形
        if n_points is None or theta_step == 1.0:
            # 1度刻みの場合
            theta_degrees = np.arange(theta_range[0], theta_range[1] + 1, 1)
        else:
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
            'critical_geometry': critical['critical_geometry'],
            'critical_moments': {
                'area': 0,  # ダミー値
                'centroid_x': critical['critical_params']['lw'],
                'M_W': critical['critical_params']['Wf'] * critical['critical_params']['lw'],
                'M_Q': critical['critical_params']['q'] * critical['critical_geometry']['B'] * (critical['critical_geometry']['la'] + critical['critical_geometry']['B']/2),
                'M_tau': critical['critical_params']['Mc']
            },
            'safety_factor': critical['safety_factor'],
            'stability': critical['stability'],
            'stability_percentage': min(100, critical['safety_factor'] * 50) if critical['safety_factor'] != float('inf') else 100,
            'true_safety_factor_result': critical.get('true_safety_factor_result', None)
        }