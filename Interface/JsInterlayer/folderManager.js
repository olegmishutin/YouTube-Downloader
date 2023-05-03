document.getElementById("select-folder").onclick = GetPathForDownloading;
document.getElementById("open-saving-path").onclick = OpenSavingPath;

const path = document.getElementById("path-input-field");

async function GetPathForDownloading() {
    path.value = await eel.GetPathForDownloading()();
}

async function OpenSavingPath() {
    await eel.OpenSavingPath(path.value)();
}