const path = document.getElementById("path-input-field");

document.getElementById("select-path").onclick = GetPathForDownloading;
document.getElementById("open-saving-path").onclick = OpenSavingPath;

async function GetPathForDownloading() {
    const selectedPath = await eel.GetPathForDownloading()();

    if (selectedPath) {
        path.value = selectedPath;
    }
}

async function OpenSavingPath() {
    await eel.OpenSavingPath(path.value)();
}