function updateClock() {
    const now = new Date();

    const time = now.toLocaleTimeString();

    document.getElementById("clock").textContent = time;
}

setInterval(updateClock, 1000);
updateClock();


// Detect whether the stream loads successfully
const camera = document.getElementById("camera");

camera.addEventListener("load", () => {
    document.querySelector(".status span:last-child").textContent =
        "CAMERA ONLINE";
});

camera.addEventListener("error", () => {
    document.querySelector(".status span:last-child").textContent =
        "CAMERA OFFLINE";
});