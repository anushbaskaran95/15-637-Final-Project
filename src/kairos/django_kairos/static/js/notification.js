// The boilerplate code below is copied from the Django 1.11 documentation.
// It establishes the necessary HTTP header fields and cookies to use
// Django CSRF protection with jQuery Ajax requests.

$( document ).ready(function() {  // Runs when the document is ready
  // using jQuery
  // https://docs.djangoproject.com/en/1.10/ref/csrf/
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  var csrftoken = getCookie('csrftoken');

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });



  // Periodically check if a task is approaching the deadline
  window.setInterval(getNotification, 5000);


  function getNotification(data) {
    //console.log("in getNotification");
    $.ajax({
      url: '/get-notification-expected-finish',
      type: 'GET',
    }).done(function(data){
      //console.log("finish get notification");
      if (data) {
        for (var key in data) {
          var message = data[key];
          Materialize.toast(message, 3000, 'rounded') // 'rounded' is the class I'm applying to the toast
        }
      }
    }).fail(function(xhr, status, errorThrown) {
          console.log("error" + errorThrown);
          console.log("status" + status);
          console.dir(xhr);
    });

    $.ajax({
      url: '/get-notification-due',
      type: 'GET',
    }).done(function(data){
      //console.log("finish get notification");
      if (data) {
        for (var key in data) {
          var message = data[key];
          Materialize.toast(message, 3000, 'rounded') // 'rounded' is the class I'm applying to the toast
        }
      }
    }).fail(function(xhr, status, errorThrown) {
          console.log("error" + errorThrown);
          console.log("status" + status);
          console.dir(xhr);
    });
  }



}); // End of $(document).ready
