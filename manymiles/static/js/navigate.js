/**
 * [toggleSidebar description]
 * Toggles the sidebar between shown and hidden by pressing the appropriate
 * button.
 */
function toggleSidebar() {
    // Get a handle to the sidebar element
    const sidebar = document.getElementById("sidebar");

    // Toggle the display style of the element
    if (["", "none"].includes(sidebar.style.display)) {
        sidebar.style.display = "flex";
    } else {
        sidebar.style.display = "none";
    }
}