document.addEventListener('DOMContentLoaded', function() {
    // 削除確認関数をグローバルスコープに定義
    window.confirmDelete = function(postId, title) {
        const deleteTitle = document.getElementById('deleteTitle');
        const deleteForm = document.getElementById('deleteForm');
        const deleteModal = document.getElementById('deleteModal');

        // 削除モーダルの要素が存在するかチェック（編集時のみ存在）
        if (deleteTitle && deleteForm && deleteModal) {
            deleteTitle.textContent = title;
            deleteForm.action = '/admin/post/' + postId + '/delete';

            if (typeof bootstrap !== 'undefined') {
                new bootstrap.Modal(deleteModal).show();
            } else {
                console.error('Bootstrap not loaded');
                // フォールバック
                if (confirm('本当に「' + title + '」を削除しますか？')) {
                    deleteForm.submit();
                }
            }
        } else {
            console.error('Delete modal elements not found');
        }
    };

    // フォーム要素の取得
    const titleElement = document.getElementById('title');
    const contentElement = document.getElementById('content');
    const publishedElement = document.getElementById('is_published');
    const formElement = document.querySelector('form');

    // 必要な要素が存在しない場合は処理を中断
    if (!titleElement || !contentElement || !publishedElement || !formElement) {
        console.log('Some form elements not found, skipping form change detection');
        return;
    }

    // フォームの保存前確認
    let hasChanges = false;
    const initialTitle = titleElement.value;
    const initialContent = contentElement.value;
    const initialPublished = publishedElement.checked;

    console.log('Initial form values loaded:', {
        title: initialTitle,
        contentLength: initialContent.length,
        published: initialPublished
    });

    // 変更検知関数
    function checkChanges() {
        hasChanges = (
            titleElement.value !== initialTitle ||
            contentElement.value !== initialContent ||
            publishedElement.checked !== initialPublished
        );

        console.log('Form changes detected:', hasChanges);
    }

    // イベントリスナーの追加
    titleElement.addEventListener('input', checkChanges);
    contentElement.addEventListener('input', checkChanges);
    publishedElement.addEventListener('change', checkChanges);

    // ページ離脱時の確認
    window.addEventListener('beforeunload', function (e) {
        if (hasChanges) {
            console.log('Preventing page unload due to unsaved changes');
            e.preventDefault();
            e.returnValue = '';
        }
    });

    // フォーム送信時は確認をスキップ
    formElement.addEventListener('submit', function() {
        console.log('Form submitted, disabling change detection');
        hasChanges = false;
    });
});