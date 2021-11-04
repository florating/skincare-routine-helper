"use strict";

// set the dimensions and margins of the graph
var margin = {top: 30, right: 30, bottom: 70, left: 60},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#my_dataviz")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// Initialize the X axis
var x = d3.scaleBand()
  .range([ 0, width ])
  .padding(1);
var xAxis = svg.append("g")
  .attr("transform", `translate(0, ${height})`)

// Initialize the Y axis
var y = d3.scaleLinear()
  .range([ height, 0]);
var yAxis = svg.append("g")
  .attr("class", "myYaxis")

// Filepaths
const realFile = "/static/files/db_summary.csv";

// A function that create / update the plot for a given variable:
function update(selectedVar) {

  // Parse the Data
  d3.csv(realFile, (data) => {

    // X axis
    x.domain(data.map((d) => { return d.category_name; }))
    xAxis.transition().duration(1000).call(d3.axisBottom(x))

    // Add Y axis
    y.domain([0, d3.max(data, (d) => { return +d[selectedVar] }) ]);
    yAxis.transition().duration(1000).call(d3.axisLeft(y));

    // variable u: map data to existing circle
    var j = svg.selectAll(".myLine")
      .data(data)
    // update lines
    j
      .enter()
      .append("line")
      .attr("class", "myLine")
      .merge(j)
      .transition()
      .duration(1000)
        .attr("x1", (d) => { return x(d.category_name); })
        .attr("x2", (d) => { return x(d.category_name); })
        .attr("y1", (d) => { return y(d[selectedVar]); })
        // .attr("y1", y(0))
        .attr("y2", y(0))
        .attr("stroke", "grey")


    // variable u: map data to existing circle
    var u = svg.selectAll("circle")
      .data(data)
    // update bars
    u
      .enter()
      .append("circle")
      .merge(u)
      .transition()
      .duration(1000)
        .attr("cx", (d) => { return x(d.category_name); })
        .attr("cy", (d) => { return y(d[selectedVar]); })
        // .attr("cy", y(0))
        .attr("r", 8)
        .attr("fill", "#69b3a2");

    // u
    //   .enter()
    //   .merge(u)
    //   .transition()
    //   .duration(2000)
    //   .attr("cy", (d) => { return y(d[selectedVar]); });
      
    // j
    //   .enter()
    //   .merge(j)
    //   .transition()
    //   .duration(2000)
    //   .attr("y1", (d) => { return y(d[selectedVar]); });
  })

}

// Initialize plot
update("num_products")
