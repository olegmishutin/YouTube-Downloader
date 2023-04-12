document.getElementById('downloadButton').onclick = StartDownload;
document.getElementById('urlTextBox').oninput = GetFullVideoInfo;

let url = document.getElementById("urlTextBox");
let path = document.getElementById("pathTextBox");
let status = document.getElementById("status");
let resolution = document.getElementById("resolution");
let availableResolution = document.getElementById("available-resolution");
let selectedResolution = document.getElementById("selectedResolution");

function ChangeSelectedResolution() {
    selectedResolution.innerHTML = this.innerHTML;
}

async function GetFullVideoInfo() {
    status.innerHTML = await eel.GetVideoInfo(url.value)();
    let availableResolutions = await eel.GetVideoResolutions()();

    for (let i = 0; availableResolution.childNodes.length > 0; i++) {
        let liTag = document.getElementById(`res-li-${i}`);
        liTag.parentNode.removeChild(liTag);
    }

    for (let i = 0; i < availableResolutions.length; i++) {
        let liTag = document.createElement("li");
        liTag.id = `res-li-${i}`;

        availableResolution.append(liTag);

        let buttonTag = document.createElement("button");
        buttonTag.id = `res-button-${i}`;
        buttonTag.innerHTML = availableResolutions[i];
        buttonTag.onclick = ChangeSelectedResolution;

        liTag.append(buttonTag);
    }

    if (availableResolutions.length === 0) {
        selectedResolution.innerHTML = "";
        resolution.removeAttribute("open")
    } else {
        selectedResolution.innerHTML = availableResolutions[0];
    }
}

async function StartDownload() {
    let isPath = await eel.CheckPath(path.value)();

    if (isPath) {
        status.innerHTML = "Downloading...";
        status.innerHTML = await eel.DowloadVideo(url.value, path.value, selectedResolution.innerHTML)();
    }
}