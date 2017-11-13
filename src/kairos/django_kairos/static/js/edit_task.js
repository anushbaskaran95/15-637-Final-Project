function getEditCourseModal(task_id, task_info_id) {
    $.get( "/edit-course-modal/"+task_id+"/"+task_info_id,)
        .done(function(data) {
            $('#edit-course-task-modal').modal('open');
            $('.modal-content div.edit-course-task-modal').html(data);
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
            Materialize.updateTextFields();
        })
        .fail(function() {
            console.log('An error occurred')
        })
}