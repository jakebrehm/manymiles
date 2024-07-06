/**
 * [fetchData description]
 * Makes a GET request to the provided endpoint and returns the JSON from the
 * response body.
 * @param   {String}    endpoint    The endpoint to make the request to.
 * @returns {Promise}               A promise containing JSON data.
 */
async function fetchData(endpoint) {
    // Make a GET request and get the JSON from the response body
    try {
        const response = await fetch(endpoint);
        // Check to see if there were any issues with the response
        if (!response.ok) {
            throw new Error("Could not fetch data.")
        }
        const data = await response.json();
        return data;
    // Throw any errors that occur
    } catch(error) {
        console.error(error);
    }
}

/**
 * [cssVariable description]
 * Gets the value of a computed style from the document body.
 * @param   {String}    variable    The name of the CSS variable.
 * @returns {String}                The value of the CSS variable.
 */
function cssVariable(variable) {
    // Get the computed style of the document body
    var style = getComputedStyle(document.body);
    // Return the desired variable
    return style.getPropertyValue(variable);
}

/**
 * [cssVariable description]
 * Appends the provided parameters to the endpoint.
 * @param   {String}    endpoint    The endpoint to attach parameters to.
 * @param   {String}    parameters  The parameters to attach to the endpoint.
 * @returns {String}                The endpoint with parameters appended.
 */
function appendParameters(endpoint, parameters) {
    const queryString = Object
        .keys(parameters)
        .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(parameters[key])}`)
        .join("&");
    return `${endpoint}?${queryString}`;
}