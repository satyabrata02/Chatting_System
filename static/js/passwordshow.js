//Password show
var input = document.querySelector(".pswrd");
var show = document.querySelector(".show");

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

//Answer show
var input2 = document.querySelector(".pswrd2");
var show2 = document.querySelector(".show2");

show2.addEventListener("click", active2);
function active2(){
    if(input2.type === "password"){
        input2.type = "text";
        show2.style.color = "#1da1f2";
        show2.textContent = "HIDE";
    }else{
        input2.type = "password";
        show2.style.color = "#111";
        show2.textContent = "SHOW";
    }
};

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