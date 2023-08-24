const expandMenu = () => {
    const menu = document.querySelector("div.menu");
    if (menu.style.display == "none") {
      menu.style.display = "flex";
    } else {
      menu.style.display = "none";
    }
}

const zoomIn = () => {
    // Get the root element
    const r = document.querySelector(":root")

    // acquire current zoom percent
    let zoom = getComputedStyle(r).getPropertyValue('--size');

    // limit to only able to zoom in to 90vw maximum
    // increase by 10 percent
    if (zoom !== "90vw") {
        r.style.setProperty('--size', `${parseInt(zoom.slice(0, -2)) + 10}vw`);
    }
}

const zoomOut = () => {
    // Get the root element
    const r = document.querySelector(":root")

    // acquire current zoom percent
    let zoom = getComputedStyle(r).getPropertyValue('--size');

    // limit to only able to zoom out to 10vw maximum
    // increase by 10 percent
    if (zoom !== "10vw") {
        r.style.setProperty('--size', `${parseInt(zoom.slice(0, -2)) - 10}vw`);
    }
}