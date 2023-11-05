/**
 * [showPasswords description]
 * Makes the password field on the page visible to the user.
 */
function showPasswords() {
    // Get handles to each of the password inputs
    const passwordInput = document.getElementById("password-input");

    // Switch between text and password inputs
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
    } else {
        passwordInput.type = "password";
    };
}