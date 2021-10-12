"use strict";

$("#search_for_product").on("submit", (evt) => {
    evt.preventDefault();
    const product_list = evt.response()
    console.log(`evt.data = ${evt.data}`)
    console.log(`evt.response() = ${evt.response()}`)
    for (const prod of product_list) {
        $("#search_results").append(`<li>${prod.product_name} - <a href="/products/${prod.product_id}">details here</a></li>`);
    }
});