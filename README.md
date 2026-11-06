# app-app

システム部門研修で作成した TODO アプリです。

## 概要

Python と FastAPI を使用したバックエンドと、HTML / JavaScript によるフロントエンドで構成されています。データの保存には SQLite を使用しています。

このアプリケーションでは、TODO の追加・一覧表示・完了状態の切り替え・削除ができます。

## 主な機能

- TODO 一覧表示
- TODO 追加
- TODO 完了状態の切り替え
- TODO 削除
- SQLite によるデータ永続化
- タイトルのバリデーション
- pytest による API 結合テスト

## 使用技術

# 言語

Python

# バックエンド

FastAPI

# データベース

SQLite

# データモデル・バリデーション

Pydantic

# フロントエンド

HTML / JavaScript

# テスト

pytest

# パッケージ管理

uv

## ディレクトリ構成
app-app
├── README.md
├── main.py
├── practice
│   ├── db.py
│   ├── fetch-example.py
│   ├── index.py
│   ├── test_validate.py
│   ├── test_validate_test.py
│   ├── todo.py
│   └── validate.test.py
├── public
│   └── index.html
├── src
│   ├── application
│   │   └── todo
│   │       └── service.py
│   ├── domain
│   │   └── todo
│   │       ├── test_validate.py
│   │       ├── types.py
│   │       └── validate.py
│   ├── infrastructure
│   │   └── todo
│   │       └── repository.py
│   ├── presentation
│   │   └── server.py
│   └── test_api.py
└── todo.db
(.gitignore や.envなどの仮想環境（.venv）やキャッシュ（__pycache__）、Gitの隠しフォルダが存在)

## セットアップ方法

1. 必要な環境

Python 3.11 以上

uv

WSL (Ubuntu) または Linux / macOS 環境

2. リポジトリのクローン

git clone https://github.com/sora-takochu/app-app.git
cd app-app

3. 依存関係のインストール

uv sync

uv sync によって仮想環境 .venv が作成され、必要なライブラリがインストールされます。

アプリケーションの起動

以下のコマンドで開発サーバーを起動します。

uv run fastapi dev main.py

起動後、ブラウザで以下にアクセスします。

アプリケーション：http://127.0.0.1:8000

APIドキュメント：http://127.0.0.1:8000/docs

## APIの動作確認方法

APIの動作確認は、FastAPIに標準搭載されている「Swagger UI」を使った手動テストと、`pytest`を用いた自動テストの2種類で行えます。

### 1. 手動テスト（Swagger UI）
ブラウザの画面上から直接APIを呼び出し、データベースの更新や結果の確認ができます。

1. サーバーを起動します（`fastapi dev main.py`）。
2. ブラウザで [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) にアクセスします。
3. 画面に表示される `GET` `POST` `PUT` `DELETE` の各項目を展開します。
4. **「Try it out」**ボタンを押し、必要なデータ（JSONなど）を入力して**「Execute」**をクリックするとテストが実行されます。

### 2. 自動テスト（pytest）
あらかじめ作成したテストコード（`src/test_api.py`）を使用し、一連のCRUD処理（作成・読み込み・更新・削除）とバリデーション機能が正しく動くかを一括で検証します。

**実行手順:**
1. ターミナル1で、開発サーバーを起動しておきます。
   ```bash
   fastapi dev main.py
   ```
2. ターミナル2（新しい画面）を開き、仮想環境を有効化します。
   ```bash
   source .venv/bin/activate
   ```
3. 以下のコマンドでテストを実行します。
   ```bash
   pytest -v src/test_api.py
   ```

## 自動テスト（pytest）

では、Pythonのテストフレームワーク `pytest` とHTTP通信ライブラリ `requests` を使用して、APIの自動テストを実装しています。

### 実行条件
テストコード（`src/test_api.py`）はローカルのAPIサーバー（`http://127.0.0.1:8000`）へ実際に通信を行って検証するため、**開発サーバーを起動した状態**で実行する必要があります。

### 実行コマンド
```bash
# 仮想環境を有効化
source .venv/bin/activate

# 詳細モード(-v)でテストを実行
pytest -v src/test_api.py
```
## コードの整形と静的解析 (Linter / Formatter)

コードの品質と一貫性を保つためにLinter兼Formatterである **[Ruff](https://docs.astral.sh/ruff/)** を導入しています。

### 実行コマンド
仮想環境を有効化した状態で、以下のコマンドを実行します。

```bash
# 1. コードの自動整形（インデントや改行のルールを綺麗に揃える）
ruff format .

# 2. 静的解析と自動修正（未使用の変数や不要なインポートなどを検知・修正）
ruff check . --fix
```
### 開発環境

# パッケージ管理

Pythonのパッケージ管理には uv を使用しています。

・pyproject.toml：プロジェクト情報と依存ライブラリの定義
・uv.lock：依存ライブラリのバージョン固定

# Git管理

以下のファイルやディレクトリは Git の管理対象から除外しています。

・.venv/：仮想環境
・__pycache__/：Pythonのキャッシュ
・*.pyc：Pythonのコンパイル済みファイル
・.env：環境変数ファイル