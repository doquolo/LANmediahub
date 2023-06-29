const expandImage = (e) => {
    // Get the modal
    var modal = document.getElementById('myModal');
    var captionText = document.getElementById("caption");
    modal.style.display = "flex";
    var modalImg = document.getElementById("img01");
    var modalVid = document.getElementById("vid01");
    
    if (e.id == "img") {
        // Get the image and insert it inside the modal - use its "alt" text as a caption
        modalVid.style.display = "none";
        modalImg.style.display = "block";
        modalImg.src = e.src;
        captionText.href = e.src;
    } else if (e.id == "vid") {
        modalImg.style.display = "none";
        modalVid.style.display = "block";
        modalImg.src = "";
        modalVid.src = e.src;
        captionText.href = e.src;
    }
}

// Get the modal
var modal = document.getElementById('myModal');

// Get the <span> element that closes the modal
var close = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
close.onclick = function() { 
  modal.style.display = "none";
}

// When the user clicks on <span> (del), delete the image
const del = (e) => { 
    if (confirm("Are you sure to delete this media? \nThis action is irreversible!")) {
        let vid01src = document.querySelector("#vid01").src;
        let img01src = document.querySelector("#img01").src;
        console.log(vid01src)
        console.log(img01src)
        var filelink = "";
        if (vid01src == "") {
            // delete image
            filelink = img01src;
        } else {
            // delete video
            filelink = vid01src;
        }
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                location.reload()
            }
        }
        xhr.open('GET', `${filelink}&action=delete`, true);
        xhr.send(null);
    }
}