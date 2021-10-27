"use strict";

$( () => {
  $("#search-keyword").on("input", (evt) => {
    
    let form_data = {
      text:$("#search-keyword").val(),
      order_by:$("#search-sort-by").val(),
      limit:10,
    };

    if (form_data.text.length < 3) {
      console.log("That's too short.");
      return;
    }

    $("#datalist").empty();

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
    //     text:$("#search-keyword").val(),
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
