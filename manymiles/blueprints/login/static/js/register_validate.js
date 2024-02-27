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
 * [validateForm description]
 * Adds event listeners to the inputs on the page that changes their respective
 * "aria-invalid" attributes according to their values' validity.
 */
function validateForm() {

    // Get handles to the form submission button
    const submitButton = document.getElementById("submit-button");
    // Get handles to the username and email inputs
    const username = document.getElementById("username-input");
    const email = document.getElementById("email-input");
    // Get handles to each of the name inputs
    const firstName = document.getElementById("first-name-input");
    const lastName = document.getElementById("last-name-input");
    // Get handles to each of the password inputs
    const newPassword = document.getElementById("new-password-input");
    const confirmPassword = document.getElementById("confirm-password-input");
    // Create an array of the two name inputs
    const nameInputs = [firstName, lastName];
    // Create an array of the two password inputs
    const passwordInputs = [newPassword, confirmPassword];
    // Create an array of all required inputs
    const allInputs = [
        username,
        email,
        firstName,
        lastName,
        newPassword,
        confirmPassword
    ];

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

    // 
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

    // 
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

    // 
    allInputs.forEach((allInput) => {
        allInput.addEventListener(
            "input",
            function() {
                // Get the values of each required input
                const newValue = newPassword.value;
                const confirmValue = confirmPassword.value;
                const firstValue = firstName.value;
                const lastValue = lastName.value;
                const usernameValue = username.value;
                const emailValue = email.value;

                // Determine if the values match
                const valuesMatch = (newValue == confirmValue);
                // Determine if both passwords are valid
                const valuesValid = (
                    validatePassword(newValue) && validatePassword(confirmValue)
                );
                // Determine if the names are valid
                const namesValid = (
                    validateName(firstValue) && validateName(lastValue)
                );
                // Determine if the user information is valid
                const validUserInfo = (
                    validateUsername(usernameValue) && validateEmail(emailValue)
                );

                // Toggle the submit button depending on the form's validity
                if (valuesValid && valuesMatch && namesValid && validUserInfo) {
                    submitButton.disabled = false;
                } else {
                    submitButton.disabled = true;
                }
            }
        );
    });
}

// Call the function
validateForm()