const documentElement = document.documentElement;
const themeSwitcher = document.getElementById("theme-switcher");

themeSwitcher.onclick = CheckForSwitching;
const themeAttributeName = "data-theme-setting";

async function ChangeDataThemeAttribute(theme) {
    themeSwitcher.setAttribute(themeAttributeName, theme);
    documentElement.setAttribute(themeAttributeName, theme);
    await eel.DataThemeSetting("w", theme)();
}

async function CheckDataThemeSetting() {
    ChangeDataThemeAttribute(await eel.DataThemeSetting("r", "")());
}

function CheckForSwitching() {
    if (themeSwitcher.getAttribute(themeAttributeName) === "dark") {
        ChangeDataThemeAttribute("light");
    } else {
        ChangeDataThemeAttribute("dark");
    }
}

CheckDataThemeSetting();