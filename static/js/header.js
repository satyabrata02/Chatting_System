const body = document.querySelector("body"),
    nav = document.querySelector("nav"),
    modeToggle = document.querySelectorAll(".dark-light"),
    menuBtn = document.querySelector(".sidebarOpen"),
    closeBtn = document.querySelector(".siderbarClose");

let getMode = localStorage.getItem("mode");
if(getMode && getMode === "dark-mode"){
    body.classList.add("dark");
    modeToggle.forEach(toggle => {
        toggle.classList.add("active");
    });
}
modeToggle.forEach(toggle => {
    toggle.addEventListener("click", () => {
        toggle.classList.toggle("active");
        body.classList.toggle("dark");

        if(!body.classList.contains("dark")){
            localStorage.setItem("mode", "light-mode");
        }else{
            localStorage.setItem("mode", "dark-mode");
        }
    });
});

menuBtn.addEventListener("click", () => {
    nav.classList.add("active");
});
closeBtn.addEventListener("click", () => {
    nav.classList.remove("active");
});
body.addEventListener("click", e => {
    let clickedElm = e.target;

    if(!clickedElm.classList.contains("sidebarOpen") && !clickedElm.classList.contains("menu")){
        nav.classList.remove("active");
    }
});