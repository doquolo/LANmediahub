var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
    if (xhr.readyState == XMLHttpRequest.DONE) {
        createImgFrame(JSON.parse(xhr.responseText).dir)
    }
}
xhr.open('GET', '/queryAllFiles?folderName=assets', true);
xhr.send(null);

function createImgFrame(list) {
    let container = document.querySelector(".imageContainer")
    console.log(list)
    for (let i in list) {
        if (list[i][1] == "image") {
            let elem = `
            <img id="img" onclick="expandImage(this)" src="/image?image=${list[i][0]}&folder=assets" alt="this is prob an image" loading="lazy"></img><br/>
            `
            container.innerHTML += elem
        } else if (list[i][1] == "video") {
            let elem = `
            <video id="vid" width="300" height="300" preload="none" onclick="expandImage(this)" src="/image?image=${list[i][0]}&folder=assets" paused muted></video><br/>
            `
            container.innerHTML += elem
        }
    }
}

createImgFrame()