---
name: pep8
description: 'PEP8に沿ってPythonコードを実装・修正する。Use when: Pythonコードを新規実装するとき、既存コードをPEP8準拠に修正するとき、flake8/pylintエラーを解消するとき、コードスタイルレビュー前の整形を行うとき。'
argument-hint: '対象ファイルまたはディレクトリのパス（例: app.py, tests/）'
---

# PEP8実装スキル

## このスキルが行うこと

Pythonコードを[PEP8](https://peps.python.org/pep-0008/)スタイルガイドに準拠した形で実装・修正する。

---

## 手順

### 1. 対象ファイルの確認

引数でファイルまたはディレクトリが指定された場合はそれを対象にする。指定がない場合はワークスペースの `*.py` ファイルをすべて対象にする。

### 2. autopep8による自動整形（Dockerコンテナ内）

まず自動整形できる違反を一括修正する。

```bash
docker compose exec app autopep8 --in-place --aggressive --max-line-length 79 <対象パス>
```

> `autopep8` が未インストールの場合は `requirements.txt` に追加してイメージを再ビルドする:
> ```
> autopep8
> ```
> ```bash
> docker compose build
> ```

### 3. flake8による静的チェック（Dockerコンテナ内）

自動整形で直せなかった残りの違反を確認する。

```bash
docker compose exec app flake8 <対象パス>
```

エラーコードの主な意味:

| コード | 内容 |
|--------|------|
| E1xx | インデント |
| E2xx | 空白 |
| E3xx | 空行 |
| E4xx | import |
| E5xx | 行の長さ |
| E7xx | 文・式 |
| W6xx | 非推奨 |
| F4xx | 未使用import／未定義名 |

### 4. 残存違反の手動修正

flake8のエラーコードを参考に、自動整形では直せなかった箇所を手動修正する。

#### インデント・行長
- インデントは **スペース4つ**（タブ禁止）
- 1行の最大文字数は **79文字**（コメントは72文字）
- 長い行は `\` または括弧で折り返す

#### 空行
- トップレベルの関数・クラス定義の前後に **2行**の空行
- クラス内メソッドの前後に **1行**の空行
- 関数内の論理的なセクション区切りに空行1行（過剰使用は避ける）

#### import
- 標準ライブラリ → サードパーティ → ローカル の順にグループ分け
- グループ間に1行空行
- `import` は1行1モジュール（`from x import a, b` はOK）
- ワイルドカードimport（`from x import *`）は禁止

```python
# Good
import os
import sys

import flask

from myapp import utils
```

#### 命名規則

| 対象 | スタイル | 例 |
|------|----------|----|
| 変数・関数 | snake_case | `get_user_name()` |
| クラス | PascalCase | `UserProfile` |
| 定数 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| プライベート | 先頭アンダースコア | `_internal_val` |

#### 空白
- 演算子の前後にスペース1つ（`=` のデフォルト引数は除く）
- `,` `:` `;` の後にスペース1つ、前にはスペースなし
- 括弧の内側にスペースを入れない

```python
# Good
x = 1 + 2
def func(a, b=0):
    return a, b

# Bad
x=1+2
def func( a , b = 0 ) :
```

#### コメント・docstring
- コメントとdocstringは必ず日本語で書くこと
- インラインコメントは `# ` + スペース2つ以上でコードと区切る
- 公開関数・クラスには必ずdocstringを付ける
- docstringは `"""` で開始・終了

### 5. 修正後の再チェック

```bash
docker compose exec app flake8 <対象パス>
```

エラー0件になるまで繰り返す。

### 6. テストの実行（回帰確認）

```bash
docker compose exec app pytest
```

既存テストがすべてPassすることを確認する。

---

## 完了条件

- [ ] `flake8` の出力がエラー0件
- [ ] 既存テストがすべてPass
- [ ] 意図しないロジック変更がない

---

## 参考

- [PEP8 公式](https://peps.python.org/pep-0008/)
- [flake8 ドキュメント](https://flake8.pycqa.org/)
