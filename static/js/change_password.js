// パスワード強度とマッチングのリアルタイムチェック
const newPassword = document.getElementById('new_password');
const confirmPassword = document.getElementById('confirm_password');
const submitBtn = document.getElementById('submitBtn');
const matchFeedback = document.getElementById('passwordMatchFeedback');
const lengthCheck = document.getElementById('length-check');
const matchCheck = document.getElementById('match-check');

function checkPasswords() {
    const newPass = newPassword.value;
    const confirmPass = confirmPassword.value;

    // 長さチェック
    if (newPass.length >= 6) {
        lengthCheck.innerHTML = '<i class="fas fa-check text-success me-1"></i>6文字以上';
        lengthCheck.classList.remove('text-muted', 'text-danger');
        lengthCheck.classList.add('text-success');
    } else {
        lengthCheck.innerHTML = '<i class="fas fa-times text-danger me-1"></i>6文字以上';
        lengthCheck.classList.remove('text-muted', 'text-success');
        lengthCheck.classList.add('text-danger');
    }

    // パスワード一致チェック
    if (confirmPass.length > 0) {
        if (newPass === confirmPass) {
            matchFeedback.innerHTML = '<i class="fas fa-check text-success me-1"></i>パスワードが一致しています';
            matchFeedback.className = 'form-text text-success';
            matchCheck.innerHTML = '<i class="fas fa-check text-success me-1"></i>パスワードが一致';
            matchCheck.classList.remove('text-muted', 'text-danger');
            matchCheck.classList.add('text-success');
        } else {
            matchFeedback.innerHTML = '<i class="fas fa-times text-danger me-1"></i>パスワードが一致しません';
            matchFeedback.className = 'form-text text-danger';
            matchCheck.innerHTML = '<i class="fas fa-times text-danger me-1"></i>パスワードが一致';
            matchCheck.classList.remove('text-muted', 'text-success');
            matchCheck.classList.add('text-danger');
        }
    } else {
        matchFeedback.innerHTML = '';
        matchCheck.innerHTML = 'パスワードが一致';
        matchCheck.classList.remove('text-success', 'text-danger');
        matchCheck.classList.add('text-muted');
    }

    // 送信ボタンの有効/無効
    const isValid = newPass.length >= 6 && confirmPass.length >= 6 && newPass === confirmPass;
    submitBtn.disabled = !isValid;
}

newPassword.addEventListener('input', checkPasswords);
confirmPassword.addEventListener('input', checkPasswords);

// フォーム送信時の確認
document.getElementById('passwordForm').addEventListener('submit', function(e) {
    if (!confirm('パスワードを変更しますか？')) {
        e.preventDefault();
    }
});