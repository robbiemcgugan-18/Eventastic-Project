// If the user clicks on the interest button
$(document).on('click', '#interest-button', function (e) {
    e.preventDefault();

    var interestURL = $(this).attr('url');

    // Perform a GET request to the interestURL (interest view)
    $.ajax({
        type: 'GET',
        url: interestURL,
        // Pass through the values currently in the interest button
        data: {
            name: $('#interest-button').val(),
            action: 'get'
        },
        // On success receive a JSON response from the interest view
        success: function (json) {
            // Update the interst counter with the new value from the JSN data
            document.getElementById("interest-counter").innerHTML = json.result

            // If the user is now interested in the event
            if (json.interested) {
                // Update the CSS to show that the user is now interested
                document.getElementById("interest-button").style.backgroundColor = "white";
                document.getElementById("interest-button").style.color = "black";
                document.getElementById("interest-button").innerHTML = "Interested";
            // Else if they are now uninterested
            } else {
              // Return the styles back to the default styles
                document.getElementById("interest-button").style.backgroundColor = "";
                document.getElementById("interest-button").style.color = "";
                document.getElementById("interest-button").innerHTML = "Register Interest";
            }
        },
    });
})
