//pie chart below
$( document ).ready(function() {  // Runs when the document is ready
  url = "/get-on-time-late-tasks"

  // Initialize empty array

var data = [];

// Get JSON data and wait for the response

d3.json(url, function(error, json) {
  $.each(json, function(d,i){
    data.push({
      label: i.label,
      value: i.value
    })
  })

  if (data[0].value == 0 && data[1].value == 0) {
    $("#pieChart").append("<h7>No task has been finished yet. Finished tasks will be used to display the analytics</h7>");
  } else {
    var pie = new d3pie("pieChart", {
  header: {
    title: {
      text: "On time vs Late"
    },
    location: "pie-center"
  },
  size: {
    pieInnerRadius: "80%"
  },
  data: {
    sortOrder: "label-asc",
    content: data
  }
  });
}


  });

}); // End of $(document).ready
