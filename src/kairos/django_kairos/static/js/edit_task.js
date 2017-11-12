function getEditCourseModal(task_id, task_info_id) {
    $.get( "/edit-course-modal/"+task_id+"/"+task_info_id,)
        .done(function(data) {

        })
        .fail(function() {
            console.log('An error occurred')
        })
}

function getEditResearchModal(task_id, task_info_id) {
    $.get( "/edit-research-modal/"+task_id+"/"+task_info_id,)
        .done(function(data) {

        })
        .fail(function() {
            console.log('An error occurred')
        })
}

function getEditRoutineModal(task_id, task_info_id) {
    $.get( "/edit-routine-modal/"+task_id+"/"+task_info_id,)
        .done(function(data) {

        })
        .fail(function() {
            console.log('An error occurred')
        })
}