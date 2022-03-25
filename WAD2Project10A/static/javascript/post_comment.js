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
                var instance = JSON.parse(response["instance"]);
                var nickname = JSON.stringify(response["nickname"]);
                var parsed = JSON.parse(nickname)
                var fields = instance[0]["fields"];
                $(".scrollable").append(
                    `<p style="float: left; margin-left: 20px;"><strong>${parsed['user_nickname']}</strong> : ${fields['text']}</p>`
                );
            },
            error: function (response) {
                // alert the error if any error occured
                alert("An error occured!")
            }
        });
    });
});