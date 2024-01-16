/**
 * [validateEmail description]
 * Determines whether or not the email is valid.
 * @param   {String}    email       The email to validate.
 * @return  {Boolean}               Whether or not the email is valid.
 */
function validateEmail(email) {
    return /^[a-z0-9]+([\._]?[a-z0-9]+)*[@]\w+[.]\w{2,3}$/.test(email);
}

/**
 * [validateForm description]
 * Adds event listeners to the appropriate inputs on the page that changes
 * their "aria-invalid" attributes according to their values' validity.
 */
function validateForm() {

    // Get handles to the form submission button
    const submitButton = document.getElementById("submit-modal-change-email");
    // Get handles to the username and email inputs
    const email = document.getElementById("new-email-input");

    // Add an event listener to the email input
    email.addEventListener(
        "input",
        function() {
            // Get the value of the email input
            const emailValue = email.value;

            // Modify the validity attribute for the email input
            if (!emailValue) {
                email.removeAttribute("aria-invalid");
            } else if (validateEmail(emailValue)) {
                email.setAttribute("aria-invalid", "false");
            } else {
                email.setAttribute("aria-invalid", "true");
            }
        }
    );

    // Add an event listener to the submit button
    email.addEventListener(
        "input",
        function() {
            // Get the values of each required input
            const emailValue = email.value;
            
            // Toggle the submit button depending on the form's validity
            if (validateEmail(emailValue)) {
                submitButton.disabled = false;
            } else {
                submitButton.disabled = true;
            }
        }
    );
}

// Call the function
validateForm()