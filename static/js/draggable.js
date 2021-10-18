"use strict";

$( () => {
    $("#draggable").draggable({
        connectToSortable: "#sortable",
        helper: "clone",
        revert: "invalid"
    });
    $("ul, li").disableSelection();
});

$( () => {
    $( "#sortable" ).sortable();
  } );