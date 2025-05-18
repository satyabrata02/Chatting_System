// secure question
const select = document.querySelector(".select");
const options_list = document.querySelector(".options-list");
const options = document.querySelectorAll(".option");

select.addEventListener("click", () => {
    options_list.classList.toggle("active");
    select.querySelector(".chevron-down").classList.toggle("up");
    select.querySelector(".chevron-up").classList.toggle("down");
});
options.forEach((option) => {
    option.addEventListener("click", () => {
        options.forEach((option) => {option.classList.remove('selected')});
        select.querySelector("span").innerHTML = option.innerHTML;
        option.classList.add("selected");
        options_list.classList.toggle("active");
        select.querySelector(".chevron-down").classList.toggle("up");
        select.querySelector(".chevron-up").classList.toggle("down");
    });
});

//Answer show
var input = document.querySelector(".pswrd2");
var show = document.querySelector(".show2");

show.addEventListener("click", active);
function active(){
    if(input.type === "password"){
        input.type = "text";
        show.style.color = "#1da1f2";
        show.textContent = "HIDE";
    }else{
        input.type = "password";
        show.style.color = "#111";
        show.textContent = "SHOW";
    }
};
