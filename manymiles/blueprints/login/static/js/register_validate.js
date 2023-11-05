/**
 * [showPasswords description]
 * Makes the password fields on the page visible to the user.
 */
function showPasswords() {
    // Get handles to each of the password inputs
    const newPassword = document.getElementById("new-password-input");
    const confirmPassword = document.getElementById("confirm-password-input");
    // Create an array of these two password inputs
    const passwordInputs = [newPassword, confirmPassword];

    // Switch between text and password inputs
    passwordInputs.forEach((passwordInput) => {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
        } else {
            passwordInput.type = "password";
        }
    });
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
 * [validatePasswords description]
 * Adds event listeners to the password inputs on the page that changes
 * their "aria-invalid" attributes according to their values' validity.
 */
function validatePasswordInputs() {

    // Get handles to each of the password inputs
    const newPassword = document.getElementById("new-password-input");
    const confirmPassword = document.getElementById("confirm-password-input");
    // Create an array of these two password inputs
    const passwordInputs = [newPassword, confirmPassword];

    //
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
}

// Call the function
validatePasswordInputs()