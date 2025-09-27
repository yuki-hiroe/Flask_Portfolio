📝 My Blog
転職活動用の個人ブログアプリケーションです。Python/Flask + Bootstrap で構築された、シンプルで使いやすいブログシステムです。

✨ 特徴
📱 レスポンシブデザイン - モバイル・デスクトップ両対応
🔐 管理機能 - 記事の作成・編集・削除
⚡ 軽量・高速 - SQLite使用でセットアップが簡単
🎨 モダンUI - Bootstrap 5 + カスタムCSS
🔧 技術スタック
バックエンド
Python 3.8+
Flask - Webフレームワーク
SQLAlchemy - ORM
SQLite - データベース
フロントエンド
HTML5 / CSS3
JavaScript (ES6+)
Bootstrap 5 - UIフレームワーク
Font Awesome - アイコン
🚀 クイックスタート
必要な環境
Python 3.8以上
pip (パッケージマネージャー)
インストール
リポジトリのクローン
bash
   git clone https://github.com/yuki-hiroe/Flask_Portlolio.git
   cd Flask_Portlolio
仮想環境の作成
bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
依存関係のインストール
bash
   pip install -r requirements.txt
アプリケーションの起動
bash
   python app.py
ブラウザでアクセス
フロントエンド: https://portfolio-yuki-2025-dfce81f5cdc4.herokuapp.com/home
管理画面: https://portfolio-yuki-2025-dfce81f5cdc4.herokuapp.com/login
デフォルトログイン情報
ユーザー名: admin
パスワード: admin123
📁 プロジェクト構造
Flask_Portfolio/
├── app.py                      # メインアプリケーション
├── requirements.txt            # 依存関係
├── instance/
│   ├── blog.db                 # SQLiteデータベース
├── static/                     # 静的ファイル
│   ├── css/
│   │   ├── about.cs
│   │   └── base_style.css
│   └── js/
│       ├── 404.js 
│       ├── about.js
│       ├── change_password.js
│       ├── post_detail.js
│       ├── post_form.js # 記事フォーム用JS
│       ├── posts.js
│       └── posts_list.js
└── templates/                  # HTMLテンプレート
    ├── login.html
    ├── admin/                  # 管理画面
    │   ├── base.html
    │   ├── dashboard.html
    │   ├── posts.html
    │   ├── post_form.html
    │   └── change_password.html
    └── frontend/               # フロントエンド
        ├── base.html
        ├── home.html
        ├── post_detail.html
        ├── posts_list.html
        ├── about.html
        └── 404.html
📖 使い方
管理者として
ログイン: /login にアクセスしてログイン
記事作成: ダッシュボードから「新規記事」をクリック
記事管理: 記事の編集・削除・公開状態の切り替え
パスワード変更: 管理画面からパスワードを変更
読者として
記事閲覧: ホームページで最新記事を確認
記事一覧: /posts で全記事を確認
プロフィール: /about で詳細なプロフィールを確認
お問い合わせ: /contact で連絡フォームを利用
⚙️ 設定
環境変数（推奨）
.env ファイルを作成して設定：

env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///blog.db
データベースの初期化
bash
python -c "from app import init_db; init_db()"
本番環境での設定
python
# app.py
import os

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
🎨 カスタマイズ
プロフィール情報の変更
templates/frontend/home.html - ホームページのプロフィール
templates/frontend/about.html - 詳細プロフィール
デザインの調整
templates/frontend/base.html の CSS変数を編集
Bootstrap クラスを変更してレイアウト調整
機能の拡張
画像アップロード: Flask-Uploadsを追加
コメント機能: Comment モデルを追加
カテゴリー機能: Category モデルを追加
📝 API（将来的な拡張）
REST APIを追加する場合の例：

python
@app.route('/api/posts', methods=['GET'])
def api_posts():
    posts = Post.query.filter_by(is_published=True).all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at.isoformat()
    } for post in posts])
🧪 テスト
bash
# テストの実行
python -m pytest tests/

# カバレッジレポート
pytest --cov=app tests/
🚢 デプロイ
Heroku にデプロイ
Procfile を作成
   web: python app.py
requirements.txt を更新
bash
   pip freeze > requirements.txt
Heroku CLI でデプロイ
bash
   heroku create your-blog-name
   git push heroku main
Docker を使用
dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
🤝 貢献
このリポジトリをフォーク
機能ブランチを作成 (git checkout -b feature/amazing-feature)
変更をコミット (git commit -m 'Add amazing feature')
ブランチをプッシュ (git push origin feature/amazing-feature)
プルリクエストを作成

👨‍💻 作者
Yuki Hiroe

GitHub: @yuki-hiroe
Email: yuhiro0331@gmail.com

📚 参考資料
Flask公式ドキュメント
SQLAlchemy公式ドキュメント
Bootstrap公式ドキュメント

