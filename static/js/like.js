function getCsrfToken() {
    const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
    return cookie ? cookie.trim().split('=')[1] : '';
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.like-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const postId = btn.dataset.postId;

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
                    btn.classList.toggle('like-btn--active', data.liked);
                    btn.querySelector('.like-count').textContent = data.count;
                });
        });
    });
});
