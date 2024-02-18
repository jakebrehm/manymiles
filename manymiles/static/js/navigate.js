/**
 * [toggleSidebar description]
 * Toggles the sidebar between shown and hidden by pressing the appropriate
 * button.
 */
function toggleSidebar() {
    // Get a handle to the relevant sidebar elements
    const sidebar = document.getElementById("sidebar");
    const openSidebar = document.getElementById("open-sidebar");

    // Toggle the display style of the element
    if (["", "none"].includes(sidebar.style.display)) {
        sidebar.style.display = "flex";
        openSidebar.style.visibility = "hidden";
    } else {
        sidebar.style.display = "none";
        openSidebar.style.visibility = "visible";
    }
}