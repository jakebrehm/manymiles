/**
 * [validateNewRecord description]
 * Dynamically updates the fields on the form that allows a user to create a new
 * record. Invalid values in the input fields will result in the submit button
 * being disabled.
 */
function validateNewRecord() {

    // Get handles to the timestamp and mileage inputs
    const timestampInput = document.getElementById("timestamp");
    const mileageInput = document.getElementById("mileage");
    // Get a handle to the submit button
    const submitButton = document.getElementById("submit-new-record");
    // Create an array of all required inputs
    const requiredInputs = [timestampInput, mileageInput];

    // Add an event listener to the timestamp input
    timestampInput.addEventListener(
        "input",
        function () {
            // Get the value of the timestamp input
            const timestampValue = timestampInput.value;

            // Set the state of the input according to the its validity
            if (timestampValue) {
                timestampInput.setAttribute("aria-invalid", "false");
            } else {
                timestampInput.removeAttribute("aria-invalid");
            }
        }
    );

    // Add an event listener to the mileage input
    mileageInput.addEventListener(
        "input",
        function () {
            // Get the value of the mileage input
            const mileageValue = mileageInput.value;

            // Set the state of the input according to the its validity
            if (!mileageValue) {
                mileageInput.removeAttribute("aria-invalid");
            } else if (mileageValue < 0) {
                mileageInput.setAttribute("aria-invalid", "true");
            } else {
                mileageInput.setAttribute("aria-invalid", "false");
            }
        }
    );

    // Add an event listener to each input to determine overall validity
    requiredInputs.forEach((requiredInput) => {
        requiredInput.addEventListener(
            "input",
            function () {
                // Get the values of each input
                const timestampValue = timestampInput.value;
                const mileageValue = mileageInput.value;

                if (timestampValue && mileageValue && (mileageValue >= 0)) {
                    submitButton.disabled = false;
                } else {
                    submitButton.disabled = true;
                }
            }
        );
    });

}

/**
 * [validateFilter description]
 * Dynamically updates the fields on the form that allows a user to filter their
 * records. Invalid values in the input fields will result in the submit button
 * being disabled.
 */
function validateFilter() {
    // Get handles to the filters
    const fromTimestampInput = document.getElementById("from-timestamp");
    const toTimestampInput = document.getElementById("to-timestamp");
    // Get a handle to the submit button
    const applyButton = document.getElementById("apply-button");
    // Create an array of all the timestamp filters
    const timestampInputs = [fromTimestampInput, toTimestampInput];

    // Add an event listener to each input to determine overall validity
    timestampInputs.forEach((timestampInput) => {
        timestampInput.addEventListener(
            "input",
            function () {
                // Get the values of each filter
                const fromTimestampValue = fromTimestampInput.value;
                const toTimestampValue = toTimestampInput.value;
                // Determine if both fields are filled out
                const timestampsFilled = fromTimestampValue && toTimestampValue;
                // Determine if the "from" timestamp is less than the "to"
                const fromLessThan = fromTimestampValue <= toTimestampValue;

                // Enable or disable the apply button accordingly
                if (timestampsFilled && !fromLessThan) {
                    fromTimestampInput.setAttribute("aria-invalid", "true");
                    toTimestampInput.setAttribute("aria-invalid", "true");
                    applyButton.disabled = true;
                } else {
                    fromTimestampInput.removeAttribute("aria-invalid");
                    toTimestampInput.removeAttribute("aria-invalid");
                    applyButton.disabled = false;
                }
            }
        );
    });
}

/**
 * [validateUpdateForm description]
 * Dynamically updates the fields on the form that allows a user to update a
 * record. Invalid values in the input fields will result in the submit button
 * being disabled.
 */
function validateUpdateForm() {
    // Define the template used to identify each dialog and its buttons
    const template = "modal-update-";
    // Get handles to each update dialog
    const updateDialogs = document.querySelectorAll(`[id^='${template}']`);

    updateDialogs.forEach((updateDialog) =>{
        // Get the unique identifier for each dialog
        const identifier = updateDialog.id.replace(template, "");

        // Get handles to each element
        const timestampInput = document.getElementById(
            `update-timestamp-${identifier}`
        );
        const mileageInput = document.getElementById(
            `update-mileage-${identifier}`
        );

        const submitButton = document.getElementById(
            `submit-update-record-${identifier}`
        );

        // Create an array of required inputs
        const requiredInputs = [timestampInput, mileageInput];

        // Add an event listener to the timestamp input
        timestampInput.addEventListener(
            "input",
            function () {
                // Get the value of the timestamp input
                const timestampValue = timestampInput.value;

                // Set the state of the input according to the its validity
                if (timestampValue) {
                    timestampInput.setAttribute("aria-invalid", "false");
                } else {
                    timestampInput.removeAttribute("aria-invalid");
                }
            }
        );

        // Add an event listener to the mileage input
        mileageInput.addEventListener(
            "input",
            function () {
                // Get the value of the mileage input
                const mileageValue = mileageInput.value;
                
                // Set the state of the input according to the its validity
                if (!mileageValue) {
                    mileageInput.removeAttribute("aria-invalid");
                } else if (mileageValue < 0) {
                    mileageInput.setAttribute("aria-invalid", "true");
                } else {
                    mileageInput.setAttribute("aria-invalid", "false");
                }
            }
        );

        // Add an event listener to each input to determine overall validity
        requiredInputs.forEach((requiredInput) => {
            requiredInput.addEventListener(
                "input",
                function () {
                    // Get the values of each input
                    const timestampValue = timestampInput.value;
                    const mileageValue = mileageInput.value;

                    if (timestampValue && mileageValue && (mileageValue >= 0)) {
                        submitButton.disabled = false;
                    } else {
                        submitButton.disabled = true;
                    }
                }
            );
        });
    });
}

// Call each function
validateNewRecord()
validateFilter()
validateUpdateForm()