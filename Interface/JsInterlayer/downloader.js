document.getElementById('downloadButton').onclick = StartDownload
document.getElementById('urlTextBox').oninput = ViewVideoInfo

let url = document.getElementById("urlTextBox");
let path = document.getElementById("pathTextBox");
let status = document.getElementById("status");

async function ViewVideoInfo() {
    status.innerHTML = await eel.GetVideoInfo(url.value)();
}

async function StartDownload() {
    let isPath = await eel.CheckPath(path.value)();

    if (isPath) {
        status.innerHTML = "Downloading...";
        status.innerHTML = await eel.DowloadVideo(url.value, path.value)();
    }
}