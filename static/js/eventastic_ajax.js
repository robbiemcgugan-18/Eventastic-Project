$(document).on('click', '#interest-button', function (e) {
    e.preventDefault();

    var interestURL = $(this).attr('url');

    $.ajax({
        type: 'GET',
        url: interestURL,
        data: {
            name: $('#interest-button').val(),
            action: 'get'
        },
        success: function (json) {
            document.getElementById("interest-counter").innerHTML = json.result
            var cssLiked = "#{background-color:white; color:black}";
            var cssUnliked = "{background-color:transparent; color:white}";

            if (json.liked) {
                document.getElementById("interest-button").style.backgroundColor = "white";
                document.getElementById("interest-button").style.color = "black";
                document.getElementById("interest-button").innerHTML = "Interested";
            } else {
                document.getElementById("interest-button").style.backgroundColor = "";
                document.getElementById("interest-button").style.color = "";
                document.getElementById("interest-button").innerHTML = "Register Interest";
            }
        },
        error: function (xhr, errmsg, err) {

        }
    });
})
