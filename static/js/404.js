// 検索機能
function searchPosts() {
    const searchTerm = document.getElementById('searchInput').value.trim();
    if (searchTerm) {
        // 実際の検索機能が実装されるまでは記事一覧ページに移動
        window.location.href = "{{ url_for('posts_list') }}";
    } else {
        document.getElementById('searchInput').focus();
    }
}

// Enterキーで検索
document.getElementById('searchInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchPosts();
    }
});

// ページロード時のアニメーション
document.addEventListener('DOMContentLoaded', function() {
    const elements = document.querySelectorAll('.card, .btn');
    elements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';

        setTimeout(() => {
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

// 10秒後に自動リダイレクト
let countdown = 30;
const redirectTimer = setInterval(function() {
    countdown--;
    if (countdown === 0) {
        window.location.href = "{{ url_for('home') }}";
    }
}, 1000);

// ユーザーが何かアクションを起こしたらタイマーを停止
document.addEventListener('click', function() {
    clearInterval(redirectTimer);
});

document.addEventListener('keypress', function() {
    clearInterval(redirectTimer);
});