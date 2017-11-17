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
            clear_errors_edit_form();
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
            clear_errors_edit_form();
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
    console.log($(this).find('button').attr('id'));
//    $.post( "/add-course", $( "#edit-course-task-form" ).serialize())
//        .done(function(data) {
//            clear_errors();
//            if(data['status'] == 'fail') {
//                $('#course-name-error').html(data['errors'][0]['course_name']);
//            }
//            else {
//                $('#add-course-modal').modal('close');
//                location.reload();
//            }
//        })
//        .fail(function() {
//            alert( "An error occurred when submitting the form" );
//        })
});


function clear_errors_edit_form() {
    $('#task-name-error').html('');
    $('#topic-error').html('');
    $('#finish-date-error').html('');
    $('#due-date-error').html('');
    $('#errors-note').html('');
}