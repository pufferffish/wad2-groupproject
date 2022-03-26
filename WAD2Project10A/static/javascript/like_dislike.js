$(document).ready(function() {
    $('[like-form]').submit(function(event){
        event.preventDefault();
        let submitter_btn = $(event.originalEvent.submitter);
        var data = new FormData(event.target);
        var picture_uuid = data['picture_uuid'];
        console.log(submitter_btn.attr("id"))

        if (submitter_btn.attr("name") == "likeButton") {
            data.append("likeButton", $("#likeButton + picture_uuid").val());
        }
        else if (submitter_btn.attr("name") == "dislikeButton") {
            data.append("dislikeButton", $("#dislikeButton + picture_uuid").val());
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
                like_dislike = response["like_result"];
                if ("error" in response) {
                    if (like_dislike) {
                        $("#haveVoted").text(response["error"] + "Like!");
                    }
                    else {
                        $("#haveVoted").text(response["error"] + "Dislike!");
                    }
                }
                else {
                    var pic_uuid = response["uuid"];

                    if (like_dislike) {
                        $("#likeButton + pic_uuid").css({'color':'#fff',
                            'background-color' :'#6c757d',
                            'border-color':'#6c757d'});
                    }
                    else {
                        $("#dislikeButton + pic_uuid").css({'color':'#fff',
                            'background-color' :'#6c757d',
                            'border-color':'#6c757d'});
                    }
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

