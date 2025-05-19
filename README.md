# Melete Species Generator

## 構成

- **requirements.txt** — 必要な Python パッケージを記載しています。
- **spegen パッケージ**
  - `app.py` — Streamlit アプリ本体。ランダムに環境を生成し、候補種族を表示します。
  - `core.py` — 互換性マスク計算やスコアリングなど主要なロジックを提供します。
  - `data.py` — 環境パラメータと能力の日本語表記を定義します。
  - `template.py` — 種族説明文のテンプレート処理を行います。
  - `compatibility.yaml` — 能力と環境の相性を数値で定義したデータファイルです。
  - `__main__.py` — コマンドラインから種族生成を行うためのインターフェースです。

## 実行方法

### 依存関係のインストール
```bash
pip install -r requirements.txt
```

### Streamlit アプリを起動する
```bash
streamlit run spegen/app.py
```
ブラウザが開き、ランダムな環境と候補種族が最大 10 件表示されます。

### CLI で利用する
```bash
python -m spegen --env KEY=VALUE --top 5
```
`--markdown` を付けると Markdown 形式で出力されます。

### LLM を利用した詳細な種族生成
`.env` ファイルに `OPENAI_API_KEY=your-key` を記載してください。
```bash
python -m spegen.llm --env KEY=VALUE --abilities "能力説明"
```
OpenAI API を使って環境と能力の概要からより詳細な種族案を生成します。
