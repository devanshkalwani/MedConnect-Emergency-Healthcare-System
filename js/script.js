window.addEventListener("scroll", reveal);

function reveal(){

const elements = document.querySelectorAll(".reveal");

elements.forEach(el => {

const windowHeight = window.innerHeight;
const elementTop = el.getBoundingClientRect().top;
const revealPoint = 120;

if(elementTop < windowHeight - revealPoint){
el.classList.add("active");
}else{
el.classList.remove("active");
}

});

revealTrust();
}



/* TRUST SLIDE FROM SIDES */

function revealTrust(){

const trustBoxes = document.querySelectorAll(".trust-box");

trustBoxes.forEach(box => {

const windowHeight = window.innerHeight;
const boxTop = box.getBoundingClientRect().top;
const triggerPoint = 330;

if(boxTop < windowHeight - triggerPoint){
box.classList.add("show");
}else{
box.classList.remove("show");
}

});

}
function toggleDropdown(menuId){

// close other dropdowns
document.querySelectorAll(".dropdown-content")
.forEach(menu => {
    if(menu.id !== menuId){
        menu.classList.remove("show");
    }
});

// toggle clicked one
document.getElementById(menuId)
.classList.toggle("show");

}


// close if clicking outside
window.onclick = function(e){

if(!e.target.matches('.dropbtn')){

document.querySelectorAll(".dropdown-content")
.forEach(menu=>{
menu.classList.remove("show");
});

}

}
