function getMedia() {
  // get the folder we're in
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  const folder = urlParams.get("folder");

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (xhr.readyState == XMLHttpRequest.DONE) {
      createImgFrame(JSON.parse(xhr.responseText));
    }
  };

  if (!folder || folder == "assets") {
    xhr.open("GET", "/queryAllFiles", true);
    document.title = `/ - LANmediahub`;
  } else {
    xhr.open("GET", `/queryAllFiles?folder=${folder}`, true);
    document.title = `${folder}/ - LANmediahub`;
  }
  xhr.send(null);

  function createImgFrame(list) {
    let container = document.querySelector(".imageContainer");
    container.innerHTML = "";
    for (let i in list) {
      if (list[i][2] == "image") {
        let elem = `
            <img id="img" onclick="expandImage(this)" src="/image?image=${list[i][0]}&folder=${list[i][1]}" alt="this is prob an image" loading="lazy"></img><br/>
            `;
        container.innerHTML += elem;
      } else if (list[i][2] == "video") {
        let elem = `
            <video id="vid" width="300" height="300" preload="none" onclick="expandImage(this)" src="/image?image=${list[i][0]}&folder=${list[i][1]}" paused muted poster="/icon/play.png"></video><br/>
            `;
        container.innerHTML += elem;
      }
    }
  }
}

function changeView() {
  let text = document.querySelector("div.heading.menu > div:nth-child(1) > p");
  if (text.innerText == "Folders View") {
    text.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" height="1em"
                    viewBox="0 0 576 512" sytle="fill: white"><!--! Font Awesome Free 6.4.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2023 Fonticons, Inc. -->
                    <path
                        d="M272 416c17.7 0 32-14.3 32-32s-14.3-32-32-32H160c-17.7 0-32-14.3-32-32V192h32c12.9 0 24.6-7.8 29.6-19.8s2.2-25.7-6.9-34.9l-64-64c-12.5-12.5-32.8-12.5-45.3 0l-64 64c-9.2 9.2-11.9 22.9-6.9 34.9s16.6 19.8 29.6 19.8l32 0 0 128c0 53 43 96 96 96H272zM304 96c-17.7 0-32 14.3-32 32s14.3 32 32 32l112 0c17.7 0 32 14.3 32 32l0 128H416c-12.9 0-24.6 7.8-29.6 19.8s-2.2 25.7 6.9 34.9l64 64c12.5 12.5 32.8 12.5 45.3 0l64-64c9.2-9.2 11.9-22.9 6.9-34.9s-16.6-19.8-29.6-19.8l-32 0V192c0-53-43-96-96-96L304 96z" />
        </svg>Files View`;
    getFolder();
  } else if (text.innerText == "Files View") {
    location.replace("/");
  }
}

getMedia();
