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
            clear_errors('#course-task-form');
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
            clear_errors('#research-task-form');
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
            clear_errors('#routine-task-form');
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


function clear_errors(form_id) {
    $(form_id).find('#course-name-error').html('');
    $(form_id).find('#task-name-error').html('');
    $(form_id).find('#topic-error').html('');
    $(form_id).find('#start-date-error').html('');
    $(form_id).find('#finish-date-error').html('');
    $(form_id).find('#due-date-error').html('');
    $(form_id).find('#errors-note').html('');
    $(form_id).find('#time-needed-error').html('');
}