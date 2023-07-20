const urlInputField = document.getElementById("url-input-field");
const pathInputField = document.getElementById("path-input-field");
const status = document.getElementById("status");
const resolutions = document.getElementById("resolutions");
const availableResolutions = document.getElementById("available-resolutions");
const selectedResolution = document.getElementById("selected-resolution");

document.getElementById("download-video").onclick = DowloadVideo;
urlInputField.oninput = GetFullVideoInfo;

function ChangeSelectedResolution() {
    selectedResolution.innerHTML = this.innerHTML;
    resolutions.removeAttribute("open");
}

async function GetFullVideoInfo() {
    selectedResolution.innerHTML = "Load";
    status.innerHTML = await eel.GetVideoInfo(urlInputField.value)();
    const videoResolutions = await eel.GetVideoResolutions()();

    for (let i = 0; availableResolutions.childNodes.length > 0; i++) {
        const liElement = document.getElementById(`resolution-li-${i}`);
        liElement.parentNode.removeChild(liElement);
    }

    if (videoResolutions.length === 0) {
        resolutions.removeAttribute("open")
        selectedResolution.innerHTML = "";
    } else {
        videoResolutions.forEach(function (item, index) {
            const liElement = document.createElement("li");
            liElement.id = `resolution-li-${index}`;

            const buttonElement = document.createElement("button");
            buttonElement.innerHTML = item;
            buttonElement.onclick = ChangeSelectedResolution;

            liElement.append(buttonElement);
            availableResolutions.append(liElement);
        })
        selectedResolution.innerHTML = videoResolutions[0];
    }
}

async function DowloadVideo() {
    if (await eel.CheckPath(pathInputField.value)()) {
        status.innerHTML = "Downloading...";
        status.innerHTML = await eel.DowloadVideo(urlInputField.value, pathInputField.value, selectedResolution.innerHTML)();
    } else {
        pathInputField.value = "Path not found";
    }
}