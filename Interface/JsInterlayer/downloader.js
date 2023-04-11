document.getElementById('downloadButton').onclick = StartDownload;
document.getElementById('urlTextBox').oninput = GetFullVideoInfo;

let url = document.getElementById("urlTextBox");
let path = document.getElementById("pathTextBox");
let status = document.getElementById("status");
let resolution = document.getElementById("resolution");

async function GetFullVideoInfo() {
    status.innerHTML = await eel.GetVideoInfo(url.value)();
    let availableResolutions = await eel.GetVideoResolutions()();

    let option = document.getElementById("available-resolution");

    if (resolution.length > 0) {
        for (let i = 0; resolution.length > 0; i++) {
            let option = document.getElementById(`available-resolution ${i}`);
            option.parentNode.removeChild(option);
        }
    }

    for (let i = 0; i < availableResolutions.length; i++) {
        let option = document.createElement("option");

        option.value = availableResolutions[i];
        option.innerHTML = availableResolutions[i];
        option.id = `available-resolution ${i}`;

        resolution.append(option);
    }

    if (availableResolutions.length > 0) {
        resolution.style.backgroundImage = "none";
    } else {
        resolution.style.backgroundImage = 'url("../Image/resolutionIcon.png")';
    }
}

async function StartDownload() {
    let isPath = await eel.CheckPath(path.value)();

    if (isPath) {
        status.innerHTML = "Downloading...";
        status.innerHTML = await eel.DowloadVideo(url.value, path.value, resolution.value)();
    }
}