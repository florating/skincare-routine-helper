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
          `translate(${margin.left}, ${margin.top})`);

// Add a tooltip (not working...)
const tooltip = d3.select("body")
  .append("div")
  .attr("class", "toolTip");
tooltip
  .style("position", "absolute")
  .style("z-index", "10")
  .style("visibility", "hidden")
  .style("background", "#000")
  .text("a simple tooltip");

// Initialize the X axis (for the buttons)
const x = d3.scaleLinear()
  .range([0, width]);
const xAxis = svg.append("g")
  .attr("transform", `translate(0, ${height})`);
  // .attr("class", "myXaxis");

// Initialize the Y axis (for the buttons)
const y = d3.scaleBand()
  .range([height, 0])
  .padding(1);
const yAxis = svg.append("g")
  

// Parse the Data
const realFile = "/static/files/db_summary.csv";
const testFile = "https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/7_OneCatOneNum_header.csv";

function update(selectedVar) {
  d3.csv(realFile, (error, data) => {
    if (error) throw error;

    // sort data
    // data.sort((b, a) => {
    //   return a[selectedVar] - b[selectedVar];
    // });

    // Set X axis 
    x.domain([0, d3.max(data, (d) => { return +d[selectedVar] }) ]);
    xAxis
    .transition()
    .duration(1000)
    .call(d3.axisBottom(x))
    .selectAll("text")
    .attr("transform", "translate(-10,0)rotate(-45)")
    .style("text-anchor", "end");

    // Y axis
    y.domain(data.map((d) => { return d.category_name; }));
    yAxis.transition().duration(1000).call(d3.axisLeft(y))

    // append the lines (starting at x=0) to the svg element
    const j = svg.selectAll(".myline")
      .data(data)

    // update lines
    j
      .enter().append("line").attr("class", "myLine")
      // .merge(j)
      .transition()
      .duration(1000)
        .attr("x1", x(0))
        .attr("x2", (d) => { return x(d[selectedVar]); })
        .attr("y1", (d) => { return y(d.category_name); })
        .attr("y2", (d) => { return y(d.category_name); })
        .attr("stroke", "grey")

    // append the circles (starting at x=0) to the svg element
    const u = svg.selectAll("mycircle")
      .data(data)
    
    u
      .enter()
      .append("circle")
      .merge(u)
      .transition()
      .duration(1000)
      .attr("cx", (d) => { return x(d[selectedVar]); })
      .attr("cy", (d) => { return y(d.category_name); })
      .attr("r", "8")
      .style("fill", "rgba(63, 127, 191, 0.8)")
      // .attr("stroke", "black")
    
    // removed data
    j.exit().remove();
    u.exit().remove();


    // d3.select("body")
    // .selectAll("div")
    //   .data(data)
    // .enter()
    // .append("div")
    //   .style("width", (d) => { return x(d) + "px"; })
    //   .text((d) => { return d; })
    //   .on("mouseover", (d) => {
    //     console.log("Found it on mouseover!")
    //     tooltip.text(d);
    //     return tooltip.style("visibility", "visible");
    //   })
    //   .on("mousemove", () => {
    //     return tooltip
    //       .style("top", (d3.event.pageY-10)+"px")
    //       .style("left",(d3.event.pageX+10)+"px");
    //   })
    //   .on("mouseout", () => {
    //     return tooltip.style("visibility", "hidden");
    //   });


  })

}

update("num_products")
