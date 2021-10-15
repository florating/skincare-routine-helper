"use strict";

$("#add_to_cabinet").on("submit", (evt) => {
    evt.preventDefault();
    // const data = $("input #product_id").serializeArray();
    // or...
    let product_id_pojo = {}
    $("input #product_id").each((index, el) => {
        product_id_pojo[index] = el.value();
    });
    $.post("/add_to_cabinet", product_id_pojo, () => {
        console.log("Success!")
    });
});