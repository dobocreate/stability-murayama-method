"""
村山の式を用いたトンネル切羽安定性評価システム
Streamlitアプリケーション
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from murayama_calculator import MurayamaCalculator
import io


# ページ設定
st.set_page_config(
    page_title="トンネル切羽安定性評価システム",
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

# タイトル
st.title("🚇 トンネル切羽安定性評価システム")

# タブの作成
tab1, tab2, tab3 = st.tabs(["安定性評価", "技術情報", "使い方"])

with tab1:
    # 2列レイアウト
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # 地盤条件の入力
        st.subheader("地盤条件")
        
        H = st.number_input(
            "切羽高さ H (m)",
            min_value=0.1,
            max_value=50.0,
            value=10.0,
            step=0.5,
            help="トンネル断面の高さを入力してください"
        )
        
        gamma = st.number_input(
            "地山単位体積重量 γ (kN/m³)",
            min_value=10.0,
            max_value=30.0,
            value=20.0,
            step=0.5,
            help="地山の単位体積重量を入力してください"
        )
        
        phi = st.number_input(
            "地山内部摩擦角 φ (度)",
            min_value=0.0,
            max_value=60.0,
            value=30.0,
            step=1.0,
            help="地山の内部摩擦角を入力してください"
        )
        
        c = st.number_input(
            "地山粘着力 c (kN/m²)",
            min_value=0.0,
            max_value=200.0,
            value=20.0,
            step=5.0,
            help="地山の粘着力を入力してください"
        )
        
        use_surcharge = st.checkbox("上載荷重を考慮する")
        q = 0.0
        if use_surcharge:
            q = st.number_input(
                "上載荷重 q (kN/m²)",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=5.0,
                help="地表面の上載荷重を入力してください"
            )
        
        # 解析パラメータ
        st.markdown("---")
        st.subheader("解析パラメータ")
        
        r0_min = st.number_input(
            "初期半径 r₀ 最小値 (m)",
            min_value=0.1,
            max_value=10.0,
            value=0.5,
            step=0.1
        )
        
        r0_max = st.number_input(
            "初期半径 r₀ 最大値 (m)",
            min_value=0.1,
            max_value=20.0,
            value=5.0,
            step=0.1
        )
        
        theta_min = st.number_input(
            "角度 θ 最小値 (度)",
            min_value=5.0,
            max_value=90.0,
            value=10.0,
            step=5.0
        )
        
        theta_max = st.number_input(
            "角度 θ 最大値 (度)",
            min_value=5.0,
            max_value=90.0,
            value=60.0,
            step=5.0
        )
        
        n_points = st.number_input(
            "計算点数",
            min_value=10,
            max_value=50,
            value=20,
            step=5,
            help="各パラメータの分割数"
        )
    
    with col2:
        # 切羽安定性評価結果
        st.subheader("切羽安定性評価結果")
        
        # 計算実行ボタン
        if st.button("解析の実行", type="primary", use_container_width=True):
            try:
                # 計算機インスタンスの作成
                calculator = MurayamaCalculator(H, gamma, phi, c, q)
                
                # パラメトリックスタディの実行
                with st.spinner("解析を実行中..."):
                    results = calculator.parametric_study(
                        (r0_min, r0_max),
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
                "要注意": "stability-warning",
                "不安定": "stability-unstable"
            }
            
            emoji = {"安定": "😊", "要注意": "😐", "不安定": "😰"}
            
            # メトリクスの表示
            col2_1, col2_2, col2_3 = st.columns(3)
            
            with col2_1:
                st.metric(
                    label="必要支保圧",
                    value=f"{results['max_P']:.2f} kN/m²"
                )
            
            with col2_2:
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
                    <p>臨界条件: r₀ = {results['critical_r0']:.2f} m, θ = {results['critical_theta_deg']:.1f}°</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # 解析概念図
        st.markdown("---")
        st.subheader("解析概念図")
        st.info("村山の式による切羽安定解析：対数らせん滑り面を仮定した極限つり合い法")
    
    # 詳細結果の表示
    if hasattr(st.session_state, 'calculated') and st.session_state.calculated:
        st.markdown("---")
        st.subheader("詳細解析結果")
        
        results_tab1, results_tab2, results_tab3 = st.tabs(["滑り面解析", "感度分析", "詳細データ"])
        
        with results_tab1:
            # 2Dヒートマップの作成
            fig = px.imshow(
                results['P_matrix'].T,
                x=results['r0_values'],
                y=results['theta_degrees'],
                labels=dict(x="初期半径 r₀ (m)", y="角度 θ (度)", color="必要支保圧 P (kN/m²)"),
                title="パラメトリックスタディ結果 - 必要支保圧の分布",
                color_continuous_scale="RdYlBu_r",
                aspect="auto"
            )
            
            # 最大値の位置にマーカーを追加
            fig.add_trace(
                go.Scatter(
                    x=[results['critical_r0']],
                    y=[results['critical_theta_deg']],
                    mode='markers',
                    marker=dict(size=15, color='red', symbol='x'),
                    name='最大支保圧点',
                    showlegend=True
                )
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        with results_tab2:
            # r0固定時のグラフ
            col_sens1, col_sens2 = st.columns(2)
            
            with col_sens1:
                # 臨界r0での角度θの影響
                critical_r0_idx = np.argmin(np.abs(results['r0_values'] - results['critical_r0']))
                fig1 = go.Figure()
                fig1.add_trace(go.Scatter(
                    x=results['theta_degrees'],
                    y=results['P_matrix'][critical_r0_idx, :],
                    mode='lines+markers',
                    name=f"r₀ = {results['critical_r0']:.2f} m"
                ))
                fig1.update_layout(
                    title=f"角度θと必要支保圧の関係（r₀ = {results['critical_r0']:.2f} m）",
                    xaxis_title="角度 θ (度)",
                    yaxis_title="必要支保圧 P (kN/m²)",
                    height=400
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col_sens2:
                # 臨界θでのr0の影響
                critical_theta_idx = np.argmin(np.abs(results['theta_values'] - results['critical_theta']))
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    x=results['r0_values'],
                    y=results['P_matrix'][:, critical_theta_idx],
                    mode='lines+markers',
                    name=f"θ = {results['critical_theta_deg']:.1f}°"
                ))
                fig2.update_layout(
                    title=f"初期半径r₀と必要支保圧の関係（θ = {results['critical_theta_deg']:.1f}°）",
                    xaxis_title="初期半径 r₀ (m)",
                    yaxis_title="必要支保圧 P (kN/m²)",
                    height=400
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        with results_tab3:
            # 詳細データの表示
            st.write("**入力パラメータ**")
            input_data = {
                "パラメータ": ["切羽高さ H", "地山単位体積重量 γ", "地山内部摩擦角 φ", "地山粘着力 c", "上載荷重 q"],
                "値": [f"{H} m", f"{gamma} kN/m³", f"{phi}°", f"{c} kN/m²", f"{q} kN/m²"],
            }
            st.table(pd.DataFrame(input_data))
            
            st.write("**解析結果サマリー**")
            summary_data = {
                "項目": ["最大必要支保圧", "臨界初期半径 r₀", "臨界角度 θ", "安全率", "安定性評価"],
                "値": [
                    f"{results['max_P']:.2f} kN/m²",
                    f"{results['critical_r0']:.2f} m",
                    f"{results['critical_theta_deg']:.1f}°",
                    f"{results['safety_factor']:.2f}",
                    results['stability']
                ],
            }
            st.table(pd.DataFrame(summary_data))
            
            # CSV出力機能
            st.write("**データエクスポート**")
            
            # 詳細な計算結果のDataFrame作成
            df_detailed = pd.DataFrame(results['detailed_results'])
            
            # カラム名を日本語に変更（オプション）
            column_names = {
                'r0_m': '初期半径r0 (m)',
                'theta_rad': '角度θ (rad)',
                'theta_deg': '角度θ (度)',
                'r_end_m': '終端半径r (m)',
                'area_m2': '滑り土塊面積 (m²)',
                'centroid_x_m': '重心x座標 (m)',
                'M_W_kNm': '土塊重量モーメントM_W (kN·m)',
                'M_Q_kNm': '上載荷重モーメントM_Q (kN·m)',
                'M_tau_kNm': 'せん断抵抗モーメントM_τ (kN·m)',
                'M_P_required_kNm': '必要支保圧モーメントM_P (kN·m)',
                'P_kN_m2': '必要支保圧P (kN/m²)'
            }
            df_detailed_jp = df_detailed.rename(columns=column_names)
            
            # 出力形式の選択
            output_format = st.radio(
                "出力形式を選択",
                ["詳細データ（計算過程を含む）", "基本データ（r0, θ, Pのみ）"],
                horizontal=True
            )
            
            if output_format == "詳細データ（計算過程を含む）":
                # 詳細データのCSV変換
                # BOM付きUTF-8でエンコード（Excelでの文字化け防止）
                csv_buffer = io.StringIO()
                df_detailed_jp.to_csv(csv_buffer, index=False, encoding='utf-8')
                csv = csv_buffer.getvalue().encode('utf-8-sig')
                filename = "murayama_analysis_detailed_results.csv"
                
                # プレビュー表示
                st.write("データプレビュー（最初の5行）")
                st.dataframe(df_detailed_jp.head())
            else:
                # 基本データのみ抽出
                df_basic = df_detailed[['r0_m', 'theta_deg', 'P_kN_m2']]
                csv_buffer = io.StringIO()
                df_basic.to_csv(csv_buffer, index=False, encoding='utf-8')
                csv = csv_buffer.getvalue().encode('utf-8-sig')
                filename = "murayama_analysis_basic_results.csv"
                
                # プレビュー表示
                st.write("データプレビュー（最初の5行）")
                st.dataframe(df_basic.head())
            
            # ダウンロードボタン
            st.download_button(
                label="計算結果をCSVでダウンロード",
                data=csv,
                file_name=filename,
                mime="text/csv;charset=utf-8-sig"
            )
            
            # 臨界条件での詳細結果も表示
            if results['critical_moments']:
                st.write("**臨界条件での詳細計算結果**")
                critical_data = {
                    "項目": [
                        "初期半径 r₀",
                        "角度 θ",
                        "終端半径 r",
                        "滑り土塊面積",
                        "重心x座標",
                        "土塊重量モーメント M_W",
                        "上載荷重モーメント M_Q",
                        "せん断抵抗モーメント M_τ",
                        "必要支保圧モーメント M_P",
                        "必要支保圧 P"
                    ],
                    "値": [
                        f"{results['critical_r0']:.3f} m",
                        f"{results['critical_theta_deg']:.1f}° ({results['critical_theta']:.3f} rad)",
                        f"{st.session_state.calculator.logarithmic_spiral(results['critical_theta'], results['critical_r0']):.3f} m",
                        f"{results['critical_moments']['area']:.3f} m²",
                        f"{results['critical_moments']['centroid_x']:.3f} m",
                        f"{results['critical_moments']['M_W']:.2f} kN·m",
                        f"{results['critical_moments']['M_Q']:.2f} kN·m",
                        f"{results['critical_moments']['M_tau']:.2f} kN·m",
                        f"{results['critical_moments']['M_W'] + results['critical_moments']['M_Q'] - results['critical_moments']['M_tau']:.2f} kN·m",
                        f"{results['max_P']:.2f} kN/m²"
                    ]
                }
                st.table(pd.DataFrame(critical_data))

with tab2:
    # 技術情報ページ
    st.header("技術情報")
    
    st.subheader("1. 村山の式について")
    st.write("""
    村山の式は、トンネル切羽の安定性を評価するための理論的手法です。
    この手法は、土木学会などで広く認められており、実務においても多く使用されています。
    """)
    
    st.subheader("基本理論")
    st.write("""
    切羽前方の地山に対数らせん滑り面を仮定し、滑り土塊に作用する力のモーメントのつり合いから、
    切羽の安定に必要な支保圧を算出します。
    """)
    
    st.latex(r"""
    \begin{align}
    \text{対数らせん曲線：} \quad r &= r_0 \times e^{\theta \times \tan \phi} \\
    \text{モーメントつり合い式：} \quad M_W + M_Q &= M_\tau + M_P
    \end{align}
    """)
    
    st.write("""
    ここで、
    - $M_W$：土塊重量によるモーメント
    - $M_Q$：上載荷重によるモーメント  
    - $M_τ$：せん断抵抗力によるモーメント
    - $M_P$：支保圧によるモーメント
    """)
    
    st.subheader("2. 詳細な計算過程")
    
    # 計算過程の詳細をタブで整理
    calc_tab1, calc_tab2, calc_tab3 = st.tabs(["計算フロー", "詳細計算式", "計算例"])
    
    with calc_tab1:
        st.write("### 計算フローの概要")
        st.write("""
        1. **地盤条件の入力**（γ, φ, c, H, q）
        2. **解析パラメータの設定**（r₀範囲、θ範囲、計算点数）
        3. **対数らせん滑り面に基づくモーメント計算**
        4. **パラメトリックスタディの実施**（r₀とθを変化させて繰り返し計算）
        5. **最不利条件の抽出**（最大支保圧となる滑り面の特定）
        """)
        
        # フローチャートの説明
        st.info("""
        **計算の流れ**
        1. 各(r₀, θ)の組み合わせに対して以下を計算：
           - 滑り土塊の面積 A
           - 滑り土塊の重心位置 x̄
           - 各種モーメント（M_W, M_Q, M_τ）
           - モーメントつり合いから必要支保圧 P
        2. 全ての組み合わせから最大の P を特定
        """)
    
    with calc_tab2:
        st.write("### 詳細な計算式")
        
        st.write("#### 2.1 滑り土塊の面積計算")
        st.latex(r"""
        A = \int_0^{\theta_{max}} \frac{1}{2} r^2 d\theta = \frac{r_0^2}{2} \int_0^{\theta_{max}} e^{2\theta \tan\phi} d\theta
        """)
        st.latex(r"""
        A = \frac{r_0^2}{4\tan\phi} \left( e^{2\theta_{max} \tan\phi} - 1 \right)
        """)
        
        st.write("#### 2.2 滑り土塊の重心位置")
        st.latex(r"""
        \bar{x} = \frac{1}{A} \int_0^{\theta_{max}} \frac{1}{3} r^3(\theta) \cos\theta \, d\theta
        """)
        st.write("※ この積分は一般に解析的に解けないため、数値積分を使用します。")
        
        st.write("#### 2.3 土塊重量によるモーメント")
        st.latex(r"""
        M_W = \gamma \cdot A \cdot \bar{x}
        """)
        
        st.write("#### 2.4 上載荷重によるモーメント")
        st.latex(r"""
        b_q = r(\theta_{max}) \cos\theta_{max} - r_0
        """)
        st.latex(r"""
        M_Q = q \cdot b_q \cdot \frac{b_q}{2}
        """)
        
        st.write("#### 2.5 せん断抵抗力によるモーメント")
        st.write("滑り面に沿う微小要素の長さ：")
        st.latex(r"""
        ds = r \sqrt{1 + \tan^2\phi} \, d\theta = r \sec\phi \, d\theta
        """)
        st.write("せん断抵抗力によるモーメント（簡略化）：")
        st.latex(r"""
        M_\tau = c \cdot r_0^2 \cdot \sec\phi \int_0^{\theta_{max}} e^{2\theta \tan\phi} d\theta \cdot (1 + \tan\phi)
        """)
        
        st.write("#### 2.6 必要支保圧の算出")
        st.write("モーメントのつり合い：")
        st.latex(r"""
        M_W + M_Q = M_\tau + M_P
        """)
        st.write("支保圧によるモーメント：")
        st.latex(r"""
        M_P = P \cdot H \cdot \frac{H}{2} = \frac{P \cdot H^2}{2}
        """)
        st.write("したがって、必要支保圧は：")
        st.latex(r"""
        P = \frac{2(M_W + M_Q - M_\tau)}{H^2}
        """)
    
    with calc_tab3:
        st.write("### 計算例")
        st.write("以下の条件での計算過程を示します：")
        
        # 計算例の条件
        example_data = {
            "パラメータ": ["H", "γ", "φ", "c", "q", "r₀", "θ"],
            "値": ["10 m", "20 kN/m³", "30°", "20 kN/m²", "0 kN/m²", "2.0 m", "30° (0.524 rad)"]
        }
        st.table(pd.DataFrame(example_data))
        
        st.write("#### 計算過程")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**1. 対数らせんの終端半径**")
            st.latex(r"r = 2.0 \times e^{0.524 \times \tan(30°)} = 2.71 \text{ m}")
            
            st.write("**2. 滑り土塊の面積**")
            st.latex(r"A = \frac{2.0^2}{4 \times \tan(30°)} \times (e^{0.605} - 1)")
            st.latex(r"A = 5.76 \text{ m}^2")
            
            st.write("**3. 重心位置（数値積分）**")
            st.latex(r"\bar{x} \approx 1.85 \text{ m}")
        
        with col2:
            st.write("**4. 土塊重量モーメント**")
            st.latex(r"M_W = 20 \times 5.76 \times 1.85 = 213.1 \text{ kN·m}")
            
            st.write("**5. せん断抵抗モーメント**")
            st.latex(r"M_\tau \approx 180.5 \text{ kN·m}")
            
            st.write("**6. 必要支保圧**")
            st.latex(r"P = \frac{2 \times (213.1 + 0 - 180.5)}{10^2}")
            st.latex(r"P = 0.65 \text{ kN/m}^2")
        
        st.info("この計算を全てのパラメータ組み合わせで実行し、最大値を求めることで最不利条件を特定します。")
    
    st.subheader("3. パラメータの詳細説明")
    param_df = pd.DataFrame({
        "パラメータ": ["H", "γ", "φ", "c", "q", "r₀", "θ"],
        "説明": [
            "切羽高さ（トンネル断面の高さ）",
            "地山の単位体積重量",
            "地山の内部摩擦角（せん断抵抗角）",
            "地山の粘着力",
            "地表面の上載荷重（建物・交通荷重等）",
            "対数らせんの初期半径",
            "滑り面の開き角度"
        ],
        "一般的な範囲": [
            "5～15",
            "18～25",
            "20～40",
            "10～50",
            "0～50",
            "0.1～10",
            "10～90"
        ],
        "単位": ["m", "kN/m³", "度", "kN/m²", "kN/m²", "m", "度"]
    })
    st.table(param_df)
    
    st.subheader("4. 使用上の注意事項")
    st.warning("""
    - 本手法は、均質な地盤を前提としています。層状地盤や不均質地盤の場合は、別途検討が必要です。
    - 地下水の影響は考慮していません。地下水位が高い場合は、別途水圧を考慮する必要があります。
    - 計算結果は理論値であり、実際の施工では安全率を考慮して支保工を設計してください。
    - 地盤定数は、現場での調査・試験結果に基づいて設定することが重要です。
    """)

with tab3:
    # 使い方ページ
    st.header("使い方")
    
    st.subheader("基本的な操作手順")
    st.write("""
    1. **地盤条件の入力**
       - 左側のパネルに、トンネルの寸法と地盤の物性値を入力します
       - 上載荷重がある場合は、チェックボックスを選択して値を入力します
    
    2. **解析パラメータの設定**
       - 対数らせんのパラメータ範囲を設定します
       - 計算点数を増やすと精度が向上しますが、計算時間も増加します
    
    3. **解析の実行**
       - 「解析の実行」ボタンをクリックして計算を開始します
       - 計算が完了すると、右側に結果が表示されます
    
    4. **結果の確認**
       - 安定性評価（安定/要注意/不安定）を確認します
       - 必要支保圧、安全率、安定度の数値を確認します
       - 詳細結果タブで、パラメトリックスタディの結果を確認できます
    
    5. **データのエクスポート**
       - 「詳細データ」タブから、計算結果をCSV形式でダウンロードできます
    """)
    
    st.subheader("入力値の目安")
    st.info("""
    **軟岩（風化岩）の場合**
    - γ: 22～24 kN/m³
    - φ: 30～40 度
    - c: 30～50 kN/m²
    
    **土砂地山の場合**
    - γ: 18～20 kN/m³
    - φ: 25～35 度
    - c: 10～30 kN/m²
    
    **粘性土の場合**
    - γ: 16～18 kN/m³
    - φ: 20～30 度
    - c: 20～40 kN/m²
    """)
    
    st.subheader("よくある質問")
    with st.expander("計算が収束しない場合はどうすればよいですか？"):
        st.write("""
        - パラメータの範囲を見直してください
        - 特に初期半径r₀の最小値が小さすぎると数値誤差が発生することがあります
        - 計算点数を減らしてみてください
        """)
    
    with st.expander("安全率はどのように評価されていますか？"):
        st.write("""
        仮定として既存支保圧100 kN/m²に対する比として計算しています。
        実際の設計では、現場条件に応じた適切な安全率を設定してください。
        """)
    
    with st.expander("3次元効果は考慮されていますか？"):
        st.write("""
        本システムは2次元解析を行っています。
        大深度トンネルや特殊な条件下では、3次元効果を考慮した詳細な解析が推奨されます。
        """)

# フッター
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888;'>
    村山の式を用いたトンネル切羽安定性評価システム v1.0
    </div>
    """,
    unsafe_allow_html=True
)