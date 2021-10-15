"use strict";

$(document).ready(() => {
  $("#livebox").on("input", (evt) => {
    $("#datalist").empty();
    $.ajax({
      method:"post",
      url:"/livesearch",
      data:{
        text:$("#livebox").val(),
        order_by:$("#order_by").val(),
        limit:10,
      },
      success:(res) => {
        $("#datalist").prepend("Results:<ul></ul>");
        console.log("Success!");
        console.log(`res = ${res}`)
        $.each(res, (index, value) => {
          $("#datalist ul").append(`
            <li>${value.product_id} - ${value.product_name}</li>`
          );
        });
      }
    });
  });  
});