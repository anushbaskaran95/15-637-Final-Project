function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function(){
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('.button-collapse').sideNav({
        menuWidth: 300, // Default is 300
        edge: 'left', // Choose the horizontal origin
        closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor
        draggable: true, // Choose whether you can drag to open on touch screens,
        onOpen: function(el) {}, // A function to be called when sideNav is opened
        onClose: function(el) {}, // A function to be called when sideNav is closed
    });

    $('.modal').modal({
        dismissible: true, // Modal can be dismissed by clicking outside of the modal
        opacity: .5, // Opacity of modal background
        inDuration: 300, // Transition in duration
        outDuration: 200, // Transition out duration
        startingTop: '4%', // Starting top style attribute
        endingTop: '10%', // Ending top style attribute
        ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
        },
        complete: function() {} // Callback for Modal close
      }
    );

    // make correct tab active
    var tab = $(location).attr('href').split( '/' ).pop();
    if (tab == '') {
        tab = 'current_tasks';
    }
    $('#'+tab).addClass('tab-indicator');

    $('select').material_select();

    initPickers();

    $( ".edit" ).click(function() {
        ids = this.id.split('/');
        switch (ids[2]) {
            case 'CourseTask':
                getEditCourseModal(ids[0], ids[1]);
                break;
            case 'Research':
                getEditResearchModal(ids[0], ids[1]);
                break;
            case 'Misc':
                getEditRoutineModal(ids[0], ids[1]);
                break;
            default:
                console.log('Invalid task type');
        }
    });

    $('.carousel').carousel();

    // get task metrics for D3
    getTaskMetrics();

    // Periodically check if a task is approaching the deadline
    window.setInterval(getNotification, 1000 * 5);
});

function initPickers() {
    $('.datepicker').pickadate({
        selectMonths: false, // Creates a dropdown to control month
        selectYears: 1, // Creates a dropdown of 15 years to control year,
        today: 'Today',
        clear: 'Clear',
        close: 'Ok',
        closeOnSelect: true, // Close upon selecting a date
        min: '0'
    });

    $('.timepicker').pickatime({
        default: 'now', // Set default time: 'now', '1:30AM', '16:30'
        fromnow: 0,       // set default time to * milliseconds from now (using with default = 'now')
        twelvehour: false, // Use AM/PM or 24-hour format
        donetext: 'OK', // text for done-button
        cleartext: 'Clear', // text for clear-button
        canceltext: 'Cancel', // Text for cancel-button
        autoclose: true, // automatic close timepicker
        ampmclickable: true, // make AM PM clickable
        aftershow: function(){} //Function for after opening timepicker
    });
}

function getTaskMetrics() {
    var settingsPB = {
        diameter: 120,
        stroke: {
            width: 15,
            gap: 2
        },
        shadow: {
            width: 1
        },
        round: true,
        series: [{value: 0}],
        center: []
    }

    var settingsPC = {
        diameter: 120,
        stroke: {
            width: 15,
            gap: 2
        },
        shadow: {
            width: 1
        },
        round: true,
        max: 100,
        series: [
            {
                value: 0,
                // if specifying a background is not necessary you can use these shortcuts
                color: '#4caf50'
            }
        ],
        // simple center text
        center: {
            content: [function(p) {
                         return p + ' %'
            }, 'complete']
        }
    }

    $.get( "/get-task-info")
        .done(function(data) {
            for (var key in data) {
                if (data[key][5] == '1') {
                    $('#switch-'+key).hide();
                    $('.task-message-'+key).html('Task starts on ' + data[key][0] + ' at ' + data[key][1]);
                    continue;
                }
                if (data[key][5] == '2') {
                    $('.task-alert-'+key).html('Task has exceeded Expected Finish Date');
                    continue;
                }

                if (data[key][3] > 0) {
                    settingsPB['max'] = data[key][4]
                    settingsPB['series'][0]['color'] = '#f44336'
                    settingsPB['center'] = [function(value) {return (value + ' Hrs')}, 'spent']
                    var chart1 = new RadialProgressChart('.pb-container-'+key, settingsPB);
                    chart1.update(data[key][1])
                } else {
                    settingsPB['max'] = data[key][0]
                    settingsPB['series'][0]['color'] = '#0277bd'
                    settingsPB['center'] = [function(value) {return (value + ' Hrs')}, 'spent']
                    var chart2 = new RadialProgressChart('.pb-container-'+key, settingsPB);
                    chart2.update(data[key][1])
                }

                var chart3 = new RadialProgressChart('.pc-container-'+key, settingsPC);
                if (data[key][2] != null) {
                    chart3.update(data[key][2]);
                }
                if (data[key][2] == null) {
                    chart3.update(0.1);
                }
            }
        })
        .fail(function() {
            console.log('An error occurred')
        })
}