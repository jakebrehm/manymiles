/**
 * [validateName description]
 * Determines whether or not a name is valid.
 * @param   {String}    name        The name to validate.
 * @return  {Boolean}               Whether or not the email is valid.
 */
function validateName(name) {
    // Validate the length of the name
    const validLength = (name.length <= 64);
    // Validate that all characters are letters
    const nameExpression = /^[A-Za-z\s]*$/;
    const validLetters = nameExpression.test(name);
    // Return whether or not both of these conditions were met
    return (validLength && validLetters) || !name;
}

/**
 * [validateUsername description]
 * Determines whether or not a username is valid.
 * @param   {String}    username    The username to validate.
 * @return  {Boolean}               Whether or not the email is valid.
 */
function validateUsername(username) {
    // Validate the length of the username
    const validLength = (username.length >= 3) && (username.length <= 30);
    // Validate that the first character is a letter
    const usernameExpression = /^[A-Za-z]/;
    const validFirstCharacter = usernameExpression.test(username.charAt(0));
    // Validate that all characters are alphanumeric
    const alphanumericExpression = /^[A-Za-z0-9]*$/;
    const noSpecialCharacters = alphanumericExpression.test(username);
    // Return whether or not both of these conditions were met
    return validLength && validFirstCharacter && noSpecialCharacters;
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
        // Check for uppercase character
        /[A-Z]/.test(password)
        // Check for lowercase character
        && /[a-z]/.test(password)
        // Check for number
        && /[0-9]/.test(password)
        // Check that there is a special character
        && /[^A-za-z\d\W_]/.test(password)
        // Check that the password is at least 7 character long
        && password.length >= 7
    );
}

/**
 * [validateEmail description]
 * Determines whether or not an email is valid.
 * @param   {String}    email       The email to validate.
 * @return  {Boolean}               Whether or not the email is valid.
 */
function validateEmail(email) {
    return /^[a-z0-9]+([\._]?[a-z0-9]+)*[@]\w+[.]\w{2,3}$/.test(email);
}