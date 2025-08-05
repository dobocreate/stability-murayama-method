# 推奨コマンド

## 開発・実行コマンド

### アプリケーション実行
```bash
streamlit run app.py
```

### 依存関係インストール
```bash
pip install -r requirements.txt
```

### テスト実行
```bash
python test_calculator_revised.py
python test_safety_factor_debug.py
python test_safety_factor_debug2.py
python test_safety_factor_debug3.py
```

### Git操作
```bash
git status
git add .
git commit -m "commit message"
git push
```

## 有用なシステムコマンド（Linux/WSL2）
```bash
ls -la          # ファイル一覧表示
pwd             # 現在のディレクトリ
cd <path>       # ディレクトリ移動
grep <pattern> <file>  # テキスト検索
find . -name "*.py"    # ファイル検索
```

## デバッグ・解析コマンド
```bash
python -c "from murayama_calculator_revised import MurayamaCalculatorRevised; print('Import OK')"
```