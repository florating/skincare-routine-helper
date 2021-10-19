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


// TODO: Test and fix, alongside this route in server.py.
$.post('/get_cabinet', '', (res) => {
  console.log(res);
});