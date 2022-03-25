$(document).ready(function() {
    $('#like-form').submit(function (e){
        e.preventDefault();
        var endpoint = $("#like-form").attr("data-url");
        $.ajax({
            type: 'POST',
            url: 'like_picture',
            dataType: 'json',
            data: $(this).serialize(),
            success: function (response) {
                var like_result = JSON.stringify(response['like_dislike'])
                var parsed_result = JSON.parse(like_result)
                if (parsed_result['like_dislike'] == true) {
                    alert("true");
                    $("#like-button").css('background-color','blue');
                }
                else {
                    alert("false");
                    $("#dislike-button").css('background-color','blue');
                }
            },
            error: function (response) {
                // alert the error if any error occured
                alert("An error occured!")
            }
        });
    });
});