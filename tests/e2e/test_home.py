"""
このテストモジュールでは、Flaskアプリケーションのホームページが正しく表示されることをエンドツーエンドでテストします。
"""

import os

from playwright.sync_api import sync_playwright


def test_home_page_renders() -> None:
    """
    ホームページが正しく表示されることをエンドツーエンドでテストする。
    このテストでは、Playwright を使用してブラウザを起動し、ホームページにアクセスして内容を検証します。
    """
    # 環境変数からベースURLを取得（デフォルトはローカルホスト）
    base_url = os.getenv("BASE_URL", "http://127.0.0.1:5000")

    # Playwright を使用してブラウザを起動し、ホームページにアクセス
    with sync_playwright() as playwright:
        # Chromium ブラウザを起動
        browser = playwright.chromium.launch()

        # 新しいページを開いてホームページにアクセス
        page = browser.new_page()
        page.goto(base_url, wait_until="networkidle")

        # ホームページの内容を検証
        assert page.locator("h1").text_content() == "Flask Container Ready"
        assert "pytest と Playwright" in page.locator("body").text_content()

        # ブラウザを閉じる
        browser.close()
