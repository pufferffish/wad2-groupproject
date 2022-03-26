function escapeHtml(html){
  var text = document.createTextNode(html);
  var p = document.createElement('p');
  p.appendChild(text);
  return p.innerHTML;
}

$(document).ready(function() {
<<<<<<< HEAD
    $('#post-comment-form').submit(function (e){
        e.preventDefault();
        var endpoint = $("#post-comment-form").attr("data-url");

=======
    $('[picture-form]').submit(function(event){
        event.preventDefault();
        var data = new FormData(event.target);
        console.log(data);
>>>>>>> main
        $.ajax({
            type: 'POST',
            url: '/onlypics/post_comment',
            enctype: 'multipart/form-data',
            cache: false,
            processData: false,
            contentType: false,
            data: data,
            success: function (response) {
<<<<<<< HEAD
                $("#post-comment-form").trigger('reset');
                var comment = JSON.stringify(response["comment_text"])
                var parsed_comment = JSON.parse(comment)
                var nickname = JSON.stringify(response["user_nickname"]);
                var parsed_nickname = JSON.parse(nickname)
                $("#comment-section").append(
                    `<p style="float: left; margin-left: 20px;"><strong>${parsed_nickname['user_nickname']}</strong> : ${parsed_comment['comment_text']}</p>`
=======
                event.target.reset();
                console.log(response);
                var nickname = escapeHtml(response["nickname"]);
                var text = escapeHtml(response["text"]);
                var p = document.createElement("p")
                p.style = "float: left; margin-left: 20px;";
                $("#comment-" + response["uuid"]).append(
                    `<p style="float: left; margin-left: 20px;"><strong>${nickname}</strong> : ${text}</p>`
>>>>>>> main
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
