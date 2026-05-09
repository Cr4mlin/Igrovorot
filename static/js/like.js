function applyLikeState(btn, liked, count) {
    btn.classList.toggle('like-btn--active', liked);
    btn.querySelector('.like-count').textContent = count;
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.like-btn').forEach(function (btn) {
        const postId = btn.dataset.postId;

        fetch('/social/like/status/?post_id=' + postId)
            .then(r => r.json())
            .then(data => applyLikeState(btn, data.liked, data.count));

        btn.addEventListener('click', function () {
            fetch('/social/like/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: 'post_id=' + postId,
            })
                .then(function (response) {
                    if (response.status === 401) {
                        window.location.href = '/accounts/login/';
                        return null;
                    }
                    return response.json();
                })
                .then(function (data) {
                    if (!data) return;
                    applyLikeState(btn, data.liked, data.count);
                });
        });
    });
});
