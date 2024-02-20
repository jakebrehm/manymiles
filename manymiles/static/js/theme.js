/*
Heavily based off of the following Pico.css example:
https://codesandbox.io/s/github/picocss/examples/tree/master/v1
*/

const themeHandler = {
    // General configuration
    _theme: "auto",
    menuTarget: "details[role='list']",
    buttonsTarget: "a[data-theme-handler]",
    buttonAttribute: "data-theme-handler",
    rootAttribute: "data-theme",
    localStorageKey: "picoPreferredTheme",

    // Logo configuration
    logoId: null,
    logoLight: null,
    logoDark:null,

    // Initialize the theme handler
    initialize() {
        // Pull the desired theme from local storage if possible
        this.theme = this.themeFromLocalStorage;
        // Initialize the appropriate buttons
        this.initializeSwitchers();
    },

    // Store theme in local storage
    themeToLocalStorage() {
        if (typeof window.localStorage !== "undefined") {
            window.localStorage.setItem(this.localStorageKey, this.theme);
        }
    },

    // Pull theme from local storage
    get themeFromLocalStorage() {
        if (typeof window.localStorage !== "undefined") {
            if (window.localStorage.getItem(this.localStorageKey) !== null) {
                return window.localStorage.getItem(this.localStorageKey);
            }
        }
        // If there is an issue with storage, return the internal theme
        return this._theme;
    },

    // Get the user's preferred theme
    get preferredTheme() {
        if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
            return "dark"
        } else {
            return "light"
        }
    },

    // Initialize each theme-switching button
    initializeSwitchers() {
        const buttons = document.querySelectorAll(this.buttonsTarget);
        buttons.forEach((button) => {
            // Execute whenever a button is clicked...
            button.addEventListener(
                "click",
                (event) => {
                    event.preventDefault();
                    // Set the theme
                    this.theme = button.getAttribute(this.buttonAttribute);
                    // Close the dropdown menu
                    const menu = document.querySelector(this.menuTarget)
                    menu.removeAttribute("open");
                },
                false
            );
        });
    },

    // Apply the theme
    applyTheme() {
        const html = document.querySelector("html")
        html.setAttribute(this.rootAttribute, this.theme)
        // Change the logo
        if (this.logoId !== null) {
            var logo = document.getElementById(this.logoId);
            if (this.theme == "light") {
                logo.src = this.logoLight;
            } else {
                logo.src = this.logoDark;
            };
        };
    },

    // Get the current theme
    get theme() {
        return this._theme;
    },

    // Set the current theme
    set theme(theme) {
        // If the user selected the auto theme...
        if (theme == "auto") {
            // Set the internal theme to the preferred theme
            if (this.preferredTheme == "dark") {
                this._theme = "dark"
            } else {
                this._theme = "light"
            }
        // Otherwise, set the internal theme to the user's choice
        } else if (theme == "dark" || theme == "light") {
            this._theme = theme;
        }
        // Apply the theme and save the choice to local storage
        this.applyTheme();
        this.themeToLocalStorage();
    },
};

// Initialize the theme switcher
themeHandler.initialize();