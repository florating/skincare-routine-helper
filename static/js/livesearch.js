"use strict";

$( () => {
  $("#livebox").on("input", (evt) => {
    $("#datalist").empty();

    let form_data = {
      text:$("#livebox").val(),
      order_by:$("#order_by").val(),
      limit:10,
    };

    $.post("/livesearch", form_data, (res) => {
      console.log(res);
      // console.log(`res.json = ${res.json}`);
      $("#datalist").prepend("<h3>Results:</h3><ul></ul>");
      $("#datalist ul").append(`
        <li>
        <a href="/products/${res.product_id}" target="_blank">
          ${res.product_name}
        </a></li>`
      );

      // $.each(res, (index, value) => {
      //   $("#datalist ul").append(`
      //     <li>${value.product_id} - ${value.product_name}</li>`
      //   );
      // });

    });
  });
});
      


    // $.ajax({
    //   method:"post",
    //   url:"/livesearch",
    //   data:{
    //     text:$("#livebox").val(),
    //     order_by:$("#order_by").val(),
    //     limit:10,
    //   },
    //   dataType: "json",
    //   success:(res) => {
    //     $("#datalist").prepend("Results:<ul></ul>");
    //     console.log("Success!");
    //     console.log(`res = ${res}`);

    //     console.log(`res.data = ${res.data}`);

    //     $.each(res, (index, value) => {
    //       $("#datalist ul").append(`
    //         <li>${value.product_id} - ${value.product_name}</li>`
    //       );
    //     });
    //   }
    // });
