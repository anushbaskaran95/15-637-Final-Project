// The boilerplate code below is copied from the Django 1.10 documentation.
// It establishes the necessary HTTP header fields and cookies to use
// Django CSRF protection with jQuery Ajax requests.

$( document ).ready(function() {  // Runs when the document is ready
  /**
   * the current path
   *
   */
  //var pathname = window.location.pathname; // Returns path only
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
       console.log(status);
       console.log(task_id);
       //console.log(info);
       //console.log(pathname);
        $.ajax({
           url : '/button_process/',
           type : "post",
           data : {
             status : status,
             task_id : task_id,
             info : info
           }
       });
   });
   /**
    * once user has clicked any of stop button, it will send its id to backend.
    * Info is to tell backend where this infomation comes from.
    */
  $(".stop").click(function(){
    var task_id = $(this).parent().prev().find('input[name = id]').val();
    var info = "stop button";
    // console.log(task_id);
    // console.log(info);
    $.ajax({
       url : '/stop_process/',
       type : "post",
       data : {
         task_id : task_id,
         info : info
       }
   });
  });

}); // End of $(document).ready
