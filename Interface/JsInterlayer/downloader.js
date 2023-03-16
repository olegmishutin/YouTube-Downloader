document.getElementById('downloadButton').onclick = StartDownload

let status = document.getElementById("status");

function SetToZero() {
    if (status.innerHTML != "Downloading...") {
        status.innerHTML = "";
        document.getElementById("urlTextBox").value = "";
    }
}

async function StartDownload() {
    let url = document.getElementById("urlTextBox").value;
    let path = document.getElementById("pathTextBox").value;

    let isPath = await eel.CheckPath(path)();

    if (isPath && (status.innerHTML == "" || status.innerHTML == "Server error, try again")) {
        status.innerHTML = "Downloading...";

        let result = await eel.DowloadVideo(url, path)();
        status.innerHTML = result;

        if (result && status.innerHTML != "Server error, try again") {
            setTimeout(SetToZero, 7500);
        }
    }
}