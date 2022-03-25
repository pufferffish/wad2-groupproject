$(document).ready(function() {
    $('[picture-form]').submit(function(event){
        event.preventDefault();
        var data = new FormData(event.target);
        console.log(data);
        $.ajax({
            type: 'POST',
            url: '/onlypics/post_comment',
            enctype: 'multipart/form-data',
            cache: false,
            processData: false,
            contentType: false,
            data: data,
            success: function (response) {
                event.target.reset();
                console.log(response);
                var nickname = response["nickname"];
                var text = response["text"];
                $("#comment-" + response["uuid"]).append(
                    `<p style="float: left; margin-left: 20px;"><strong>${nickname}</strong> : ${text}</p>`
                );
            },
            error: function (response) {
                // alert the error if any error occured
                alert("An error occured!")
            }
        });
        return false;
    });
});
