fetch("components/navbar.html")
    .then((response) => response.text())
    .then((html) => {
        const navbar = document.getElementById("navbar");
        navbar.innerHTML = html;
        // if (idPage) {
        //     document.querySelector(`#${idPage}`).classList.add("active");
        // }
    })

fetch("components/topnav.html")
    .then((response) => response.text())
    .then((html) => {
        const topnav = document.getElementById("topnav");
        topnav.innerHTML = html;
        // if (idPage) {
        //     document.querySelector(`#${idPage}`).classList.add("active");
        // }
    })

fetch("components/footer.html")
    .then((response) => response.text())
    .then((html) => {
        const footer = document.getElementById("footer");
        footer.innerHTML = html;
        // if (idPage) {
        //     document.querySelector(`#${idPage}`).classList.add("active");
        // }
    })