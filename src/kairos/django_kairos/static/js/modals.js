$('#add-course-form').on('submit', function(e) {
    e.preventDefault();
    $.post( "/add-course", $( "#add-course-form" ).serialize())
        .done(function(data) {
            clear_errors();
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
            clear_errors();
            if(data['status'] == 'fail') {
                errors = data['errors'];
                for (var key in errors) {
                    $('#course-task-form').find('#'+key).html(errors[key]);
                }
                $('#course-task-form').find('#errors-note').html('Check errors above');
            }
            else {
                $.ajax({
                    url : 'pause-task',
                    type : "post",
                    data : {
                        status : 'true',
                        task_id : data['task_id']
                    }
                }).done(function() {
                    $('#course-task-modal').modal('close');
                    location.reload();
                });
            }
        })
        .fail(function() {
            alert( "An error occurred when submitting the form" );
        })
});


$('#research-task-form').on('submit', function(e) {
    e.preventDefault();
    $.post( "/add-research-task", $( "#research-task-form" ).serialize())
        .done(function(data) {
            clear_errors();
            if(data['status'] == 'fail') {
                errors = data['errors'];
                for (var key in errors) {
                    $('#research-task-form').find('#'+key).html(errors[key]);
                }
                $('#research-task-form').find('#errors-note').html('Check errors above');
            }
            else {
                $.ajax({
                    url : 'pause-task',
                    type : "post",
                    data : {
                        status : 'true',
                        task_id : data['task_id']
                    }
                }).done(function() {
                    $('#research-task-modal').modal('close');
                    location.reload();
                });
            }
        })
        .fail(function() {
            alert( "An error occurred when submitting the form" );
        })
});


$('#routine-task-form').on('submit', function(e) {
    e.preventDefault();
    $.post( "/add-routine-task", $( "#routine-task-form" ).serialize())
        .done(function(data) {
            clear_errors();
            if(data['status'] == 'fail') {
                errors = data['errors'];
                for (var key in errors) {
                    $('#routine-task-form').find('#'+key).html(errors[key]);
                }
                $('#routine-task-form').find('#errors-note').html('Check errors above');
            }
            else {
                $.ajax({
                    url : 'pause-task',
                    type : "post",
                    data : {
                        status : 'true',
                        task_id : data['task_id']
                    }
                }).done(function() {
                    $('#routine-task-modal').modal('close');
                    location.reload();
                });
            }
        })
        .fail(function() {
            alert( "An error occurred when submitting the form" );
        })
});


function clear_errors() {
    $('#course-name-error').html('');
    $('#task-name-error').html('');
    $('#topic-error').html('');
    $('#start-date-error').html('');
    $('#finish-date-error').html('');
    $('#due-date-error').html('');
    $('#errors-note').html('');
    $('#time-needed-error').html('');
}