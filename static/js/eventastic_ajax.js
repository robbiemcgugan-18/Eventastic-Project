$(document).on('click', '#interest-button', function(e) {
  e.preventDefault();

  var interestURL = $(this).attr('url');

  $.ajax({
    type: 'GET',
    url: interestURL,
    data: {
      name: $('#interest-button').val(),
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
      action: 'post'
    },
    success: function(json) {
      document.getElementById("interest-counter").innerHTML = json['result']
      console.log(json)
    },
    error: function(xhr, errmsg, err) {

    }
  });
})
