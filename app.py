from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'my-secretkey'  # 本番環境では環境変数から取得

# SQLAlchemy設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ===========================================
# データベースモデル
# ===========================================

class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Admin {self.username}>'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)

    def get_summary(self, length=150):
        return self.content[:length] + '...' if len(self.content) > length else self.content

    def __repr__(self):
        return f'<Post {self.title}>'


# ===========================================
# データベース初期化
# ===========================================

def init_db():
    with app.app_context():
        # テーブル作成
        db.create_all()

        # デフォルト管理者アカウント作成
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("デフォルト管理者アカウント (admin/admin123) を作成しました")


# ===========================================
# ヘルパー関数
# ===========================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('ログインが必要です', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


# ===========================================
# 認証ルート
# ===========================================

@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('ログインしました', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('ユーザー名またはパスワードが間違っています', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('ログアウトしました', 'success')
    return redirect(url_for('login'))


# ===========================================
# フロントエンド（読者向け）ルート
# ===========================================

@app.route('/home')
def home():
    # 公開記事を最新順で取得（最大5件）
    recent_posts = Post.query.filter_by(is_published=True) \
        .order_by(Post.created_at.desc()) \
        .limit(5) \
        .all()

    # 記事の概要を作成
    posts_with_summary = []
    for post in recent_posts:
        posts_with_summary.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'summary': post.get_summary(),
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return render_template('frontend/home.html', posts=posts_with_summary)


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    # 公開記事のみ取得
    post = Post.query.filter_by(id=post_id, is_published=True).first()

    if not post:
        return render_template('frontend/404.html'), 404

    # 前後の記事を取得
    prev_post = Post.query.filter(
        Post.id < post_id,
        Post.is_published == True
    ).order_by(Post.id.desc()).first()

    next_post = Post.query.filter(
        Post.id > post_id,
        Post.is_published == True
    ).order_by(Post.id.asc()).first()

    # タプル形式に変換（テンプレートとの互換性のため）
    post_tuple = (
        post.id,
        post.title,
        post.content,
        post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        post.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    )

    prev_tuple = (prev_post.id, prev_post.title) if prev_post else None
    next_tuple = (next_post.id, next_post.title) if next_post else None

    return render_template('frontend/post_detail.html',
                           post=post_tuple,
                           prev_post=prev_tuple,
                           next_post=next_tuple)


@app.route('/posts')
def posts_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # ページネーション
    pagination = Post.query.filter_by(is_published=True) \
        .order_by(Post.created_at.desc()) \
        .paginate(page=page, per_page=per_page, error_out=False)

    posts = pagination.items

    # 記事の概要を作成
    posts_with_summary = []
    for post in posts:
        posts_with_summary.append({
            'id': post.id,
            'title': post.title,
            'summary': post.get_summary(200),
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })

    return render_template('frontend/posts_list.html',
                           posts=posts_with_summary,
                           page=page,
                           total_pages=pagination.pages,
                           has_prev=pagination.has_prev,
                           has_next=pagination.has_next)


@app.route('/about')
def about():
    return render_template('frontend/about.html')


# ===========================================
# 管理者向けルート
# ===========================================

@app.route('/admin')
@login_required
def admin_dashboard():
    # 記事統計
    total_posts = Post.query.count()
    published_posts = Post.query.filter_by(is_published=True).count()
    draft_posts = total_posts - published_posts

    # 最新記事5件
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    # タプル形式に変換
    recent_posts_tuple = [
        (post.id, post.title, post.created_at.strftime('%Y-%m-%d %H:%M:%S'), post.is_published)
        for post in recent_posts
    ]

    return render_template('admin/dashboard.html',
                           total_posts=total_posts,
                           published_posts=published_posts,
                           draft_posts=draft_posts,
                           recent_posts=recent_posts_tuple)


@app.route('/admin/posts')
@login_required
def admin_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()

    # タプル形式に変換
    posts_tuple = [
        (post.id, post.title, post.created_at.strftime('%Y-%m-%d %H:%M:%S'), post.is_published)
        for post in posts
    ]

    return render_template('admin/posts.html', posts=posts_tuple)


@app.route('/admin/post/new', methods=['GET', 'POST'])
@login_required
def admin_post_new():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        is_published = 'is_published' in request.form

        post = Post(
            title=title,
            content=content,
            is_published=is_published
        )

        db.session.add(post)
        db.session.commit()

        flash('記事を作成しました', 'success')
        return redirect(url_for('admin_posts'))

    return render_template('admin/post_form.html', post=None, action='作成')


@app.route('/admin/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_post_edit(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.is_published = 'is_published' in request.form
        post.updated_at = datetime.utcnow()

        db.session.commit()

        flash('記事を更新しました', 'success')
        return redirect(url_for('admin_posts'))

    # タプル形式に変換
    post_tuple = (
        post.id,
        post.title,
        post.content,
        post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        post.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        post.is_published
    )

    return render_template('admin/post_form.html', post=post_tuple, action='編集')


@app.route('/admin/post/<int:post_id>/delete', methods=['POST'])
@login_required
def admin_post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    flash('記事を削除しました', 'success')
    return redirect(url_for('admin_posts'))


@app.route('/admin/post/<int:post_id>/toggle', methods=['POST'])
@login_required
def admin_post_toggle(post_id):
    post = Post.query.get_or_404(post_id)
    post.is_published = not post.is_published
    post.updated_at = datetime.utcnow()

    db.session.commit()

    flash('記事の公開状態を変更しました', 'success')
    return redirect(url_for('admin_posts'))


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
        admin = Admin.query.filter_by(username=session['admin_username']).first()

        if admin and admin.check_password(current_password):
            # パスワード更新
            admin.set_password(new_password)
            db.session.commit()

            flash('パスワードを変更しました', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('現在のパスワードが間違っています', 'error')

    return render_template('admin/change_password.html')


# ===========================================
# デバッグ・テスト用ルート（本番では削除）
# ===========================================

@app.route('/debug/session')
def debug_session():
    return {
        'session_data': dict(session),
        'admin_logged_in': 'admin_logged_in' in session,
        'admin_username': session.get('admin_username', 'Not set')
    }


@app.route('/test')
@login_required
def test_page():
    return render_template('test_page.html')


@app.route('/reset-db')
def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # デフォルト管理者再作成
        admin = Admin(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

        return "データベースをリセットしました。admin/admin123 でログインできます。"


if __name__ == '__main__':
    init_db()
    app.run(debug=True)