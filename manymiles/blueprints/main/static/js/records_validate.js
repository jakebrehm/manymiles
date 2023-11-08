function validateNewRecord() {

    // Get handles to the timestamp and mileage inputs
    const timestampInput = document.getElementById("timestamp");
    const mileageInput = document.getElementById("mileage");
    // Get a handle to the submit button
    const submitButton = document.getElementById("submit-new-record");
    // Create an array of all required inputs
    const requiredInputs = [timestampInput, mileageInput];

    // 
    timestampInput.addEventListener(
        "input",
        function () {
            // Get the value of the timestamp input
            const timestampValue = timestampInput.value;

            // 
            if (timestampValue) {
                timestampInput.setAttribute("aria-invalid", "false");
            } else {
                timestampInput.removeAttribute("aria-invalid");
            }
        }
    );

    // 
    mileageInput.addEventListener(
        "input",
        function () {
            // Get the value of the mileage input
            const mileageValue = mileageInput.value;

            // 
            if (!mileageValue) {
                mileageInput.removeAttribute("aria-invalid");
            } else if (mileageValue < 0) {
                mileageInput.setAttribute("aria-invalid", "true");
            } else {
                mileageInput.setAttribute("aria-invalid", "false");
            }
        }
    );

    //
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

function validateFilter() {
    // Get handles to the filters
    const fromTimestampInput = document.getElementById("from-timestamp");
    const toTimestampInput = document.getElementById("to-timestamp");
    // Get a handle to the submit button
    const applyButton = document.getElementById("apply-button");
    // Create an array of all the timestamp filters
    const timestampInputs = [fromTimestampInput, toTimestampInput];

    // 
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

                // 
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

//
validateNewRecord()
validateFilter()