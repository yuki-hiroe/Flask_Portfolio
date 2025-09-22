ブログアプリ セットアップガイド
プロジェクト構造
blog-app/
│
├── app.py                  # メインアプリケーションファイル
├── blog.db                 # SQLiteデータベース（自動生成）
│
└── templates/
    ├── login.html          # ログインページ
    └── admin/
        ├── base.html       # 管理画面ベーステンプレート
        ├── dashboard.html  # ダッシュボード
        ├── posts.html      # 記事一覧
        └── post_form.html  # 記事作成・編集フォーム
セットアップ手順
1. 必要なパッケージのインストール
bashpip install flask
2. ファイルの配置

app.py をプロジェクトのルートディレクトリに配置
templates/ フォルダを作成し、各HTMLファイルを配置

templates/login.html
templates/admin/base.html
templates/admin/dashboard.html
templates/admin/posts.html
templates/admin/post_form.html



3. アプリケーションの起動
bashpython app.py
アプリケーションは http://127.0.0.1:5000 で起動します。
4. 初回ログイン

URL: http://127.0.0.1:5000/login
ユーザー名: admin
パスワード: admin123

主な機能
管理画面

ダッシュボード (/admin)

記事統計の表示
最新記事一覧
クイックアクション


記事管理 (/admin/posts)

全記事の一覧表示
公開/非公開の切り替え
記事の編集・削除


記事作成 (/admin/post/new)

新規記事の作成
タイトルと本文の入力
公開/下書き選択


記事編集 (/admin/post/<id>/edit)

既存記事の編集
公開状態の変更
記事削除機能



セキュリティ機能

セッションベースの認証
ログイン必須の管理画面
パスワードハッシュ化（Werkzeug使用）

データベース構造
admin テーブル

id: 管理者ID（主キー）
username: ユーザー名
password_hash: パスワードハッシュ

posts テーブル

id: 記事ID（主キー）
title: 記事タイトル
content: 記事本文
created_at: 作成日時
updated_at: 更新日時
is_published: 公開状態（0: 下書き, 1: 公開）

カスタマイズのポイント
デザイン

Bootstrap 5を使用したレスポンシブデザイン
Font Awesomeアイコン使用
CSS変数で色調整可能

セキュリティ

app.secret_key を本番環境では環境変数に変更
必要に応じてCSRF対策の追加

機能拡張

記事カテゴリー機能
画像アップロード機能
SEO対策（メタタグ等）
コメント機能

注意事項

本番環境では必ず app.secret_key を変更してください
SQLiteは開発用途に適しています。本番環境ではPostgreSQLやMySQLの使用を推奨
定期的なデータベースバックアップを推奨

次のステップ
管理画面が完成したら、次はフロントエンド（読者向けページ）の実装に進みます：

ホームページ（記事一覧）
記事詳細ページ
アバウトページ
お問い合わせページ