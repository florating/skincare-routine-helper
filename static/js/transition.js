"use strict";

/*
THIS TUTORIAL:
https://www.d3-graph-gallery.com/graph/interactivity_transition.html
*/

// Transition for rectangle
d3.select("#my_rect")
  .transition()
  .duration(2000)
  .attr("width", "400")

console.log("Success!")
// Position of the circles on the X axis
let position = [50, 100, 150, 200, 250, 300, 350]

// Add circles at the top
d3.select("#dataviz_delay")
  .selectAll("mycircles")
  .data(position)
  .enter()
  .append("circle")
    .attr("cx", function(d){return d} )
    .attr("cy", 40)
    .attr("r", 10)

// Animation: put them down one by one:
function triggerTransitionDelay() {
  console.log("D3 is doing something!")
  d3.selectAll("circle")
    .transition()
    .duration(2000)
    .attr("cy", 300)
    .delay(function(i){return(i*10)})
}

/*
MORE RESOURCES:

Build interactive charts using flask and D3.js
https://towardsdatascience.com/build-interactive-charts-using-flask-and-d3-js-70f715a76f93

Combining Python and D3.js to create dynamic visualization applications
https://towardsdatascience.com/combining-python-and-d3-js-to-create-dynamic-visualization-applications-73c87a494396
*/