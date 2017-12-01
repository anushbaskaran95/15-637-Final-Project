function getEditCourseModal(task_id, task_info_id) {
    $.get( "/edit-course-modal/"+task_id+"/"+task_info_id,)
        .done(function(data) {
            $('#edit-course-task-modal').modal('open');
            $('.edit-course-task-modal').html(data);
            initPickers();
            Materialize.updateTextFields();
        })
        .fail(function() {
            console.log('An error occurred')
        })
}

function getEditResearchModal(task_id, task_info_id) {
    $.get( "/edit-research-modal/"+task_id+"/"+task_info_id,)
        .done(function(data) {
            $('#edit-research-task-modal').modal('open');
            $('.edit-research-task-modal').html(data);
            initPickers();
            Materialize.updateTextFields();
        })
        .fail(function() {
            console.log('An error occurred')
        })
}

function getEditRoutineModal(task_id, task_info_id) {
    $.get( "/edit-routine-modal/"+task_id+"/"+task_info_id,)
        .done(function(data) {
            $('#edit-routine-task-modal').modal('open');
            $('.edit-routine-task-modal').html(data);
            initPickers();
            Materialize.updateTextFields();
        })
        .fail(function() {
            console.log('An error occurred')
        })
}


$('body').on('submit', '#edit-course-task-form', function(e) {
    e.preventDefault();
    ids = $(this).find('.modal-action').attr('id').split('/');
    task_id = ids[0]
    task_info_id = ids[1]
    $.post( "/edit-course-task", {'form': $( "#edit-course-task-form" ).serialize(),
                                  'task_id': task_id, 'task_info_id': task_info_id})
        .done(function(data) {
            clear_errors_edit_form('#edit-course-task-form');
            if(data['status'] == 'fail') {
                errors = data['errors'];
                for (var key in errors) {
                    $('.edit-course-task-modal').find('#'+key).html(errors[key]);
                }
                $('.edit-course-task-modal').find('#errors-note').html('Check errors above');
            }
            else {
                $('#edit-course-task-modal').modal('close');
                location.reload();
            }
        })
        .fail(function() {
            alert( "An error occurred" );
        })
});


$('body').on('submit', '#edit-research-task-form', function(e) {
    e.preventDefault();
    ids = $(this).find('.modal-action').attr('id').split('/');
    task_id = ids[0]
    task_info_id = ids[1]
    $.post( "/edit-research-task", {'form': $( "#edit-research-task-form" ).serialize(),
                                  'task_id': task_id, 'task_info_id': task_info_id})
        .done(function(data) {
            clear_errors_edit_form('#edit-research-task-form');
            if(data['status'] == 'fail') {
                errors = data['errors'];
                for (var key in errors) {
                    $('.edit-research-task-modal').find('#'+key).html(errors[key]);
                }
                $('.edit-research-task-modal').find('#errors-note').html('Check errors above');
            }
            else {
                $('#edit-research-task-modal').modal('close');
                location.reload();
            }
        })
        .fail(function() {
            alert( "An error occurred" );
        })
});


$('body').on('submit', '#edit-routine-task-form', function(e) {
    e.preventDefault();
    ids = $(this).find('.modal-action').attr('id').split('/');
    task_id = ids[0]
    task_info_id = ids[1]
    $.post( "/edit-routine-task", {'form': $( "#edit-routine-task-form" ).serialize(),
                                  'task_id': task_id, 'task_info_id': task_info_id})
        .done(function(data) {
            clear_errors_edit_form('#edit-routine-task-form');
            if(data['status'] == 'fail') {
                errors = data['errors'];
                for (var key in errors) {
                    $('.edit-routine-task-modal').find('#'+key).html(errors[key]);
                }
                $('.edit-routine-task-modal').find('#errors-note').html('Check errors above');
            }
            else {
                $('#edit-routine-task-modal').modal('close');
                location.reload();
            }
        })
        .fail(function() {
            alert( "An error occurred" );
        })
});


function clear_errors_edit_form(form_id) {
    $(form_id).find('#task-name-error').html('');
    $(form_id).find('#topic-error').html('');
    $(form_id).find('#finish-date-error').html('');
    $(form_id).find('#due-date-error').html('');
    $(form_id).find('#errors-note').html('');
    $(form_id).find('#pc-error').html('');
}