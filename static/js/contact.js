// フォームバリデーション
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    const submitBtn = form.querySelector('button[type="submit"]');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // 送信ボタンの状態変更
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>送信中...';

        // 実際の送信処理（今回はシミュレート）
        setTimeout(function() {
            // 成功メッセージ
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-success alert-dismissible fade show';
            alertDiv.innerHTML = `
                お問い合わせありがとうございました。24時間以内にご返信いたします。
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;

            form.parentNode.insertBefore(alertDiv, form);

            // フォームリセット
            form.reset();

            // ボタンを元に戻す
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;

            // ページトップにスクロール
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }, 2000);
    });

    // リアルタイムバリデーション
    const requiredFields = form.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        field.addEventListener('blur', function() {
            if (!this.value.trim()) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });

        field.addEventListener('input', function() {
            if (this.classList.contains('is-invalid') && this.value.trim()) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
    });

    // メールアドレス形式チェック
    const emailField = document.getElementById('email');
    emailField.addEventListener('blur', function() {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (this.value && !emailPattern.test(this.value)) {
            this.classList.add('is-invalid');
        } else if (this.value) {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        }
    });
});

// 文字数カウンター
const messageField = document.getElementById('message');
const charCounter = document.createElement('div');
charCounter.className = 'form-text text-end';
charCounter.innerHTML = '0 文字';
messageField.parentNode.appendChild(charCounter);

messageField.addEventListener('input', function() {
    const length = this.value.length;
    charCounter.innerHTML = `${length} 文字`;

    if (length < 10) {
        charCounter.className = 'form-text text-end text-danger';
    } else if (length > 1000) {
        charCounter.className = 'form-text text-end text-warning';
    } else {
        charCounter.className = 'form-text text-end text-muted';
    }
});