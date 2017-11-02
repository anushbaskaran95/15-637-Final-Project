function add_course() {
    $.post( "/add-course", $( "#add-course-form" ).serialize())
        .done(function(data) {
            if(data['status'] == 'fail') {
                console.log(data['error']);
                $('.course-name-error').html(data['error']);
            }
            else {
                console.log('ok');
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