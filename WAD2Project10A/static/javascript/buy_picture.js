function buyPicture(picture_id) {
    console.log(picture_id);
    $.ajax({
        type: 'GET',
        url: '/onlypics/buy_picture',
        data: {'picture_id':picture_id},
        success: function (response) {
            result = response['result'];
            if (result == "failure") {
                alert("This picture cannot be bought because you dont have enough tokens!");
            }
            window.location = "/onlypics/account";
        },
        error: function (response) {
            alert("An error occured!");
        },
    })
}

