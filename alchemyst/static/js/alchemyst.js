if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/js/service-worker.js');
}

function hamburger() {
    var x = document.getElementById("top-nav");
    if (x.className === "nav-menu") {
        x.className += " responsive";
    } else {
        x.className = "nav-menu";
    }
}