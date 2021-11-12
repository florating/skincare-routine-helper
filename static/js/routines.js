"use strict";

/* SKINCARE ROUTINES */

const BEGINNER_ROUTINE = {
  1: "Cleanser",
  9: "Moisturizer",
};

const INTERMEDIATE_ROUTINE = {
  1: "Cleanser",
  4: "Toner",
  2: "Exfoliator",
  6: "Serum",
  9: "Moisturizer",
};

const AM_STEP = {
  12: "Sunscreen",
};

/* GENERATING SKINCARE ROUTINE STEPS */
/*  EXAMPLE:
      <li class="ui-state-default" name="9">Cleanser:</li>
      <select class="category_id_9" name="product_id">
    */
function add_am_step(routine = AM_STEP) {
  create_routine_steps("am", routine);
}

function create_routine_steps(am_or_pm, routine) {
  console.log("Now routine looks like...");
  console.log(routine);
  for (const [categoryId, categoryName] of Object.entries(routine)) {
    $(`div.${am_or_pm}-routine .sortable`).append(`
      <li class="ui-state-default step" data-routine-type="${am_or_pm}" data-category-id="${categoryId}" name="${categoryId}" id="${am_or_pm}_routine-category_id_${categoryId}">
        ${categoryName}:
        <select class="category_id_${categoryId}" data-category-id="${categoryId}" name="product_id">
          <option value="">--Select--</option>
        </select>
      </li>`);
  }
}

/* GENERATING SKINCARE ROUTINE STEPS + CABINET OPTIONS */

function generate_complete_routine(am_or_pm, routine, cabinet_list) {
  if (routine === "BEGINNER_ROUTINE") {
    create_routine_steps(am_or_pm, BEGINNER_ROUTINE);
  } else if (routine === "INTERMEDIATE_ROUTINE") {
    create_routine_steps(am_or_pm, INTERMEDIATE_ROUTINE);
  }
  if (am_or_pm === "am") {
    create_routine_steps(am_or_pm, AM_STEP);
  }
}

/* GENERATING CABINET OPTIONS for pre-existing steps */
/*  EXAMPLE:
    <option class="dropdown-item" value="716">
      COSRX Low pH Good Morning Cleanser
    </option>
  */

function add_cabinet_options(cabinetArray, amOrPm) {
  for (const cabObj of cabinetArray) {
    const catId = cabObj.category_id;
    const prodId = cabObj.product_id;
    const prodName = cabObj.product_name;
    $(`#form-${amOrPm}-routine select.category_id_${catId}`).append(`
      <option class="dropdown-item" data-category-id="${catId}" data-product-id="${prodId}" value="${prodId}">
        ${prodName}
      </option>
    `);
  }
}

/* CODE TO RUN ALL THE TIME */

$(() => {
  $(".sortable").sortable({
    axis: "y",
    // stop: (evt, ui) => {}
  });

  $(".draggable").draggable({
    connectToSortable: ".sortable",
    // helper: "clone",  // can use this to add a new step, maybe?
    revert: "invalid",
  });
  // $(".routine ul, .routine li").disableSelection();

  /* CHECK IF CURRENT USER HAS ANY ROUTINES */

  /* IF YES, LOAD STEPS PER ROUTINE */
  // create_routine_steps('am', current_user.routine.routine_id);
  // $("div.am-routine ul.steps").append(
  //   '<li></li>'
  // );

  /* CREATING ROUTINES FROM SCRATCH */

  $("#create-am-routine").on("click", () => {
    console.log(`I just clicked the "Create AM Routine" button.`);
    $("#create-am-routine").addClass("disabled");
    $.post("/get_cabinet", "", (res) => {
      console.log(res);
      const cabinetArray = res.cabinet; // should I make this a global variable?
      // console.log(`cabinetArray = ${cabinetArray}`);
      // console.log(`cabinetArray[0] = ${cabinetArray[0]}`);
      console.log(`cabinetArray[0].product_id = ${cabinetArray[0].product_id}`);
      const categoriesDict = res.cat_dict[0];
      console.log(`categoriesDict = ${categoriesDict}`);
      let routineLv = document.querySelector(
        'input[name="routine-level"]:checked'
      ).value;
      generate_complete_routine("am", routineLv, cabinetArray);
      add_cabinet_options(cabinetArray, "am");
    });
  });

  $("#create-pm-routine").on("click", () => {
    console.log(`I just clicked the "Create AM Routine" button.`);
    $("#create-pm-routine").addClass("disabled");
    $.post("/get_cabinet", "", (res) => {
      console.log(res);
      const cabinetArray = res.cabinet; // should I make this a global variable?
      // console.log(`cabinetArray = ${cabinetArray}`);
      // console.log(`cabinetArray[0] = ${cabinetArray[0]}`);
      console.log(`cabinetArray[0].product_id = ${cabinetArray[0].product_id}`);
      const categoriesDict = res.cat_dict[0];
      console.log(`categoriesDict = ${categoriesDict}`);

      // PM ROUTINE:
      let routineLv = document.querySelector(
        'input[name="routine-level"]:checked'
      ).value;
      generate_complete_routine("pm", routineLv, cabinetArray);
      add_cabinet_options(cabinetArray, "pm");
    });
  });

  // TODO: save the order of the skincare routine in the updated ORM class for routines
  $("#submit-am-routine").on("click", (evt) => {
    evt.preventDefault();
    console.log("%cI hit the save button, success!", "color:blue;");

    let amForm = document.getElementById("form-am-routine");
    const routine_steps = [];
    const formData = $(amForm).serializeArray();
    for (let step of formData) {
      if (step.value !== "") {
        routine_steps.push(step.value);
      }
    }

    console.log("Now routine_steps looks like this:");
    console.log(routine_steps);

    console.log(formData);

    if (routine_steps.length === 0) {
      // if (formData["steps"].length === 0) {
      alert("Uh oh! You didn't select any products for this skincare routine.");
    } else {
      const form_data = { routine_type: "am", steps: routine_steps };
      console.log("form_data is...");
      console.log(form_data);
      // don't send arrays
      $.post("/routine", form_data, (res) => {
        console.log(res);
        // console.log(`res.json = ${res.json}`);
        // TODO: change this to a flashed message? redirect to refresh the page on success
        alert("You have successfully saved your skincare routine!");
      });
    }
  });

  $("#submit-pm-routine").on("click", (evt) => {
    evt.preventDefault();
    console.log("%cI hit the save button, success!", "color:blue;");

    let pmForm = document.getElementById("form-pm-routine");
    const routine_steps = [];
    const formData = $(pmForm).serializeArray();
    for (let step of formData) {
      if (step.value !== "") {
        routine_steps.push(step.value);
      }
    }

    console.log("Now routine_steps looks like this:");
    console.log(routine_steps);

    console.log(formData);

    if (routine_steps.length === 0) {
      alert("Uh oh! You didn't select any products for this skincare routine.");
    } else {
      const form_data = { routine_type: "pm", steps: routine_steps };
      console.log("form_data is...");
      console.log(form_data);
      // don't send arrays
      $.post("/routine", form_data, (res) => {
        console.log(res);
        // console.log(`res.json = ${res.json}`);
        alert("You have successfully saved your skincare routine!");
      });
    }
  });

  // NOTE: look at serialize, serializeArray for jQuery?
});
