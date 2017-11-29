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
    console.log("hi");
    $("#pieChart").append("<h7>There is no task finished yet. Consider finishing a task first to show the analytics</h7>");
  } else {
    var pie = new d3pie("pieChart", {
  header: {
    title: {
      text: "on time vs late"
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
