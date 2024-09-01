$(document).ready(function() {
    $('.follow-form').submit(function(e) {
        e.preventDefault();
        var form = $(this);
        var url = form.attr('action');
        var button = form.find('button');
        
        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            success: function(response) {
                if (response.is_following) {
                    // Set button text to "Following" and add a class to maintain state
                    button.text('Following').addClass('following');
                } else {
                    // Set button text to "Follow" and remove the class
                    button.text('Follow').removeClass('following');
                }

                // Update follower and following count
                $('#follower-count').text(response.follower_count);
                $('#following-count').text(response.following_count);
            },
            error: function(xhr, status, error) {
                console.error('AJAX Error: ' + error);
            }
        });
    });
});
