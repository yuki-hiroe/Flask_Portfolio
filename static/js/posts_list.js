// 記事カードにホバー効果を追加
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.3s ease';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});

// 無限スクロール（将来の拡張用）
function loadMorePosts() {
    // 実装時はAJAXで追加の記事を読み込み
    console.log('無限スクロール機能は将来実装予定');
}