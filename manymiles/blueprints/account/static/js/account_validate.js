/**
 * [validateUpdateUsernameForm description]
 * Dynamically updates the fields on the form that allows a user to update
 * their username. Invalid values in the input fields will result in the
 * submit button being disabled.
 */
function validateUpdateUsernameForm() {

    // Get handles to the form submission button
    const submitButton = document.getElementById("submit-modal-change-username");
    // Get handles to the username inputs
    const username = document.getElementById("new-username-input");

    // Add an event listener to the username input
    username.addEventListener(
        "input",
        function() {
            // Get the value of the username input
            const usernameValue = username.value;

            // Modify the validity attribute for the username input
            if (!usernameValue) {
                username.removeAttribute("aria-invalid");
            } else if (validateUsername(usernameValue)) {
                username.setAttribute("aria-invalid", "false");
            } else {
                username.setAttribute("aria-invalid", "true");
            }
        }
    );

    // Add an event listener to the submit button
    username.addEventListener(
        "input",
        function() {
            // Get the values of each required input
            const usernameValue = username.value;
            
            // Toggle the submit button depending on the form's validity
            if (validateUsername(usernameValue)) {
                submitButton.disabled = false;
            } else {
                submitButton.disabled = true;
            }
        }
    );
}

/**
 * [validateUpdateNameForm description]
 * Dynamically updates the fields on the form that allows a user to update
 * their first and last name. Invalid values in the input fields will result in
 * the submit button being disabled.
 */
function validateUpdateNameForm() {

    // Get handles to the form submission button
    const submitButton = document.getElementById("submit-modal-change-name");
    // Get handles to the name inputs
    const firstName = document.getElementById("new-first-name-input");
    const lastName = document.getElementById("new-last-name-input");
    // Create an array of all required inputs
    const nameInputs = [firstName, lastName];

    // Add event listeners to each of the name inputs
    nameInputs.forEach((nameInput) => {
        nameInput.addEventListener(
            "input",
            function() {
                // Get the value of the input
                const nameValue = nameInput.value;

                // Determine if the names are valid
                namesValid = validateName(nameValue);

                // Modify the validity attribute for the name input
                if (!nameValue) {
                    nameInput.removeAttribute("aria-invalid");
                } else if (namesValid) {
                    nameInput.setAttribute("aria-invalid", "false");
                } else {
                    nameInput.setAttribute("aria-invalid", "true");
                }
            }
        );
    });

    // Add event listeners to each of the name inputs
    nameInputs.forEach((nameInput) => {
        nameInput.addEventListener(
            "input",
            function() {
                // Get the value of the input
                const firstValue = firstName.value;
                const lastValue = lastName.value;

                // Determine if the names are valid
                namesValid = validateName(firstValue) && validateName(lastValue);

                // Toggle the submit button depending on the form's validity
                if (namesValid) {
                    submitButton.disabled = false;
                } else {
                    submitButton.disabled = true;
                }
            }
        );
    });
}

/**
 * [validateUpdateEmailForm description]
 * Dynamically updates the fields on the form that allows a user to update
 * their email. Invalid values in the input fields will result in the
 * submit button being disabled.
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
 * Dynamically updates the fields on the form that allows a user to update
 * their password. Invalid values in the input fields will result in the
 * submit button being disabled.
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

/**
 * [enableDeleteAccountConfirm() description]
 * Toggles the confirmation button for account deletion a specified number
 * of milliseconds after being called.
 * @param   {Number}    timeout    The number of seconds to wait to toggle.
 */
function enableDeleteAccountConfirm(timeout=5000) {

    // Get handles to the form submission button
    const confirmButton = document.getElementById("confirm-modal-delete-account");
    const confirmHref = document.getElementById("confirm-href-delete-account");

    // Disabled the button to begin
    confirmButton.disabled = true;

    // Disable the functionality of the href
    confirmHref.href = "javascript:void(0);";

    // Re-enable the button after the specified amount of time has passed
    setTimeout(function() {
        confirmButton.disabled = false;
        confirmHref.href = "/account/delete_account";
    }, timeout);
}

// Call the functions
validateUpdateUsernameForm()
validateUpdateNameForm()
validateUpdateEmailForm()
validateUpdatePasswordForm()