$(document).ready(function() {
    $('[like-form]').submit(function(event){
        event.preventDefault();
        let submitter_btn = $(event.originalEvent.submitter);
        var data = new FormData(event.target);
        if (submitter_btn.attr("name") == "likeButton") {
            data.append("likeButton", $("#likeButton").val());
        }
        else if (submitter_btn.attr("name") == "dislikeButton") {
            data.append("dislikeButton", $("#dislikeButton").val());
        }

        $.ajax({
            type: 'POST',
            url: '/onlypics/like_picture',
            enctype: 'multipart/form-data',
            cache: false,
            processData: false,
            contentType: false,
            data: data,
            success: function (response) {
                event.target.reset();
                var result = response["like_result"];
                alert(result);
                if (result) {
                    $("#likeButton").css({'color':'#fff',
                        'background-color' :'#6c757d',
                        'border-color':'#6c757d'});
                }
                else {
                    $("#dislikeButton").css({'color':'#fff',
                        'background-color' :'#6c757d',
                        'border-color':'#6c757d'});
                }
            },
            error: function (response) {
                // alert the error if any error occured
                alert("An error occured!");
                alert("wowowo");
            }
        });
        return false;
    });
});

