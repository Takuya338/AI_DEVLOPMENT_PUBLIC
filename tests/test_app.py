"""
このテストモジュールでは、Flaskアプリケーションのホームページとヘルスチェックエンドポイントのテストを行います。
"""
from app import create_app


def test_home_page() -> None:
    """
    ホームページが正しく表示されることをテストする。
    このテストでは、Flaskのテストクライアントを使用してホームページにアクセスし、ステータスコードと内容を検証します。
    """
    # アプリケーションを作成し、テストクライアントを取得
    app = create_app()
    client = app.test_client()

    # ホームページにアクセス
    response = client.get("/")

    # ステータスコードが200であることを確認
    assert response.status_code == 200
    assert "Flask Container Ready" in response.get_data(as_text=True)


def test_health_check() -> None:
    """
    ヘルスチェックエンドポイントが正しく機能することをテストする。
    このテストでは、Flaskのテストクライアントを使用してヘルスチェックエンドポイントにアクセスし、ステータスコードと内容を検証します。
    """
    # アプリケーションを作成し、テストクライアントを取得
    app = create_app()
    client = app.test_client()

    # ヘルスチェックエンドポイントにアクセス
    response = client.get("/health")

    # ステータスコードが200であることを確認
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
