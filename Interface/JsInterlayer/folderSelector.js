document.getElementById('openFolder').onclick = SelectFolder

async function SelectFolder() {
    let path = await eel.SelectFolder()();
    document.getElementById("pathTextBox").value = path;
}