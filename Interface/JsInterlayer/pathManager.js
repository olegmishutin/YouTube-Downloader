const path = document.getElementById("path-input-field");
document.getElementById("select-path").onclick = GetPathForDownloading;

async function GetPathForDownloading() {
    const selectedPath = await eel.GetPathForDownloading()();

    if (selectedPath) {
        path.value = selectedPath;
        eel.Settings("save_path", "w", selectedPath)
    }
}

async function GetSavePath() {
    const savedPath = await eel.Settings("save_path", "r")()

    if (await eel.CheckPath(savedPath)()){
        path.value = savedPath
    }
}

document.getElementById("open-saving-path").onclick = async function () {
    await eel.OpenSavingPath(path.value)();
}
document.getElementById("start-video").onclick = async function () {
    await eel.StartVideoFile()();
}

GetSavePath()