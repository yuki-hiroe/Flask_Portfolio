function confirmDelete(postId, title) {
    document.getElementById('deleteTitle').textContent = title;
    document.getElementById('deleteForm').action = '/admin/post/' + postId + '/delete';
    new bootstrap.Modal(document.getElementById('deleteModal')).show();
}