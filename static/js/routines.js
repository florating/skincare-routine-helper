"use strict";

$( () => {
    $("#draggable").draggable({
        connectToSortable: "#sortable",
        helper: "clone",
        revert: "invalid"
    });
    $(".routine ul, .routine li").disableSelection();
});

$( () => {
    $( "#sortable" ).sortable();
  }
);

let BEGINNER_ROUTINE = {
  9: "Cleanser",
  1: "Moisturizer",
  16: "Sun Protection",
};


// TODO: Test and fix, alongside this route in server.py.
$.post('/get_cabinet', '', (res) => {
  console.log(res);
  const cabinet_list = res.cabinet;
  console.log(`cabinet_list = ${cabinet_list}`);
  console.log(`cabinet_list[0] = ${cabinet_list[0]}`);
  console.log(`cabinet_list[0].product_id = ${cabinet_list[0].product_id}`);
  const categories_dict = res.cat_dict[0];
  console.log(`categories_dict = ${categories_dict}`);

  let NUM = 10;
  

  // AM ROUTINE:
  for (const [key, value] of Object.entries(BEGINNER_ROUTINE)) {
    $(".am-routine #sortable").append(`
      <li class="ui-state-default category_id_${key}">
        TEST ${value}:
        <select name="${key}" class="category_id_${key}">
          <option val="">--Select--</option>
        </select>
      </li>`
    );
  };

  for (const cab_obj of cabinet_list) {
    let cat_id = cab_obj.category_id;
    $(`select.category_id_${cat_id}`).append(`
      <option val="${cat_id}">${cab_obj.product_name}</option>
    `);
  };
  
  // for (const [key, value] of Object.entries(BEGINNER_ROUTINE)) {
  //   console.log(`key = ${key}, value = ${value}`)
  //   $(`select.category_id_${NUM}`).append(`
  //     <option val="${NUM}">${key}, ${value}</option>
  //   `);
  // }
  
});
