$(document).ready(function() {
    $('#post-comment-form').submit(function (e){
        e.preventDefault();
        var endpoint = $("#post-comment-form").attr("data-url");

        $.ajax({
            type: 'POST',
            url: endpoint,
            data: $(this).serialize(),
            success: function (response) {
                $("#post-comment-form").trigger('reset');
                var comment = JSON.stringify(response["comment_text"])
                var parsed_comment = JSON.parse(comment)
                var nickname = JSON.stringify(response["user_nickname"]);
                var parsed_nickname = JSON.parse(nickname)
                $("#comment-section").append(
                    `<p style="float: left; margin-left: 20px;"><strong>${parsed_nickname['user_nickname']}</strong> : ${parsed_comment['comment_text']}</p>`
                );
            },
            error: function (response) {
                // alert the error if any error occured
                alert("An error occured!")
            }
        });
    });
});