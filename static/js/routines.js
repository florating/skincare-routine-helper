"use strict";


/* SKINCARE ROUTINES */

const BEGINNER_ROUTINE = {
  9: "Cleanser",
  1: "Moisturizer",
};

const INTERMEDIATE_ROUTINE = {
  9: "Cleanser",
  // ?: "Toner",
  // ?: "Exfoliator",
  1: "Moisturizer",
}

const AM_STEP = {
  16: "Sun Protection",
}


/* GENERATING SKINCARE ROUTINE STEPS */

function add_am_step(routine = AM_STEP) {
  create_routine_steps("am", routine);
}

function create_routine_steps(am_or_pm, routine = BEGINNER_ROUTINE) {
  for (const [key, value] of Object.entries(routine)) {
    /*  EXAMPLE:
      <li class="ui-state-default" name="9">Cleanser:</li>
      <select class="category_id_9" name="product_id">
    */

    $(`div.${am_or_pm}-routine .sortable`).append(`
      <li class="ui-state-default" name="${key}" id="${am_or_pm}_routine-category_id_${key}">
        TEST ${value}:
        <select class="category_id_${key}" name="product_id">
          <option value="">--Select--</option>
        </select>
      </li>`
    );
  };
}


/* GENERATING SKINCARE ROUTINE STEPS + CABINET OPTIONS */

function generate_complete_routine(am_or_pm, cabinet_list, routine = BEGINNER_ROUTINE) {
  create_routine_steps(am_or_pm);
  if (am_or_pm === "am") { add_am_step() }
}


/* GENERATING CABINET OPTIONS for pre-existing steps */

function add_cabinet_options(cabinet_list) {
  /*  EXAMPLE:
    <option class="dropdown-item" value="716">
      COSRX Low pH Good Morning Cleanser
    </option>
  */
  for (const cab_obj of cabinet_list) {
    let cat_id = cab_obj.category_id;
    $(`select.category_id_${cat_id}`).append(`
      <option class="dropdown-item" value="${cab_obj.product_id}">
        ${cab_obj.product_name}
      </option>
    `);
  };
}


/* CODE TO RUN ALL THE TIME */

$(() => {
  $(".sortable").sortable({
    axis: 'y',
    // stop: (evt, ui) => {}
  });

  $(".draggable").draggable({
    connectToSortable: ".sortable",
    // helper: "clone",  // can use this to add a new step, maybe?
    revert: "invalid"
  });
  // $(".routine ul, .routine li").disableSelection();


  /* CREATING ROUTINES FROM SCRATCH */

  // TODO: Test and fix, alongside this route in server.py.
  // Do this if the user needs to create new skincare routines from scratch!
  $("#create-new-routines").on("click", () => {
    console.log(`I just clicked the "Create AM and PM Routines" button.`)
    $.post('/get_cabinet', '', (res) => {
      console.log(res);
      const cabinet_list = res.cabinet;  // should I make this a global variable?
      // console.log(`cabinet_list = ${cabinet_list}`);
      // console.log(`cabinet_list[0] = ${cabinet_list[0]}`);
      console.log(`cabinet_list[0].product_id = ${cabinet_list[0].product_id}`);
      const categories_dict = res.cat_dict[0];
      console.log(`categories_dict = ${categories_dict}`);

      // AM ROUTINE:
      generate_complete_routine("am", cabinet_list, BEGINNER_ROUTINE);

      // PM ROUTINE:
      generate_complete_routine("pm", cabinet_list, BEGINNER_ROUTINE);
      add_cabinet_options(cabinet_list);
    });

  });


  // TODO: save the order of the skincare routine in the updated ORM class for routines
  $("#submit-am-routine").on("click", (evt) => {

    console.log("I hit the save button, success!")
    evt.preventDefault();

    const routine_steps = [];
    $("div.am-routine li").each((index, li_el) => {

      console.log("li_el is below:")
      console.log(li_el);

      const stepObj = {};
      stepObj["category_id"] = $(li_el).attr("name");
      console.log("category_id");
      console.log(stepObj["category_id"]);

      const select_obj = $(`.am-routine select.category_id_${stepObj["category_id"]}`);
      console.log("select_obj");
      console.log(select_obj);

      stepObj["product_id"] = $(select_obj).val();
      console.log("product_id");
      console.log(stepObj["product_id"]);

      console.log("stepObj is below:");
      console.log(stepObj);

      if (stepObj["product_id"] !== "" && stepObj["product_id"] !== undefined) {
        console.log("The product_id was valid.");
        routine_steps.push(stepObj);
      } else {
        console.log("The product_id was invalid.")
      }
    });

    let form_data = {
      routine_type: "am",
      steps: routine_steps,
    };

    console.log("Here is the form_data variable!")
    console.log(form_data);

    console.log(`form_data["steps"]`);
    console.log(form_data["steps"]);

    if (form_data["steps"].length === 0) {
      alert("Uh oh! You didn't select any products for this skincare routine.");
    }
    else {
      $.post("/routine", form_data, (res) => {
        console.log(res);
        // console.log(`res.json = ${res.json}`);
        alert("You have successfully saved your skincare routine!")
        // $("#datalist").prepend("<h3>Results:</h3><ul></ul>");
        // $("#datalist ul").append(`
        //   <li>
        //   <a href="/products/${res.product_id}" target="_blank">
        //     ${res.product_name}
        //   </a></li>`
        // );
  
        // $.each(res, (index, value) => {
        //   $("#datalist ul").append(`
        //     <li>${value.product_id} - ${value.product_name}</li>`
        //   );
        // });
  
      });
    }

    // TODO: LATER... save the order of the skincare routine in the updated ORM class for routines
    // serialize( options )
    // It works by default by looking at the id of each item in the format "setname_number",
    // and it spits out a hash like "setname[]=number&setname[]=number"
    // const data = $("ul.sortable").sortable("serialize", { key: "test_sort" });
    // $("#test-query").text(data);
    // console.log(`data = ${data}`)
  });

  // TODO: look at serialize, serializeArray for jQuery

  // $(document).ready(function () {
  //   $('ul').sortable({
  //     axis: 'y',
  //     stop: function (event, ui) {
  //       var data = $(this).sortable('serialize');
  //       $('span').text(data);
  //       /*$.ajax({
  //               data: oData,
  //           type: 'POST',
  //           url: '/your/url/here'
  //       });*/
  //     }
  //   });
  // });



});
