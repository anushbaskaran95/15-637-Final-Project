$(document).ready(function(){
    getCourseData();
});

function getCourseData() {
    time_per_course = [];
    total_time = 0;
    $.get( "/get-course-analytics")
        .done(function(data) {
            if (!$.isEmptyObject(data['time_per_course'])) {
                for (var x in data['time_per_course']) {
                    time_per_course.push({'course':x, 'time': data['time_per_course'][x] });
                }
                delete data['time_per_course'];
                total_time = data['total_time_courses'];
                delete data['total_time_courses'];
                plotCourseTimes(time_per_course);
                for (var x in data) {
                    plotTaskTimes(data[x], data[x][0]['course_id']);
                }
            } else {
                $('.chart-heading').html('No Course Tasks have been added');
            }
        })
        .fail(function() {
            console.log('An error occurred')
        })
}

function plotCourseTimes(data) {
    courses = data.map(function(t) {
                return t.course
              });
    $('.chart-heading').html('Time Spent per Course')

    var margin = {top: 5, right: 5, bottom: 100, left: 70};
    // here, we want the full chart to be 700x200, so we determine
    // the width and height by subtracting the margins from those values
    var fullWidth = 350;
    var fullHeight = 450;
    // the width and height values will be used in the ranges of our scales
    var width = fullWidth - margin.right - margin.left;
    var height = fullHeight - margin.top - margin.bottom;
    var svg = d3.select('.time_per_course').append('svg')
        .attr('width', fullWidth)
        .attr('height', fullHeight)
        // this g is where the bar chart will be drawn
        .append('g')
        // translate it to leave room for the left and top margins
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    // use the width and height defined above
    var courseScale = d3.scaleBand()
                       .domain(courses)
                       .range([1, width])
                       // allow for some padding between bars
                       .paddingInner(0.1);

    var timeScale = d3.scaleLinear()
                      .domain([0, d3.max(data, function(d) { return d.time; })])
                      .range([height, 0])
                      // use nice to round the domain values to nice numbers
                      .nice();

    var bandwidth = courseScale.bandwidth();

    var xAxis = d3.axisBottom(courseScale);
    var yAxis = d3.axisLeft(timeScale);

    // add the axes to your chart
    var xAxisEle = svg.append('g')
      .classed('x axis', true)
      // a horizontal axis is rendered at y=0, so the axis needs to be translated
      // down to the bottom of the chart
      .attr('transform', 'translate(0,' + height + ')')
      .style("font-size", 15)
      // call the axis function on the selection
      .call(xAxis)
      .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("transform", "rotate(-35)");

    var yAxisEle = svg.append('g')
                      .classed('y axis', true)
                      .call(yAxis);

    var yText = yAxisEle.append('text')
                        .attr('transform', 'rotate(-90)translate(-' + height/2 + ',0)')
                        .style('text-anchor', 'middle')
                        .style('fill', 'black')
                        .attr('dy', '-3em')
                        .style('font-size', 15)
                        .text('Hours');

    var barHolder = svg.append('g')
      .classed('bar-holder', true);

    // draw the bars
    var bars = barHolder.selectAll('rect.bar')
             .data(data)
             .enter().append('rect')
             .classed('bar', true)
             .attr('x', function(d, i) {
                return courseScale(d.course)
             })
             .attr('y', function(d) {
                return height - timeScale(d.time);
             })
            .attr('width', bandwidth)
            .attr('fill', '#00bcd4')
            .transition()
                .duration(700)
                .ease(d3.easeLinear)
                .attr('height', function(d) {
                    // the bar's height should align it with the base of the chart (y=0)
                    return height - timeScale(d.time);
                })
                .attr('y', function(d) {
                    return timeScale(d.time);
                });
}


function plotTaskTimes(data, id) {
    tasks = data.map(function(t) {
                return t.task_name
              });

    var margin = {top: 5, right: 5, bottom: 100, left: 70};
    // here, we want the full chart to be 700x200, so we determine
    // the width and height by subtracting the margins from those values
    var fullWidth = 350;
    var fullHeight = 450;
    // the width and height values will be used in the ranges of our scales
    var width = fullWidth - margin.right - margin.left;
    var height = fullHeight - margin.top - margin.bottom;
    var svg = d3.select('.course_'+id).append('svg')
        .attr('width', fullWidth)
        .attr('height', fullHeight)
        // this g is where the bar chart will be drawn
        .append('g')
        // translate it to leave room for the left and top margins
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    // use the width and height defined above
    var taskScale = d3.scaleBand()
                       .domain(tasks)
                       .range([1, width])
                       // allow for some padding between bars
                       .paddingInner(0.1);

    var timeScale = d3.scaleLinear()
                      .domain([0, d3.max(data, function(d) { return d.time_spent; })])
                      .range([height, 0])
                      // use nice to round the domain values to nice numbers
                      .nice();

    var bandwidth = taskScale.bandwidth();

    var xAxis = d3.axisBottom(taskScale);
    var yAxis = d3.axisLeft(timeScale);

    // add the axes to your chart
    var xAxisEle = svg.append('g')
      .classed('x axis', true)
      // a horizontal axis is rendered at y=0, so the axis needs to be translated
      // down to the bottom of the chart
      .attr('transform', 'translate(0,' + height + ')')
      .style("font-size", 15)
      // call the axis function on the selection
      .call(xAxis)
      .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("transform", "rotate(-35)");

    var yAxisEle = svg.append('g')
                      .classed('y axis', true)
                      .call(yAxis);

    var yText = yAxisEle.append('text')
                        .attr('transform', 'rotate(-90)translate(-' + height/2 + ',0)')
                        .style('text-anchor', 'middle')
                        .style('fill', 'black')
                        .attr('dy', '-3em')
                        .style('font-size', 15)
                        .text('Hours');

    var barHolder = svg.append('g')
      .classed('bar-holder', true);

    // draw the bars
    var bars = barHolder.selectAll('rect.bar')
             .data(data)
             .enter().append('rect')
             .classed('bar', true)
             .attr('x', function(d, i) {
                return taskScale(d.task_name)
             })
             .attr('y', function(d) {
                return height - timeScale(d.time_spent);
             })
            .attr('width', bandwidth)
            .attr('fill', '#00bcd4')
            .transition()
                .duration(700)
                .ease(d3.easeLinear)
                .attr('height', function(d) {
                    // the bar's height should align it with the base of the chart (y=0)
                    return height - timeScale(d.time_spent);
                })
                .attr('y', function(d) {
                    return timeScale(d.time_spent);
                });
}