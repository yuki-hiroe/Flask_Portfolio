function copyToClipboard() {
    navigator.clipboard.writeText(window.location.href).then(function() {
        // 一時的な成功メッセージを表示
        const btn = event.target.closest('button');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check me-1"></i>コピーしました！';
        btn.classList.remove('btn-outline-secondary');
        btn.classList.add('btn-success');

        setTimeout(function() {
            btn.innerHTML = originalText;
            btn.classList.remove('btn-success');
            btn.classList.add('btn-outline-secondary');
        }, 2000);
    }).catch(function(err) {
        console.error('コピーに失敗しました: ', err);
    });
}

// 読み進めた割合を表示するプログレスバー
window.addEventListener('scroll', function() {
    const article = document.querySelector('article');
    if (article) {
        const rect = article.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        const articleHeight = article.offsetHeight;
        const scrollProgress = Math.max(0, Math.min(1, (windowHeight - rect.top) / articleHeight));

        // プログレスバーを表示する場合はここに追加
    }
});