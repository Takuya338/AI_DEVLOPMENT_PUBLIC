# Flask2 サンプルシステム

Flask + Docker を使ったサンプルアプリです。pytest（ユニットテスト）と Playwright（E2E テスト）によるテストが実行できます。

## 技術スタック

| 技術 | バージョン |
|------|-----------|
| Flask | 3.1.0 |
| pytest | 8.3.5 |
| Playwright | 1.51.0 |
| Python ベースイメージ | mcr.microsoft.com/playwright/python:v1.51.0-noble |

## ディレクトリ構成

```
.
├── app.py               # Flask アプリ本体
├── compose.yaml         # Docker Compose 設定
├── Dockerfile           # コンテナ定義
├── requirements.txt     # Python 依存パッケージ
├── pytest.ini           # pytest 設定
├── templates/
│   └── index.html       # ホーム画面テンプレート
└── tests/
    ├── test_app.py      # ユニットテスト
    └── e2e/
        └── test_home.py # E2E テスト（Playwright）
```

## エンドポイント

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/` | ホーム画面 |
| GET | `/health` | ヘルスチェック (`{"status": "ok"}`) |

## 使い方

### アプリの起動

```bash
docker compose up
```

ブラウザで http://localhost:5000 にアクセス。

### ユニットテスト + E2E テストの実行

```bash
docker compose --profile test run --rm test
```

`web` サービスが起動してヘルスチェックが通ってから `pytest` が実行されます。

### コンテナの停止・削除

```bash
docker compose down
```
