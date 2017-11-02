function add_course() {
    $.post( "/add-course", $( "#add-course-form" ).serialize())
        .done(function(data) {
            if(data['success'] == 'fail') {
                $('.course-name-error').html(data['error']);
            }
            else {
                $('#add-course-modal').modal('close');
                location.reload();
            }
        })
        .fail(function() {
            alert( "An error occurred when submitting the form" );
        })
        .always(function() {
        });
}