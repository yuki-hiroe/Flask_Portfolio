// ページ読み込み時のアニメーション効果
document.addEventListener('DOMContentLoaded', function() {
    // カードのアニメーション
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';

        setTimeout(() => {
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // スキルバーのアニメーション（将来の拡張用）
    const skillBars = document.querySelectorAll('.skill-progress');
    skillBars.forEach(bar => {
        const targetWidth = bar.dataset.skill;
        setTimeout(() => {
            bar.style.width = targetWidth + '%';
        }, 500);
    });
});

// スムーススクロール
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});