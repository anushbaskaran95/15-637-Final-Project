$( document ).ready(function() {  // Runs when the document is ready
   /**
    * once user has clicked the switch, it will send the boolean value and corresponding
    * task id to the backend for further processing.
    * Info is to tell backend where this infomation comes from.
    *
    */
    $(".switch").find("input[type=checkbox]").on("change",function() {
        var status = $(this).prop('checked');
        var task_id = $(this).val();
        var info = "switch";
        //console.log(status);
        //console.log(task_id);
        $.ajax({
            url : 'button_process',
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
        var task_id = $(this).attr('id');
        var info = "stop button";
        //console.log(task_id);
        $.ajax({
            url : 'stop_process',
            type : "post",
            data : {
                task_id : task_id,
                info : info
            }
        }).done(function() {
            location.reload();
        });
    });
}); // End of $(document).ready
