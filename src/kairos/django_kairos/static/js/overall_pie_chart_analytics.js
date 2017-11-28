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

  var pie = new d3pie("pieChart", {
header: {
  title: {
    text: "A Simple Donut Pie"
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

});


}); // End of $(document).ready
