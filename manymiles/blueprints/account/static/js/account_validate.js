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
 * [validatePassword description]
 * Determines whether or not the provided password is valid. The function
 * requires that the password has at least 7 characters, one character is a
 * number, one character is lowercase, one character is uppercase, and one
 * character is a special character.
 * @param   {String}    password    The password to validate.
 * @return  {Boolean}               Whether or not the password is valid.
 */
function validatePassword(password) {
    return (
        /[A-Z]/.test(password)
        && /[a-z]/.test(password)
        && /[0-9]/.test(password)
        && /[^A-za-z0-9]/.test(password)
        && password.length >= 7
    );
}

/**
 * [validateUpdateEmailForm description]
 * Adds event listeners to the appropriate inputs on the page that changes
 * their "aria-invalid" attributes according to their values' validity.
 */
function validateUpdateEmailForm() {

    // Get handles to the form submission button
    const submitButton = document.getElementById("submit-modal-change-email");
    // Get handles to the email inputs
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

/**
 * [validateUpdatePasswordForm description]
 * Adds event listeners to the appropriate inputs on the page that changes
 * their "aria-invalid" attributes according to their values' validity.
 */
function validateUpdatePasswordForm() {

    // Get handles to the form submission button
    const submitButton = document.getElementById("submit-modal-change-password");
    // Get handles to the password inputs
    const newPassword = document.getElementById("new-password-input");
    const confirmPassword = document.getElementById("confirm-password-input");
    // Create an array of these two password inputs
    const passwordInputs = [newPassword, confirmPassword];
    // Create an array of all required inputs
    const requiredInputs = passwordInputs;

    // Add an event listener to each password input
    passwordInputs.forEach((passwordInput) => {
        passwordInput.addEventListener(
            "input",
            function() {
                // Get the values of each password input
                const newValue = newPassword.value;
                const confirmValue = confirmPassword.value;

                // Determine if the values match
                const valuesMatch = (newValue == confirmValue);
                // Determine if both passwords are valid
                const valuesValid = (
                    validatePassword(newValue) && validatePassword(confirmValue)
                );

                // Modify the appropriate attribute for the "new" input
                if (!newValue) {
                    newPassword.removeAttribute("aria-invalid");
                } else if (validatePassword(newValue)) {
                    newPassword.setAttribute("aria-invalid", "false");
                } else {
                    newPassword.setAttribute("aria-invalid", "true");
                }

                // Modify the appropriate attribute for the "confirm" input
                if (!confirmValue) {
                    confirmPassword.removeAttribute("aria-invalid");
                } else if (valuesValid && valuesMatch) {
                    confirmPassword.setAttribute("aria-invalid", "false");
                } else {
                    confirmPassword.setAttribute("aria-invalid", "true");
                }
            }
        );
    });

    // Add an event listener to the submit button
    requiredInputs.forEach((requiredInput) => {
        requiredInput.addEventListener(
            "input",
            function() {
                // Get the values of each required input
                const newValue = newPassword.value;
                const confirmValue = confirmPassword.value;

                // Determine if the values match
                const valuesMatch = (newValue == confirmValue);
                // Determine if both passwords are valid
                const valuesValid = (
                    validatePassword(newValue) && validatePassword(confirmValue)
                );

                // Toggle the submit button depending on the form's validity
                if (valuesValid && valuesMatch) {
                    submitButton.disabled = false;
                } else {
                    submitButton.disabled = true;
                }
            }
        );
    });
}

// Call the functions
validateUpdateEmailForm()
validateUpdatePasswordForm()