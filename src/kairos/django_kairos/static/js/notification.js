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

  function setCookie(exdays, task_id) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    console.log(task_id);
    document.cookie = expires + ";path=/;" + "task_shown=" + task_id;
    console.log(document.cookie);
}

function checkCookie(task_id) {
  $.ajax({
    type:"POST",
    url:"/check-cookie",
    data: {
      'task_id':task_id
    }
  }).done(function(data){
    if (data == 'true') {
      return true;
    } else {
      return false;
    }
  })
    // var task_id_shown = getCookie("task_shown");
    // console.log(task_id_shown);
    // if (task_id_shown == null ||task_id_shown == "") {
    //     return false;
    // }
    // console.log(task_id_shown);
    // for (var i = 0; i < task_id_shown.length; i++) {
    //   if (task_id == parseInt(task_id_shown.charAt(i))) {
    //     return true;
    //   }
    // }
    //
    // return false;
}



  // Periodically check if a task is approaching the deadline
  window.setInterval(getNotification, 5000);


  function getNotification(data) {
    //console.log("in getNotification");
    $.ajax({
      url: '/get-notification',
      type: 'GET',
    }).done(function(data){
      //console.log("finish get notification");
      if (data) {
        for (var key in data) {
          // if (!checkCookie(key)) {
          //   var message = data[key];
          //   Materialize.toast(message, 3000, 'rounded') // 'rounded' is the class I'm applying to the toast
          //   //setCookie(1, key);
          // }
          var message = data[key];
          Materialize.toast(message, 3000, 'rounded') // 'rounded' is the class I'm applying to the toast
        }
      }
    }).fail(function(xhr, status, errorThrown) {
          alert("error");
          console.log("error" + errorThrown);
          console.log("status" + status);
          console.dir(xhr);
    });
  }



}); // End of $(document).ready
