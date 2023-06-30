function getFolder() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            createImgFrame(JSON.parse(xhr.responseText))
        }
    }

    document.title = `folderview - LANmediahub`
    xhr.open('GET', '/queryAllFiles', true);
    xhr.send(null);

    function createImgFrame(list) {
        let container = document.querySelector(".imageContainer")
        container.innerHTML = ""
        // get list of folder
        let owo = {}
        for (let i in list) {
            if (!owo[list[i][1]]) {
                owo[list[i][1]] = [];
            }
            owo[list[i][1]].push(list[i])    
        }
        for (let i in owo) {
            let imageName = "", imageFolder = "";
            for (let j in owo[i]) {
                if (owo[i][j][2] == "image") {
                    imageName = owo[i][j][0]
                    imageFolder = owo[i][j][1]
                }
            }
            if (imageName == "") {
                const splitted_i = i.split("\\")
                let elem = `
                <img id="img" onclick="location.replace('/?folder=${splitted_i[splitted_i.length - 1]}')" src="/icon/play.png" alt="this is prob an image" loading="lazy"></img><br/>
                `
                container.innerHTML += elem
            } else {
                const splitted_i = i.split("\\")
                let elem = `
                <img id="img" onclick="location.replace('/?folder=${splitted_i[splitted_i.length - 1]}')" src="/image?image=${imageName}&folder=${imageFolder}" alt="this is prob an image" loading="lazy"></img><br/>
                `
                container.innerHTML += elem
            }
        }
    }
}