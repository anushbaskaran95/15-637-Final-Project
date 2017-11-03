$('#add-course-form').on('submit', function(e) {
    e.preventDefault();
    $.post( "/add-course", $( "#add-course-form" ).serialize())
        .done(function(data) {
            if(data['status'] == 'fail') {
                $('#course-name-error').html(data['errors'][0]['course_name']);
            }
            else {
                $('#add-course-modal').modal('close');
                location.reload();
            }
        })
        .fail(function() {
            alert( "An error occurred when submitting the form" );
        })
});


$('#course-task-form').on('submit', function(e) {
    e.preventDefault();
    $.post( "/add-course-task", $( "#course-task-form" ).serialize())
        .done(function(data) {
            console.log(data)
            if(data['status'] == 'fail') {
                errors = data['errors'];
                for (var key in errors) {
                    $('#'+key).append(errors[key]);
                }
                $('#errors-note').html('Check errors above');
            }
            else {
                $('#course-task-modal').modal('close');
                location.reload();
            }
        })
        .fail(function() {
            alert( "An error occurred when submitting the form" );
        })
});