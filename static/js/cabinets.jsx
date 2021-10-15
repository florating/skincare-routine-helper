"use strict";

const { checkPropTypes } = require("prop-types");

function GenericButton(props) {
    function addToCabinet() {
        console.log("Add to cabinet!")
    }

    return (
        <React.Fragment>
            <button id="add-to-cabinet-button" onClick={}>
                {props.message}
            </button>
        </React.Fragment>
    )
}



ReactDOM.render(<GenericButton message="Add to Cabinet" action="#" />, document.querySelector('#add-to-cabinet'));
