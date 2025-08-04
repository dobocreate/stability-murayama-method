"""
村山の式を用いたトンネル切羽安定性評価システム（修正版）
Streamlitアプリケーション - murayama_stability_design_revised.mdに基づく実装
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from murayama_calculator_revised import MurayamaCalculatorRevised
import io


# ページ設定
st.set_page_config(
    page_title="トンネル切羽安定性評価システム（修正版）",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSSスタイルの適用
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 20px;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .stability-stable {
        color: #00cc00;
        font-size: 2rem;
        font-weight: bold;
    }
    .stability-warning {
        color: #ff9900;
        font-size: 2rem;
        font-weight: bold;
    }
    .stability-unstable {
        color: #ff0000;
        font-size: 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# タイトル（中央配置）
st.markdown("""
<h1 style='text-align: center;'>🚇 トンネル切羽の安定性評価アプリ（村山の式）</h1>
""", unsafe_allow_html=True)

# タブの作成
tab1, tab2, tab3 = st.tabs(["安定性評価", "技術情報", "使い方"])

with tab1:
    # 2列レイアウト
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # 地盤条件の入力
        st.subheader("地盤条件")
        
        # 土被り（最初に配置）
        H = st.number_input(
            "土被り H (m)",
            min_value=0.0,
            max_value=200.0,
            value=30.0,
            step=5.0,
            help="地表面からトンネル天端までの土被りを入力してください"
        )
        
        # 切羽高さ
        H_f = st.number_input(
            "切羽高さ H_f (m)",
            min_value=0.1,
            max_value=50.0,
            value=10.0,
            step=0.5,
            help="トンネル断面の高さを入力してください"
        )
        
        # 地山単位体積重量
        gamma = st.number_input(
            "地山単位体積重量 γ (kN/m³)",
            min_value=10.0,
            max_value=30.0,
            value=20.0,
            step=0.5,
            help="地山の単位体積重量を入力してください"
        )
        
        # 地山内部摩擦角
        phi = st.number_input(
            "地山内部摩擦角 φ (度)",
            min_value=0.0,
            max_value=60.0,
            value=30.0,
            step=1.0,
            help="地山の内部摩擦角を入力してください"
        )
        
        # 地山粘着力
        coh = st.number_input(
            "地山粘着力 coh (kPa)",
            min_value=0.0,
            max_value=1000.0,
            value=20.0,
            step=5.0,
            help="地山の粘着力を入力してください（kPa単位）"
        )
        
        # 解析パラメータ
        st.subheader("解析パラメータ")
        
        st.write("**探索角度 θ_d の範囲 (度)**")
        theta_col1, theta_col2 = st.columns(2)
        with theta_col1:
            theta_min = st.number_input(
                "最小値",
                min_value=10,
                max_value=80,
                value=20,
                step=1,
                key="theta_min"
            )
        with theta_col2:
            theta_max = st.number_input(
                "最大値",
                min_value=20,
                max_value=90,
                value=80,
                step=1,
                key="theta_max"
            )
        
        # 計算点数は自動で決定（1度刻み）
        n_points = theta_max - theta_min + 1
        st.write(f"**計算点数**: {n_points} 点（1度刻み）")
        
        # 詳細パラメータ
        st.subheader("詳細パラメータ")
        
        with st.expander("係数の設定（通常は変更不要）"):
            alpha = st.number_input(
                "影響幅係数 α",
                min_value=1.0,
                max_value=3.0,
                value=1.8,
                step=0.1,
                help="標準値: 1.8（有効幅係数 = α/2 = 0.9）"
            )
            
            K = st.number_input(
                "経験係数 K",
                min_value=0.5,
                max_value=2.0,
                value=1.0,
                step=0.1,
                help="Terzaghi実験による係数（標準値: 1.0、範囲: 1.0～1.5）"
            )
            
            force_finite_cover = st.checkbox(
                "有限土被り式を強制的に使用", 
                value=True,
                help="チェックすると深部条件（H > 1.5B）でも常に有限土被り式を使用します"
            )
    
    with col2:
        # 安定性評価結果
        st.subheader("安定性評価結果")
        
        # 計算実行ボタン
        if st.button("解析の実行", type="primary", use_container_width=True):
            try:
                # 計算機インスタンスの作成
                calculator = MurayamaCalculatorRevised(H_f, gamma, phi, coh, H, alpha, K, force_finite_cover)
                
                # パラメトリックスタディの実行
                with st.spinner("解析を実行中..."):
                    results = calculator.parametric_study(
                        (theta_min, theta_max),
                        n_points
                    )
                
                # 結果をセッション状態に保存
                st.session_state.results = results
                st.session_state.calculator = calculator
                st.session_state.calculated = True
                
            except ValueError as e:
                st.error(f"入力エラー: {str(e)}")
                st.session_state.calculated = False
            except Exception as e:
                st.error(f"計算エラー: {str(e)}")
                st.session_state.calculated = False
        
        # 結果の表示
        if hasattr(st.session_state, 'calculated') and st.session_state.calculated:
            results = st.session_state.results
            
            # 安定性の表示
            stability_class = {
                "安定": "stability-stable",
                "安定（自立）": "stability-stable",
                "要注意": "stability-warning",
                "不安定": "stability-unstable"
            }
            
            emoji = {"安定": "😊", "安定（自立）": "😊", "要注意": "😐", "不安定": "😰"}
            
            # メトリクスの表示（2:1:1の割合）
            col2_1, col2_2, col2_3 = st.columns([2, 1, 1])
            
            with col2_1:
                st.metric(
                    label="必要支保圧",
                    value=f"{results['max_P']:.2f} kN/m²"
                )
            
            with col2_2:
                # 安全率の表示（無限大の場合は特別な表示）
                if results['safety_factor'] == float('inf'):
                    st.metric(
                        label="安全率",
                        value="∞"
                    )
                else:
                    st.metric(
                        label="安全率",
                        value=f"{results['safety_factor']:.2f}"
                    )
            
            with col2_3:
                st.metric(
                    label="安定度",
                    value=f"{results['stability_percentage']:.0f}%"
                )
            
            # 安定性評価の表示
            st.markdown(
                f"""
                <div class="metric-container">
                    <div class="{stability_class[results['stability']]}">
                        {results['stability']} {emoji[results['stability']]}
                    </div>
                    <p>切羽は{results['stability']}状態です</p>
                    <p>最大必要支保圧: {results['max_P']:.2f} kN/m²</p>
                    <p>臨界条件: θ_d = {results['critical_theta_deg']:.1f}°</p>
                    <p>対応する r₀ = {results['critical_r0']:.2f} m</p>
                    <p>崩壊位置までの水平距離: B = {results.get('critical_geometry', {}).get('B', 0):.2f} m</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # 概念図
        st.markdown("---")
        st.subheader("概念図")
        st.image("data/image.jpg", width=None, use_container_width=False)
    
    # 詳細結果の表示
    if hasattr(st.session_state, 'calculated') and st.session_state.calculated:
        st.markdown("---")
        st.subheader("詳細計算結果")
        
        results_tab1, results_tab2 = st.tabs(["計算結果", "結果出力"])
        
        with results_tab1:
            # 必要支保圧の分布グラフ
            fig = go.Figure()
            
            # theta_valuesを取得
            theta_values = results.get('theta_degrees', [])
            
            # P値の抽出
            if results.get('detailed_results') and len(results['detailed_results']) > 0:
                P_values = [r.get('P_kN_m2', 0) for r in results['detailed_results']]
            else:
                P_values = []
            
            fig.add_trace(go.Scatter(
                x=theta_values,
                y=P_values,
                mode='lines+markers',
                name='必要支保圧',
                line=dict(width=2)
            ))
            
            # 最大値の位置にマーカーを追加（旗揚げ付き）
            fig.add_trace(go.Scatter(
                x=[results['critical_theta_deg']],
                y=[results['max_P']],
                mode='markers+text',
                marker=dict(size=15, color='red', symbol='x'),
                name='最大支保圧点',
                text=[f"最大支保圧点<br>θ_d = {results['critical_theta_deg']:.1f}°<br>P = {results['max_P']:.2f} kN/m²"],
                textposition="top center",
                textfont=dict(size=12, color='red'),
                showlegend=True
            ))
            
            fig.update_layout(
                title="探索角度θ_dと必要支保圧の関係",
                xaxis_title="探索角度 θ_d (度)",
                yaxis_title="必要支保圧 P (kN/m²)",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with results_tab2:
            # 2列レイアウトで表示
            col_result1, col_result2 = st.columns(2)
            
            with col_result1:
                st.write("**入力パラメータ**")
                input_data = {
                    "パラメータ": ["切羽高さ H_f", "地山単位体積重量 γ", "地山内部摩擦角 φ", "地山粘着力 coh",
                            "土被り H", "影響幅係数 α", "経験係数 K"],
                    "値": [f"{H_f} m", f"{gamma} kN/m³", f"{phi}°", f"{coh} kPa",
                        f"{H} m" if H is not None else "深部前提", f"{alpha}", f"{K}"],
                }
                st.table(pd.DataFrame(input_data))
            
            with col_result2:
                st.write("**解析結果サマリー**")
                # 安全率の表示（無限大の場合の処理）
                safety_factor_str = "∞" if results['safety_factor'] == float('inf') else f"{results['safety_factor']:.2f}"
                
                summary_data = {
                    "項目": ["最大必要支保圧", "臨界探索角度 θ_d", "対応する初期半径 r₀", "安全率", "安定性評価"],
                    "値": [
                        f"{results['max_P']:.2f} kN/m²",
                        f"{results['critical_theta_deg']:.1f}°",
                        f"{results['critical_r0']:.2f} m",
                        safety_factor_str,
                        results['stability']
                    ],
                }
                st.table(pd.DataFrame(summary_data))
            
            
            # 全角度範囲での詳細な計算結果を生成
            calculator = st.session_state.calculator
            theta_range = (theta_min, theta_max)
            
            # 全角度での計算結果を取得
            all_results = []
            for theta_deg in range(theta_min, theta_max + 1):
                theta_rad = np.radians(theta_deg)
                try:
                    result = calculator.calculate_support_pressure(theta_rad)
                    if result['valid']:
                        geom = result['geometry']
                        all_results.append({
                            'theta_deg': theta_deg,
                            'theta_rad': theta_rad,
                            'r0_m': geom['r0'],
                            'rd_m': geom['rd'],
                            'B_m': geom['B'],
                            'la_m': geom['la'],
                            'lp_m': geom['lp'],
                            'q_kN_m2': result['q'],
                            'Wf_kN': result['Wf'],
                            'lw_m': result['lw'],
                            'Mc_kNm': result['Mc'],
                            'P_kN_m2': result['P']
                        })
                except:
                    continue
            
            # DataFrameを作成
            df_all_results = pd.DataFrame(all_results)
            
            # プレビュー用のDataFrame（既存のresultsから）
            df_detailed = pd.DataFrame(results['detailed_results'])
            
            # カラム名を日本語に変更
            column_names = {
                'theta_deg': '探索角度θ_d (度)',
                'theta_rad': '探索角度θ_d (rad)',
                'r0_m': '初期半径r0 (m)',
                'rd_m': '終端半径rd (m)',
                'B_m': '水平投影幅B (m)',
                'la_m': '距離la (m)',
                'lp_m': '支保圧作用腕lp (m)',
                'q_kN_m2': '等価合力q (kN/m²)',
                'Wf_kN': '自重Wf (kN)',
                'lw_m': '自重作用点lw (m)',
                'Mc_kNm': '粘着抵抗モーメントMc (kN·m)',
                'P_kN_m2': '必要支保圧P (kN/m²)'
            }
            df_detailed_jp = df_detailed.rename(columns=column_names)
            df_all_results_jp = df_all_results.rename(columns=column_names)
            
            # CSV変換（全結果）
            csv_buffer = io.StringIO()
            df_all_results_jp.to_csv(csv_buffer, index=False, encoding='utf-8')
            csv = csv_buffer.getvalue().encode('utf-8-sig')
            
            # プレビュー表示（臨界角度±10データポイント）
            st.write("**データプレビュー（臨界角度θ_d周辺±10データポイント）**")
            
            # 臨界角度を取得
            critical_theta = results['critical_theta_deg']
            
            # 臨界角度を中心とした±10データポイントの範囲を決定
            preview_min = max(0, len(df_detailed_jp) // 2 - 10)  # 中央付近から-10
            preview_max = min(len(df_detailed_jp), len(df_detailed_jp) // 2 + 11)  # 中央付近から+10
            
            # より正確に臨界角度周辺のデータを抽出
            if 'theta_deg' in df_detailed.columns:
                # 臨界角度に最も近いインデックスを見つける
                theta_values = df_detailed['theta_deg'].values
                critical_index = np.argmin(np.abs(theta_values - critical_theta))
                
                # ±10データポイントの範囲を設定
                preview_min = max(0, critical_index - 10)
                preview_max = min(len(df_detailed_jp), critical_index + 11)
            
            preview_df = df_detailed_jp.iloc[preview_min:preview_max]
            
            # 臨界角度行をピンク色で強調表示
            def highlight_critical_row(row):
                if abs(float(row['探索角度θ_d (度)']) - critical_theta) < 0.5:
                    return ['background-color: #FFB6C1'] * len(row)  # ピンク色
                else:
                    return [''] * len(row)
            
            styled_preview = preview_df.style.apply(highlight_critical_row, axis=1)
            st.dataframe(styled_preview, use_container_width=True)
            
            # ダウンロードボタン
            st.download_button(
                label="計算結果の出力",
                data=csv,
                file_name="murayama_analysis_revised_results.csv",
                mime="text/csv;charset=utf-8-sig",
                help=f"指定した角度範囲（{theta_min}°～{theta_max}°）の全計算結果をCSVファイルでダウンロードします"
            )

with tab2:
    # 技術情報ページ
    st.header("技術情報（修正版）")
    
    st.subheader("1. 実装の特徴")
    st.write("""
    本システムは村山の式による切羽安定性評価を実装したもので、以下の特徴があります：
    
    - **r₀を入力から削除**：幾何の閉合式から内部で自動決定
    - **支保圧の作用腕**：l_p = r₀sinφ + H_f/2 に統一
    - **粘着抵抗モーメント**：閉形式 Mc = coh(rd² - r₀²)/(2tanφ) を採用
    - **上載荷重の等価合力**：影響幅係数αと経験係数Kを導入
    - **有限土被りの考慮**：深部前提と有限土被りの切り替えが可能
    - **分岐なし実装**：条件分岐を削除し、数値的安定性を向上
    """)
    
    st.subheader("2. 幾何の閉合")
    st.latex(r"""
    \begin{align}
    r_0 &= \frac{H_f}{\exp(\theta_d\tan\phi)\sin(\phi+\theta_d) - \sin\phi} \\
    r_d &= r_0 \exp(\theta_d\tan\phi) \\
    l_a &= r_d \cos(\phi+\theta_d) \\
    B &= r_0\cos\phi - l_a \\
    l_p &= r_0\sin\phi + \frac{H_f}{2}
    \end{align}
    """)
    
    st.subheader("3. 荷重の等価合力")
    
    st.write("**有効幅**")
    st.latex(r"B_{eff} = \frac{\alpha}{2} B")
    
    st.write("**上載荷重の等価合力 q**")
    st.latex(r"""
    q = \frac{\alpha B\left(\gamma - \frac{2c}{\alpha B}\right)}{2K\tan\phi}
    \left[1 - \exp\left(-\frac{2KH}{\alpha B}\tan\phi\right)\right]
    """)
    
    st.write("""
    - 深部条件では角括弧を1と近似
    - H は土被り（H_f は切羽高さ）
    - 標準値：α = 1.8、K = 1.0
    """)
    
    st.subheader("4. 自重の計算")
    st.write("""
    **分岐なし実装による統一的な計算式**
    
    自重の等価合力の重心位置 lw2 は、以下の統一式で計算されます：
    """)
    
    st.latex(r"""
    lw_2 = S\cos(\phi + T) + \frac{2}{3} \cdot \frac{U}{1-\cos V} \cdot \frac{1-\cos^2 V}{V-\sin V \cos V} \cdot \sin V \cdot \cos\left(\arctan\frac{B}{H_f}\right) - \frac{U\cos V}{1-\cos V} \cdot \cos\left(\arctan\frac{B}{H_f}\right)
    """)
    
    st.write("""
    ここで、中間パラメータ S, T, U, V は対数らせん滑り面の幾何形状から決定されます。
    この実装により、条件分岐がなくなり、数値的安定性が向上しました。
    """)
    
    st.subheader("5. 粘着の抵抗モーメント")
    st.latex(r"M_c = \frac{coh(r_d^2 - r_0^2)}{2\tan\phi}")
    
    st.subheader("6. 支保圧の算定")
    st.latex(r"""
    P = \frac{W_f \cdot l_w + q \cdot B \cdot \left(l_a + \frac{B}{2}\right) - M_c}{l_p}
    """)
    
    st.write("""
    θ_d を掃引して P を評価し、最大値を必要支保圧とします。
    """)

with tab3:
    # 使い方ページ
    st.header("使い方（修正版）")
    
    st.subheader("基本的な操作手順")
    st.write("""
    1. **地盤条件の入力**
       - 切羽高さ H_f、単位体積重量 γ、内部摩擦角 φ、粘着力 coh を入力
       - 粘着力の単位は **kPa** です（旧版の kN/m² から変更）
    
    2. **土被り条件の設定**
       - 深部条件の場合：チェックボックスをオフのまま
       - 有限土被りの場合：チェックボックスをオンにして土被り C を入力
    
    3. **詳細パラメータ（必要に応じて）**
       - 影響幅係数 α（標準: 1.8）
       - 経験係数 K（標準: 1.0、Terzaghi実験では1.0～1.5）
    
    4. **解析パラメータの設定**
       - 探索角度 θ_d の範囲を設定（標準: 20°～80°）
       - 計算は1度刻みで自動実行されます
    
    5. **解析の実行**
       - 「解析の実行」ボタンをクリック
       - r₀ は自動的に計算されます（入力不要）
    """)
    
    st.subheader("旧版との違い")
    st.warning("""
    **重要な変更点**
    - r₀ の入力欄がありません（自動計算）
    - 粘着力の単位が kPa に変更されています
    - 上載荷重 q は入力ではなく、内部で計算されます
    - 探索するのは θ_d のみです（r₀ の範囲設定は不要）
    """)
    
    st.subheader("パラメータの目安")
    st.info("""
    **軟岩（風化岩）の場合**
    - γ: 22～24 kN/m³
    - φ: 30～40 度
    - coh: 30～50 kPa（旧: kN/m²）
    
    **土砂地山の場合**
    - γ: 18～20 kN/m³
    - φ: 25～35 度
    - coh: 10～30 kPa
    
    **粘性土の場合**
    - γ: 16～18 kN/m³
    - φ: 20～30 度
    - coh: 20～40 kPa
    """)

# フッター
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888;'>
    村山の式を用いたトンネル切羽安定性評価システム（修正版） v2.0
    </div>
    """,
    unsafe_allow_html=True
)