$('.comment-button').click(function() {
    var postId = $(this).data('post-id');
    var commentSection = $(this).closest('.post-card').find('.comment-section');

    $.get("{% url 'get_comments' %}".replace('0', postId), function(data) {
        commentSection.html(data);
    });
});
