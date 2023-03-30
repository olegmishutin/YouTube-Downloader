document.getElementById('openFolder').onclick = SelectFolder
document.getElementById('openSavingPath').onclick = OpenSavingPath

async function SelectFolder() {
    document.getElementById("pathTextBox").value = await eel.SelectFolder()();
}

async function OpenSavingPath() {
    await eel.OpenSavingPath(document.getElementById("pathTextBox").value)();
}