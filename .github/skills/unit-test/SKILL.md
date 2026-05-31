---
name: unit-test
description: 'メソッド実装後に単体テストを作成する。Use when: 新しいメソッド・関数を実装したとき、単体テストを追加するとき、コードカバレッジ100%を達成したいとき、境界値テストやNoneテストを網羅したいとき。テストはtests/unitフォルダに作成する。'
argument-hint: 'テスト対象のファイルまたはメソッド名（例: app.py, utils.py::calculate）'
---

# 単体テスト作成スキル

## このスキルが行うこと

メソッド・関数の実装後に、**コードカバレッジ100%** を目標とした単体テストを `tests/unit/` フォルダに作成する。
境界値分割とNoneパターンを必ず網羅する。

---

## 手順

### 1. 対象メソッドの確認

テスト対象のメソッド・関数を読み込み、以下を把握する。

- 引数の型・取りうる値の範囲
- 戻り値・副作用
- 例外を送出するケース
- 依存する外部モジュール（モック対象）

### 2. テストケースの設計

下記の分類で必ずテストケースを列挙する。

#### 正常系
- 典型的な入力で期待値が返ること

#### 境界値分割
数値・文字列・リストなどに対して境界を特定し、以下を必ずテストする。

| 境界の種類 | テストすべき値 |
|-----------|--------------|
| 数値の最小値 | 最小値 - 1 / 最小値 / 最小値 + 1 |
| 数値の最大値 | 最大値 - 1 / 最大値 / 最大値 + 1 |
| 空文字列 | `""` |
| 空リスト | `[]` |
| 要素数0/1/最大 | 各境界値 |

#### Noneパターン（必須）
各引数に対して `None` を渡したときの挙動を必ずテストする。
- `None` を受け入れる場合 → 期待の戻り値を検証
- `None` を受け入れない場合 → 例外（`TypeError` / `ValueError` 等）の送出を検証

#### 異常系
- 不正な型・範囲外の値
- 例外が正しく送出されること（`pytest.raises` を使用）

### 3. テストファイルの作成

#### ファイル配置ルール

```
tests/
└── unit/
    └── test_<対象モジュール名>.py
```

例: `app.py` のテスト → `tests/unit/test_app.py`

#### ファイルの雛形

```python
"""<対象モジュール> の単体テスト"""
import pytest
from <対象モジュール> import <対象クラス・関数>


class Test<メソッド名>:
    """<メソッド名> のテストクラス"""

    # --- 正常系 ---
    def test_<メソッド名>_正常系(self):
        """典型的な入力で正しい値が返ること"""
        assert <対象関数>(引数) == 期待値

    # --- 境界値 ---
    def test_<メソッド名>_境界値_最小値(self):
        assert <対象関数>(最小値) == 期待値

    def test_<メソッド名>_境界値_最小値未満(self):
        with pytest.raises(ValueError):
            <対象関数>(最小値 - 1)

    def test_<メソッド名>_境界値_最大値(self):
        assert <対象関数>(最大値) == 期待値

    def test_<メソッド名>_境界値_最大値超過(self):
        with pytest.raises(ValueError):
            <対象関数>(最大値 + 1)

    # --- Noneパターン ---
    def test_<メソッド名>_None(self):
        with pytest.raises(TypeError):
            <対象関数>(None)

    # --- 異常系 ---
    def test_<メソッド名>_不正な型(self):
        with pytest.raises(TypeError):
            <対象関数>("invalid")
```

#### コーディングルール
- テストクラスは `Test<対象メソッド名>` の命名（PascalCase）
- テストメソッドは `test_<メソッド名>_<ケース説明>` の命名（snake_case）
- 各テストメソッドに日本語docstringを付ける
- `pytest.raises` でコンテキストマネージャを使って例外を検証する
- モックが必要な場合は `unittest.mock.patch` または `pytest-mock` を使用する

### 4. テストの実行とカバレッジ確認

```bash
docker compose exec app pytest tests/unit/ --cov=<対象モジュール> --cov-report=term-missing
```

カバレッジレポートの見方:

| 表示 | 意味 |
|------|------|
| `100%` | 全行・全分岐をカバー済み |
| `Missing: 15, 20` | 15行目・20行目が未テスト |

> `pytest-cov` が未インストールの場合は `requirements.txt` に追加してイメージを再ビルドする:
> ```
> pytest-cov
> ```
> ```bash
> docker compose build
> ```

### 5. カバレッジ100%になるまで補完

`Missing` に表示された行に対応するテストケースを追加し、再実行する。
カバレッジが100%になるまで繰り返す。

### 6. PEP8チェック

```bash
docker compose exec app flake8 tests/unit/
```

エラー0件になるまで修正する。

---

## 完了条件

- [ ] `tests/unit/test_<モジュール名>.py` が作成されている
- [ ] 境界値分割のテストケースが網羅されている
- [ ] 全引数の `None` パターンがテストされている
- [ ] `pytest --cov` のカバレッジが **100%**
- [ ] `flake8 tests/unit/` がエラー0件

---

## 参考

- [pytest 公式](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [unittest.mock](https://docs.python.org/ja/3/library/unittest.mock.html)
