/*
Based heavily off of the following example code form Pico.css:
https://github.com/picocss/examples/blob/master/v1-preview/js/modal.js
*/

// Configure
const isOpenClass = "model-is-open";
const isOpeningClass = "model-is-opening";
const isClosingClass = "model-is-closing";
const animationDuration = 400; // ms
let visibleModal = null;

const isScrollbarVisible = () => {
    return document.body.scrollHeight > screen.height;
};

const toggleModal = (event) => {
    // event.preventDefault();
    const modal = document.getElementById(event.currentTarget.getAttribute("data-target"));
    console.log(event.currentTarget.getAttribute("data-target"));
    console.log(modal);
    console.log(isModalOpen(modal));
    (typeof modal != "undefined") && (modal != null) && (isModalOpen(modal))
        ? closeModal(modal)
        : openModal(modal);
};

const isModalOpen = (modal) => {
    return modal.hasAttribute("open") && (modal.getAttribute("open") != "false")
        ? true
        : false;
};

const openModal = (modal) => {
    if (isScrollbarVisible()) {
        document.documentElement.style.setProperty(
            "--scrollbar-width",
            `${getScrollbarWidth()}px`
        )};
    document.documentElement.classList.add(isOpenClass, isOpeningClass);
    setTimeout(() => {
        visibleModal = modal;
        document.documentElement.classList.remove(isOpeningClass);
    }, animationDuration);
    modal.setAttribute("open", true);
};

const closeModal = (modal) => {
    visibleModal = null;
    document.documentElement.classList.add(isClosingClass);
    setTimeout(() => {
        document.documentElement.classList.remove(isClosingClass, isOpenClass);
        document.documentElement.style.removeProperty("--scrollbar-width");
        modal.removeAttribute("open");
    }, animationDuration);
};

document.addEventListener(
    "click",
    (event) => {
        if (visibleModal != null) {
            const modalContent = visibleModal.querySelector("article");
            const isClickInside = modalContent.contains(event.target);
            !isClickInside && closeModal(visibleModal);
        }
    }
);

document.addEventListener(
    "keydown",
    (event) => {
        if (event.key === "Escape" && visibleModal != null) {
            closeModal(visibleModal);
        }
    }
);

const getScrollbarWidth = () => {
    // Creating invisible container
    const outer = document.createElement("div");
    outer.style.visibility = "hidden";
    outer.style.overflow = "scroll"; // forcing scrollbar to appear
    outer.style.msOverflowStyle = "scrollbar"; // needed for WinJS apps
    document.body.appendChild(outer);

    // Creating inner element and placing it in the container
    const inner = document.createElement("div");
    outer.appendChild(inner);

    // Calculating the difference between container's and child's widths
    const scrollbarWidth = outer.offsetWidth - inner.offsetWidth;

    // Removing the temporary elements
    outer.parentNode.removeChild(outer);

    return scrollbarWidth;
};