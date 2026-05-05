---
name: docker-compose-in-container
description: Docker Composeアプリケーションの起動・開発・テストを必ずDockerコンテナ内で実行する。ホストOSで直接python/pytest/flaskを実行しない運用を徹底したいときに使用。
argument-hint: "[run|test|shell]"
---

# Docker Compose In-Container Workflow

## このスキルが行うこと

Docker Compose を使うプロジェクトで、アプリ実行やテスト実行を常にコンテナ内で行う運用を徹底します。

このスキルはこのリポジトリ専用です。別リポジトリへはそのまま流用せず、`compose.yaml` のサービス名に合わせて調整します。

## 使うタイミング

- Docker Compose でアプリを起動したいとき
- `pytest` などのテストを実行したいとき
- 「ローカルで直接実行」ではなく「コンテナ内実行」を強制したいとき

## 基本ルール

- `python app.py` / `flask run` / `pytest` をホストで直接実行しない
- 実行は `docker compose up` / `docker compose exec` / `docker compose run` を使う
- サービス名は `compose.yaml` を参照する（このリポジトリの主サービスは `web`、テスト用は `test`）

## 実行フロー

1. `compose.yaml` の `services` を確認し、対象サービスを決める
2. まだ起動していなければ `docker compose up -d web` でアプリコンテナを起動する
3. 目的に応じてコマンドを分岐する
4. 実行結果とコンテナ状態を確認する

## 分岐ルール

### 1) アプリを動かす

- 常駐起動: `docker compose up -d web`
- ログ確認: `docker compose logs -f web`
- 動作確認: `http://localhost:5000` と `http://localhost:5000/health`

### 2) テストを実行する

- E2E を含む標準実行: `docker compose --profile test run --rm test`
- 起動済み `web` に対して単発実行したい場合: `docker compose exec web pytest`

### 3) コンテナ内で手動調査する

- シェルに入る: `docker compose exec web sh`
- その中で `python` や `pytest` を実行する

## 完了条件

- 目的の操作（起動・テスト・調査）が Docker コンテナ内で完了している
- ホスト側で直接 `python` / `pytest` / `flask` を実行していない
- 必要に応じて `docker compose ps` でサービス状態を確認している

## 失敗時チェック

1. `docker compose ps` でサービスの状態を確認
2. `docker compose logs web` でエラー原因を確認
3. 必要なら `docker compose down` 後に `docker compose up -d --build web` を実行
4. テスト系は `--profile test` の付け忘れを確認
