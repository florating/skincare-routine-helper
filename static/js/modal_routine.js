"use strict";

console.log("Hello!");
$(document).ready( () => {
  console.log("We are in the example event!");
  $("#exampleModal").on("show.bs.modal", function (event) {
    console.log("We are in the example event!");
    // Button that triggered the modal
    var button = event.relatedTarget;
    // Extract info from data-bs-* attributes
    var recipient = button.getAttribute('data-bs-whatever');
    // If necessary, you could initiate an AJAX request here
    // and then do the updating in a callback.
    //
    // Update the modal's content.
    var modalTitle = exampleModal.querySelector('.modal-title');
    var modalBodyInput = exampleModal.querySelector('.modal-body input');
  
    modalTitle.textContent = 'New message to ' + recipient;
    modalBodyInput.value = recipient;
  });
}
);
