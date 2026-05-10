function applyLikeState(btn, liked, count) {
    btn.classList.toggle('like-btn--active', liked);
    btn.querySelector('.like-count').textContent = count;
}

function initLikeButton(btn) {
    const postId = btn.dataset.postId;
    const reviewId = btn.dataset.reviewId;
    const statusParam = postId ? 'post_id=' + postId : 'review_id=' + reviewId;
    const bodyParam = postId ? 'post_id=' + postId : 'review_id=' + reviewId;

    fetch('/social/like/status/?' + statusParam)
        .then(r => r.json())
        .then(data => applyLikeState(btn, data.liked, data.count));

    btn.addEventListener('click', function () {
        fetch('/social/like/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCsrfToken(),
            },
            body: bodyParam,
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
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.like-btn[data-post-id], .like-btn[data-review-id]').forEach(initLikeButton);
});
