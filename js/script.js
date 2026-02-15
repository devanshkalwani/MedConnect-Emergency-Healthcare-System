// ===============================
// MEDCONNECT MAIN SCRIPT
// ===============================

// ===============================
// SCROLL REVEAL ANIMATION
// ===============================

window.addEventListener("scroll", reveal);
window.addEventListener("load", reveal);

function reveal() {

    const elements = document.querySelectorAll(".reveal");
    const windowHeight = window.innerHeight;
    const revealPoint = 120;

    elements.forEach(el => {

        const elementTop = el.getBoundingClientRect().top;

        if (elementTop < windowHeight - revealPoint) {
            el.classList.add("active");
        } else {
            el.classList.remove("active");
        }
    });

    revealTrust();
}


// ===============================
// TRUST SECTION SLIDE EFFECT
// ===============================

function revealTrust() {

    const trustBoxes = document.querySelectorAll(".trust-box");
    const windowHeight = window.innerHeight;
    const triggerPoint = 330;

    trustBoxes.forEach(box => {

        const boxTop = box.getBoundingClientRect().top;

        if (boxTop < windowHeight - triggerPoint) {
            box.classList.add("show");
        } else {
            box.classList.remove("show");
        }
    });
}


// ===============================
// DROPDOWN MENU FUNCTIONALITY
// ===============================

function toggleDropdown(menuId) {

    // Close other dropdowns first
    document.querySelectorAll(".dropdown-content").forEach(menu => {
        if (menu.id !== menuId) {
            menu.classList.remove("show");
        }
    });

    // Toggle selected dropdown
    const menu = document.getElementById(menuId);
    if (menu) {
        menu.classList.toggle("show");
    }
}


// Close dropdown when clicking outside
window.addEventListener("click", function (e) {

    if (!e.target.closest(".dropdown")) {

        document.querySelectorAll(".dropdown-content").forEach(menu => {
            menu.classList.remove("show");
        });
    }

});
// ===============================
// LOGIN DROPDOWN CONTROL
// ===============================

const loginToggle = document.getElementById("loginToggle");
const loginMenu = document.getElementById("loginMenu");
const loginDropdown = document.getElementById("loginDropdown");
const getStartedBtn = document.getElementById("getStartedBtn");


// Toggle dropdown when clicking Login
if(loginToggle){
loginToggle.addEventListener("click", function(e){
e.preventDefault();

if(loginMenu.style.display === "block"){
loginMenu.style.display = "none";
}else{
loginMenu.style.display = "block";
}

});
}


// Open dropdown when clicking Get Started
if(getStartedBtn){
getStartedBtn.addEventListener("click", function(e){
e.preventDefault();

loginMenu.style.display = "block";

// smooth scroll to navbar
loginDropdown.scrollIntoView({
behavior: "smooth",
block: "center"
});

});
}


// Close dropdown when clicking outside
window.addEventListener("click", function(e){

if(
loginMenu &&
!loginDropdown.contains(e.target) &&
!getStartedBtn.contains(e.target)
){
loginMenu.style.display = "none";
}

});



// ===============================
// SMOOTH SCROLL FOR NAV LINKS
// ===============================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        const targetId = this.getAttribute("href");

        if (targetId.length > 1) {

            e.preventDefault();

            const target = document.querySelector(targetId);

            if (target) {
                target.scrollIntoView({
                    behavior: "smooth"
                });
            }
        }
    });
});


// ===============================
// ACTIVE NAV LINK ON SCROLL
// ===============================

window.addEventListener("scroll", function () {

    const sections = document.querySelectorAll("section");
    const navLinks = document.querySelectorAll(".nav-link");

    let current = "";

    sections.forEach(section => {

        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;

        if (pageYOffset >= sectionTop - 200) {
            current = section.getAttribute("id");
        }
    });

    navLinks.forEach(link => {
        link.classList.remove("active");

        if (link.getAttribute("href") === "#" + current) {
            link.classList.add("active");
        }
    });

});


// ===============================
// PREVENT FORM EMPTY SUBMISSION (Optional)
// ===============================

document.querySelectorAll("form").forEach(form => {

    form.addEventListener("submit", function (e) {

        let valid = true;

        this.querySelectorAll("input[required], textarea[required]").forEach(input => {
            if (input.value.trim() === "") {
                valid = false;
                input.style.border = "1px solid red";
            } else {
                input.style.border = "";
            }
        });

        if (!valid) {
            e.preventDefault();
            alert("Please fill all required fields.");
        }

    });

});
