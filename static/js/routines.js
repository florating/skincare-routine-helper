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
  for (const [categoryId, categoryName] of Object.entries(routine)) {
    /*  EXAMPLE:
      <li class="ui-state-default" name="9">Cleanser:</li>
      <select class="category_id_9" name="product_id">
    */

    $(`div.${am_or_pm}-routine .sortable`).append(`
      <li class="ui-state-default step" data-routine-type="${am_or_pm}" data-category-id="${categoryId}" name="${categoryId}" id="${am_or_pm}_routine-category_id_${categoryId}">
        TEST ${categoryName}:
        <select class="category_id_${categoryId}" data-category-id="${categoryId}" name="product_id">
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

function add_cabinet_options(cabinetArray) {
  /*  EXAMPLE:
    <option class="dropdown-item" value="716">
      COSRX Low pH Good Morning Cleanser
    </option>
  */
  for (const cabObj of cabinetArray) {
    const catId = cabObj.category_id;
    const prodId = cabObj.product_id;
    const prodName = cabObj.product_name;
    $(`select.category_id_${catId}`).append(`
      <option class="dropdown-item" data-category-id="${catId}" data-product-id="${prodId}" value="${prodId}">
        ${prodName}
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

  /* CHECK IF CURRENT USER HAS ANY ROUTINES */

  /* IF YES, LOAD STEPS PER ROUTINE */
  // create_routine_steps('am', current_user.routine.routine_id);
  // $("div.am-routine ul.steps").append(
  //   '<li></li>'
  // );

  /* CREATING ROUTINES FROM SCRATCH */

  // TODO: Test and fix, alongside this route in server.py.
  // Do this if the user needs to create new skincare routines from scratch!
  $("#create-am-routine").on("click", () => {
    console.log(`I just clicked the "Create AM Routine" button.`)
    $.post('/get_cabinet', '', (res) => {
      console.log(res);
      const cabinetArray = res.cabinet;  // should I make this a global variable?
      // console.log(`cabinetArray = ${cabinetArray}`);
      // console.log(`cabinetArray[0] = ${cabinetArray[0]}`);
      console.log(`cabinetArray[0].product_id = ${cabinetArray[0].product_id}`);
      const categoriesDict = res.cat_dict[0];
      console.log(`categoriesDict = ${categoriesDict}`);

      // AM ROUTINE:
      generate_complete_routine("am", cabinetArray, BEGINNER_ROUTINE);

      // PM ROUTINE:
      generate_complete_routine("pm", cabinetArray, BEGINNER_ROUTINE);
      add_cabinet_options(cabinetArray);
    });

  });


  // TODO: save the order of the skincare routine in the updated ORM class for routines
  $("#submit-am-routine").on("click", (evt) => {
    evt.preventDefault();
    console.log("%cI hit the save button, success!", "color:blue;");

    let amForm = document.getElementById("form-am-routine");
    const routine_steps = [];
    // const formData = {
    //   routine_type: "am",
    //   steps: routine_steps,
    // };
    // console.log("Creating formData...");
    // console.log(formData);
    // for (let step of amForm.elements) {
    //   console.log("In the for loop, step is now:")
    //   console.log(step);
    //   if (step.value > 0) {
    //     routine_steps.push({
    //       category_id: step.dataset.categoryId,
    //       product_id: step.value,
    //     });
    //   }
    //   console.log("formData is...")
    //   console.log(formData);
    // }
    const formData = $(amForm).serializeArray();
    for (let step of formData) {
      if (step.value !== "") {
      routine_steps.push(step.value)
      }
    }
    // const amSteps = document.querySelectorAll('div.am-routine li.step');
    // for (let step of amSteps) {
    //   let catId = step.dataset.categoryId;
    //   console.log("catId: ", catId);
    //   console.log($(step).attr("name"));
    //   $(`.am-routine select.`)
    // }
    // console.table(amSteps);

    // const routine_steps = [];
    // $("div.am-routine li").each((index, li_el) => {

    //   console.log("li_el is below:");
    //   console.log(li_el);

    //   const stepObj = {};
    //   stepObj["category_id"] = $(li_el).attr("name");
    //   console.log("category_id");
    //   console.log(stepObj["category_id"]);

    //   const select_obj = $(`.am-routine select.category_id_${stepObj["category_id"]}`);
    //   //   console.log("select_obj");
    //   //   console.log(select_obj);

    //   stepObj["product_id"] = $(select_obj).val();
    //   console.log("product_id");
    //   console.log(stepObj["product_id"]);

    //   console.log("stepObj is below:");
    //   console.log(stepObj);

    //   if (stepObj["product_id"] !== "" && stepObj["product_id"] !== undefined) {
    //     console.log("The product_id was valid.");
    //     routine_steps.push(stepObj);
    //   } else {
    //     console.log("The product_id was invalid.")
    //   }
    // });

    console.log("Now routine_steps looks like this:")
    console.log(routine_steps);

    // let form_data = {
    //   routine_type: "am",
    //   steps: routine_steps,
    // };

    // console.log("Here is the form_data variable!")
    // console.log(form_data);

    // console.log(`form_data["steps"]`);
    // console.log(form_data["steps"]);
    console.log(formData);
    
  
    if (routine_steps.length === 0) {

    // if (formData["steps"].length === 0) {
      alert("Uh oh! You didn't select any products for this skincare routine.");
    }
    else {
      const form_data = {routine_type: 'am', steps: routine_steps};
      console.log("form_data is...")
      console.log(form_data);
      // form_data_1 = {routine_type: 'am', steps: routine_steps}
      // don't send arrays
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
