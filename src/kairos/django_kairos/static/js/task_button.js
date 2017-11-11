// The boilerplate code below is copied from the Django 1.10 documentation.
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
  /**
   * the current path
   *
   */
  var pathname = window.location.pathname; // Returns path only
  /**
   * once user has clicked the switch, it will send the boolean value and corresponding
   * task id to the backend for further processing.
   * Info is to tell backend where this infomation comes from.
   *
   */
  $(".switch").find("input[type=checkbox]").on("change",function() {
       var status = $(this).prop('checked');
       var task_id = $(this).parent().next().val();
       var info = "switch";
       //console.log(status);
       //console.log(task_id);
        $.ajax({
           url : pathname,
           type : "post",
           data : {
             status : status,
             task_id : task_id,
             info : info
           }
       })
   });
   /**
    * once user has clicked any of stop button, it will send its id to backend.
    * Info is to tell backend where this infomation comes from.
    */
  $(".waves-effect.waves-light.btn").click(function(){
    var task_id = $(this).parent().prev().find('input[name = id]').val();
    var info = "stop button";
    // console.log(task_id);
    // console.log(info);
    $.ajax({
       url : pathname,
       type : "post",
       data : {
         task_id : task_id,
         info : info
       }
   })
  })

}); // End of $(document).ready
