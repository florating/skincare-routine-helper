"use strict";

/*
Tutorial:
https://www.d3-graph-gallery.com/graph/lollipop_ordered.html
*/

// set the dimensions and margins of the graph
const margin = { top: 10, right: 30, bottom: 40, left: 100 },
  width = 460 - margin.left - margin.right,
  height = 500 - margin.top - margin.bottom;

// append the svg object to the body of the page
const svg = d3.select("#my_dataviz")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          `translate(${margin.left},${margin.top})`);

// Add a tooltip (not working...)
const tooltip = d3.select("body")
  .append("div")
  .style("position", "absolute")
  .style("z-index", "10")
  .style("visibility", "hidden")
  .style("background", "#000")
  .text("a simple tooltip");

// Initialize the X axis (for the buttons)
var x = d3.scaleBand()
  .range([ 0, width ])
  .padding(1);
var xAxis = svg.append("g")
  .attr("transform", "translate(0," + height + ")")

// Initialize the Y axis (for the buttons)
var y = d3.scaleLinear()
  .range([ height, 0]);
var yAxis = svg.append("g")
  .attr("class", "myYaxis")

// Parse the Data
const realFile = "/static/files/db_summary.csv";
const testFile = "https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/7_OneCatOneNum_header.csv";

d3.csv(realFile, (error, data) => {
  if (error) throw error;

  // sort data
  data.sort((b, a) => {
    return a.num_products - b.num_products;
  });

  // Add X axis
  const x = d3.scaleLinear()
    .domain([0, 130])
    .range([0, width]);
  svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x))
    .selectAll("text")
    .attr("transform", "translate(-10,0)rotate(-45)")
    .style("text-anchor", "end");

  // Y axis
  const y = d3.scaleBand()
    .range([0, height])
    .domain(data.map((d) => { return d.category_name; }))
    .padding(1);
  svg.append("g")
    .call(d3.axisLeft(y))


  // append the lines (starting at x=0) to the svg element
  svg.selectAll("myline")
    .data(data)
    .enter()
    .append("line")
    .attr("x1", x(0))
    .attr("x2", x(0))
    .attr("y1", (d) => { return y(d.category_name); })
    .attr("y2", (d) => { return y(d.category_name); })
    .attr("stroke", "grey")

  // append the circles (starting at x=0) to the svg element
  svg.selectAll("mycircle")
    .data(data)
    .enter()
    .append("circle")
    .attr("cx", x(0) )
    .attr("cy", (d) => { return y(d.category_name); })
    .attr("r", "7")
    .style("fill", "#69b3a2")
    // .attr("stroke", "black")
  
  // Change the X coordinates of the lines and circles
  svg.selectAll("line")
    .transition()
    .duration(2000)
    .attr("x1", (d) => { return x(d.num_products); })
  
  svg.selectAll("circle")
    .transition()
    .duration(2000)
    .attr("cx", (d) => { return x(d.num_products); })
  
})

d3.select("body")
  .selectAll("div")
    .data(data)
  .enter()
  .append("div")
    .style("width", (d) => { return x(d) + "px"; })
    .text((d) => { return d; })
    .on("mouseover", (d) => {
      console.log("Found it on mouseover!")
      tooltip.text(d);
      return tooltip.style("visibility", "visible");
    })
    .on("mousemove", () => {
      return tooltip
        .style("top", (d3.event.pageY-10)+"px")
        .style("left",(d3.event.pageX+10)+"px");
    })
    .on("mouseout", () => {
      return tooltip.style("visibility", "hidden");
    });
