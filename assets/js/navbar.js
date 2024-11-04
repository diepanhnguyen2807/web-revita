fetch("navbar.html")
    .then((response) => response.text())
    .then((html) => {
        const navbar = document.getElementById("navbar");
        navbar.innerHTML = html;
        // if (idPage) {
        //     document.querySelector(`#${idPage}`).classList.add("active");
        // }
    })