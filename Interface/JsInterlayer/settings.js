document.getElementById("open-settings-button").onclick = () => {
  document.getElementById("settings").classList.add("show-settings");
};

document.getElementById("close-settings-button").onclick = () => {
  document.getElementById("settings").classList.remove("show-settings");
};

const path = document.getElementById("videos-folder");

path.onchange = async () => {
  await eel.Settings("videos_folder", "w", path.value)();
};

document.getElementById("select-folder").onclick = async () => {
  const selectedPath = await eel.GetPathForDownloading()();

  if (selectedPath) {
      path.value = selectedPath;
      await eel.Settings("videos_folder", "w", selectedPath)();
  }
};

async function GetVideosFolder() {
    path.value = await eel.Settings("videos_folder", "r")()
}

GetVideosFolder()

document.getElementById("select-dark-theme").onclick = () => {
  ChangeDataThemeAttribute("dark");
};

document.getElementById("select-light-theme").onclick = () => {
  ChangeDataThemeAttribute("light");
};

async function ChangeDataThemeAttribute(theme) {
  document.documentElement.setAttribute("data-theme-setting", theme);
  await eel.Settings("theme", "w", theme)();
}

async function CheckDataThemeSetting() {
  ChangeDataThemeAttribute(await eel.Settings("theme", "r")());
}

CheckDataThemeSetting();
