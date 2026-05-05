"""
ホームページとヘルスチェックエンドポイントを提供するシンプルな Flask アプリケーション。
"""

from flask import Flask, render_template


def create_app() -> Flask:
    """
    Flask アプリケーションを作成するファクトリ関数。
    この関数は、Flask アプリケーションのインスタンスを作成し、ルートとエンドポイントを定義します。
    """

    # Flask アプリケーションのインスタンスを作成
    app = Flask(__name__)

    @app.get("/")
    def home() -> str:
        """
        ホームページを表示する。
        このエンドポイントは、`index.html` テンプレートをレンダリングしてホームページを表示します。
        """
        return render_template("index.html")

    @app.get("/health")
    def health() -> dict[str, str]:
        """
        ヘルスチェックエンドポイント。
        このエンドポイントは、アプリケーションの健康状態を確認するために使用されます。
        """
        return {"status": "ok"}

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
