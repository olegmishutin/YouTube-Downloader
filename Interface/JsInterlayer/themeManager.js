const documentElement = document.documentElement;
const themeAttributeName = "data-theme-setting";
document.getElementById("theme-switcher").onclick = CheckForSwitching;

async function ChangeDataThemeAttribute(theme) {
    documentElement.setAttribute(themeAttributeName, theme);
    await eel.Settings("theme", "w", theme)();
}

async function CheckDataThemeSetting() {
    ChangeDataThemeAttribute(await eel.Settings("theme", "r")());
}

function CheckForSwitching() {
    if (documentElement.getAttribute(themeAttributeName) === "dark") {
        ChangeDataThemeAttribute("light");
    } else {
        ChangeDataThemeAttribute("dark");
    }
}

CheckDataThemeSetting();