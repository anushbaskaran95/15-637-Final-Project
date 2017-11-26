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
