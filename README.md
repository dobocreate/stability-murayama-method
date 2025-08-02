# トンネル切羽安定性評価システム

村山の式を用いたトンネル切羽の安定性評価を行うWebアプリケーションです。

## 概要

本システムは、対数らせん滑り面を仮定した極限つり合い法（村山の式）により、トンネル切羽の安定性を評価し、必要な支保圧を算出します。

## 機能

- 地盤条件の入力と安定性評価
- パラメトリックスタディによる最不利条件の探索
- 結果の可視化（2Dヒートマップ、感度分析グラフ）
- 計算結果のCSVエクスポート

## インストール

```bash
# リポジトリのクローン
git clone https://github.com/yourusername/stability-murayama-method.git
cd stability-murayama-method

# 依存パッケージのインストール
pip install -r requirements.txt
```

## 使用方法

### ローカル環境での実行

```bash
streamlit run app.py
```

ブラウザが自動的に開き、`http://localhost:8501`でアプリケーションにアクセスできます。

### Streamlit Cloudへのデプロイ

1. GitHubにリポジトリをプッシュ
2. [Streamlit Cloud](https://streamlit.io/cloud)にサインイン
3. 新しいアプリをデプロイ
4. リポジトリとブランチを選択
5. メインファイルパスに`app.py`を指定

## システム構成

- `app.py`: Streamlitアプリケーションのメインファイル
- `murayama_calculator.py`: 村山の式による計算処理モジュール
- `requirements.txt`: 必要なPythonパッケージのリスト
- `docs/`: プロジェクト設計書とモックアップ

## 入力パラメータ

### 地盤条件
- 切羽高さ H (m)
- 地山単位体積重量 γ (kN/m³)
- 地山内部摩擦角 φ (度)
- 地山粘着力 c (kN/m²)
- 上載荷重 q (kN/m²)（オプション）

### 解析パラメータ
- 初期半径 r₀ の範囲
- 角度 θ の範囲
- 計算点数

## 技術仕様

- Python 3.8以上
- Streamlit 1.29.0
- NumPy, SciPy（数値計算）
- Plotly（グラフ描画）

## ライセンス

MIT License

## 参考文献

- 村山朔郎：「トンネル切羽の安定性に関する研究」、土木学会論文集
- 土木学会：「トンネル標準示方書（山岳工法編）・同解説」