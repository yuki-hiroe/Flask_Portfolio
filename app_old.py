from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'my-secretkey'  # 本番環境では環境変数から取得


# データベース初期化
def init_db():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()

    # 管理者テーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')

    # 記事テーブル
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_published BOOLEAN DEFAULT 0
        )
    ''')

    # デフォルト管理者アカウント作成（username: admin, password: admin123）
    admin_exists = c.execute('SELECT COUNT(*) FROM admin').fetchone()[0]

    if admin_exists == 0:
        password_hash = generate_password_hash('admin123')
        c.execute('INSERT INTO admin (username, password_hash) VALUES (?, ?)',
                  ('admin', password_hash))
        print("デフォルト管理者アカウント (admin/admin123) を作成しました")

    conn.commit()
    conn.close()


# ルートURL - ログイン画面にリダイレクト
@app.route('/')
def index():
    if 'admin_logged_in' in session:
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))


# ログイン確認用デコレータ
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('ログインが必要です', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('blog.db')
        c = conn.cursor()
        admin = c.execute('SELECT * FROM admin WHERE username = ?', (username,)).fetchone()
        conn.close()

        if admin and check_password_hash(admin[2], password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('ログインしました', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('ユーザー名またはパスワードが間違っています', 'error')

    return render_template('login.html')


# ログアウト
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('ログアウトしました', 'success')
    return redirect(url_for('login'))


# デバッグ用：セッション状態確認（本番環境では削除してください）
@app.route('/debug/session')
def debug_session():
    return {
        'session_data': dict(session),
        'admin_logged_in': 'admin_logged_in' in session,
        'admin_username': session.get('admin_username', 'Not set')
    }


# テスト用ページ（本番環境では削除してください）
@app.route('/test')
@login_required
def test_page():
    return render_template('test_page.html')


# データベースリセット用（本番環境では削除してください）
@app.route('/reset-db')
def reset_db():
    import os
    if os.path.exists('blog.db'):
        os.remove('blog.db')
        print("既存のデータベースを削除しました")

    init_db()
    return "データベースをリセットしました。admin/admin123 でログインできます。"

# ===========================================
# フロントエンド（読者向け）ルート
# ===========================================

# ホームページ
@app.route('/home')
def home():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()

    # 公開記事を最新順で取得（最大5件）
    recent_posts = c.execute('''
         SELECT id, title, content, created_at
         FROM posts
         WHERE is_published = 1
         ORDER BY created_at DESC LIMIT 5
     ''').fetchall()

    # 記事の概要を作成（最初の150文字）
    posts_with_summary = []
    for post in recent_posts:
        summary = post[2][:150] + '...' if len(post[2]) > 150 else post[2]
        posts_with_summary.append({
            'id': post[0],
            'title': post[1],
            'content': post[2],
            'summary': summary,
            'created_at': post[3]
        })

    conn.close()
    return render_template('frontend/home.html', posts=posts_with_summary)


# 記事詳細ページ
@app.route('/post/<int:post_id>')
def post_detail(post_id):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()

    # 公開記事のみ取得
    post = c.execute('''
         SELECT id, title, content, created_at, updated_at
         FROM posts
         WHERE id = ? AND is_published = 1
     ''', (post_id,)).fetchone()

    if not post:
        conn.close()
        return render_template('frontend/404.html'), 404

    # 前後の記事を取得
    prev_post = c.execute('''
          SELECT id, title
          FROM posts
          WHERE id < ? AND is_published = 1
          ORDER BY id DESC LIMIT 1
    ''', (post_id,)).fetchone()

    next_post = c.execute('''
          SELECT id, title
          FROM posts
          WHERE id > ? AND is_published = 1
          ORDER BY id ASC LIMIT 1
      ''', (post_id,)).fetchone()

    conn.close()

    return render_template('frontend/post_detail.html',
                           post=post, prev_post=prev_post, next_post=next_post)


# 記事一覧ページ
@app.route('/posts')
def posts_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10  # 1ページあたりの記事数
    offset = (page - 1) * per_page

    conn = sqlite3.connect('blog.db')
    c = conn.cursor()

    # 総記事数を取得
    total_posts = c.execute('SELECT COUNT(*) FROM posts WHERE is_published = 1').fetchone()[0]

    # ページネーション用の記事取得
    posts = c.execute('''
          SELECT id, title, content, created_at
          FROM posts
          WHERE is_published = 1
          ORDER BY created_at DESC LIMIT ? OFFSET ?
      ''', (per_page, offset)).fetchall()

    # 記事の概要を作成
    posts_with_summary = []
    for post in posts:
        summary = post[2][:200] + '...' if len(post[2]) > 200 else post[2]
        posts_with_summary.append({
            'id': post[0],
            'title': post[1],
            'summary': summary,
            'created_at': post[3]
        })

    # ページネーション情報
    total_pages = (total_posts + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < total_pages

    conn.close()

    return render_template('frontend/posts_list.html',
                           posts=posts_with_summary,
                           page=page,
                           total_pages=total_pages,
                           has_prev=has_prev,
                           has_next=has_next)


# アバウトページ
@app.route('/about')
def about():
    return render_template('frontend/about.html')


# お問い合わせページ
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # ここで実際にはメール送信処理を行います
        # 今回はフラッシュメッセージで代用
        flash(f'{name}様、お問い合わせありがとうございました。', 'success')
        return redirect(url_for('contact'))

    return render_template('frontend/contact.html')

# ===========================================
# 管理者向けルート
# ===========================================

# 管理ダッシュボード
@app.route('/admin')
@login_required
def admin_dashboard():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()

    # 記事統計
    total_posts = c.execute('SELECT COUNT(*) FROM posts').fetchone()[0]
    published_posts = c.execute('SELECT COUNT(*) FROM posts WHERE is_published = 1').fetchone()[0]
    draft_posts = total_posts - published_posts

    # 最新記事5件
    recent_posts = c.execute('''
                             SELECT id, title, created_at, is_published
                             FROM posts
                             ORDER BY created_at DESC LIMIT 5
                             ''').fetchall()

    conn.close()

    return render_template('admin/dashboard.html',
                           total_posts=total_posts,
                           published_posts=published_posts,
                           draft_posts=draft_posts,
                           recent_posts=recent_posts)


# 記事管理一覧
@app.route('/admin/posts')
@login_required
def admin_posts():
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()

    posts = c.execute('''
                      SELECT id, title, created_at, is_published
                      FROM posts
                      ORDER BY created_at DESC
                      ''').fetchall()

    conn.close()
    return render_template('admin/posts.html', posts=posts)


# 記事作成
@app.route('/admin/post/new', methods=['GET', 'POST'])
@login_required
def admin_post_new():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        is_published = 'is_published' in request.form

        conn = sqlite3.connect('blog.db')
        c = conn.cursor()
        c.execute('''
                  INSERT INTO posts (title, content, is_published)
                  VALUES (?, ?, ?)
                  ''', (title, content, is_published))
        conn.commit()
        conn.close()

        flash('記事を作成しました', 'success')
        return redirect(url_for('admin_posts'))

    return render_template('admin/post_form.html', post=None, action='作成')


# 記事編集
@app.route('/admin/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_post_edit(post_id):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        is_published = 'is_published' in request.form

        c.execute('''
                  UPDATE posts
                  SET title        = ?,
                      content      = ?,
                      is_published = ?,
                      updated_at   = CURRENT_TIMESTAMP
                  WHERE id = ?
                  ''', (title, content, is_published, post_id))
        conn.commit()
        conn.close()

        flash('記事を更新しました', 'success')
        return redirect(url_for('admin_posts'))

    post = c.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()

    if not post:
        flash('記事が見つかりません', 'error')
        return redirect(url_for('admin_posts'))

    return render_template('admin/post_form.html', post=post, action='編集')


# 記事削除
@app.route('/admin/post/<int:post_id>/delete', methods=['POST'])
@login_required
def admin_post_delete(post_id):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()

    flash('記事を削除しました', 'success')
    return redirect(url_for('admin_posts'))


# 記事公開/非公開切り替え
@app.route('/admin/post/<int:post_id>/toggle', methods=['POST'])
@login_required
def admin_post_toggle(post_id):
    conn = sqlite3.connect('blog.db')
    c = conn.cursor()
    c.execute('''
              UPDATE posts
              SET is_published = NOT is_published,
                  updated_at   = CURRENT_TIMESTAMP
              WHERE id = ?
              ''', (post_id,))
    conn.commit()
    conn.close()

    flash('記事の公開状態を変更しました', 'success')
    return redirect(url_for('admin_posts'))


# パスワード変更ページ
@app.route('/admin/change-password', methods=['GET', 'POST'])
@login_required
def admin_change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # 新しいパスワードの確認
        if new_password != confirm_password:
            flash('新しいパスワードが一致しません', 'error')
            return render_template('admin/change_password.html')

        # パスワードの長さチェック
        if len(new_password) < 6:
            flash('新しいパスワードは6文字以上にしてください', 'error')
            return render_template('admin/change_password.html')

        # 現在のパスワード確認
        conn = sqlite3.connect('blog.db')
        c = conn.cursor()
        admin = c.execute('SELECT * FROM admin WHERE username = ?',
                          (session['admin_username'],)).fetchone()

        if admin and check_password_hash(admin[2], current_password):
            # パスワード更新
            new_password_hash = generate_password_hash(new_password)
            c.execute('UPDATE admin SET password_hash = ? WHERE username = ?',
                      (new_password_hash, session['admin_username']))
            conn.commit()
            conn.close()

            flash('パスワードを変更しました', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            conn.close()
            flash('現在のパスワードが間違っています', 'error')

    return render_template('admin/change_password.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)