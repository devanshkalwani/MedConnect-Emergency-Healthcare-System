// ===============================
// MEDCONNECT MAIN SCRIPT (FINAL)
// ===============================

// ===============================
// CONFIG
// ===============================
const BASE_URL = window.MEDCONNECT_API_BASE || "http://127.0.0.1:8001/api";

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
// TRUST SECTION
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
// DROPDOWN MENU
// ===============================
function toggleDropdown(menuId) {
    document.querySelectorAll(".dropdown-content").forEach(menu => {
        if (menu.id !== menuId) {
            menu.classList.remove("show");
        }
    });

    const menu = document.getElementById(menuId);
    if (menu) menu.classList.toggle("show");
}

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

if (loginToggle) {
    loginToggle.addEventListener("click", function (e) {
        e.preventDefault();
        loginMenu.style.display =
            loginMenu.style.display === "block" ? "none" : "block";
    });
}

if (getStartedBtn) {
    getStartedBtn.addEventListener("click", function (e) {
        e.preventDefault();
        loginMenu.style.display = "block";

        loginDropdown.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });
    });
}

window.addEventListener("click", function (e) {
    if (
        loginMenu &&
        !loginDropdown.contains(e.target) &&
        !getStartedBtn.contains(e.target)
    ) {
        loginMenu.style.display = "none";
    }
});

// ===============================
// SMOOTH SCROLL
// ===============================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
        const targetId = this.getAttribute("href");

        if (targetId.length > 1) {
            e.preventDefault();
            const target = document.querySelector(targetId);

            if (target) {
                target.scrollIntoView({ behavior: "smooth" });
            }
        }
    });
});

// ===============================
// ACTIVE NAV LINK
// ===============================
window.addEventListener("scroll", function () {
    const sections = document.querySelectorAll("section");
    const navLinks = document.querySelectorAll(".nav-link");

    let current = "";

    sections.forEach(section => {
        const sectionTop = section.offsetTop;

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
// FORM VALIDATION
// ===============================
document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", function (e) {
        let valid = true;

        this.querySelectorAll("input[required]").forEach(input => {
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

// ===============================
// 🔐 USER LOGIN (FINAL CLEAN)
// ===============================


// ===============================
// 🏥 HOSPITAL LOGIN (FINAL CLEAN)
// ===============================


// ===============================
// 📍 GET LOCATION
// ===============================
function getLocation() {
    return new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
            pos => {
                resolve({
                    lat: pos.coords.latitude,
                    lon: pos.coords.longitude
                });
            },
            err => reject(err)
        );
    });
}

// ===============================
// 🚨 SOS TRIGGER (FINAL FIXED)
// ===============================
async function triggerSOS(type = "general") {
    try {

        const user_id = localStorage.getItem("user_id");

        if (!user_id) {
            alert("Please login first");
            return;
        }

        // 🔥 STOP previous polling (IMPORTANT)
        if (window.sosPolling) {
            clearInterval(window.sosPolling);
        }

        // 🔥 Get location
        const location = await getLocation();

        // 🔥 Send SOS request
        const res = await fetch(`${BASE_URL}/sos/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                user_id: user_id,
                latitude: location.lat,
                longitude: location.lon,
                emergency_type: type
            })
        });

        const data = await res.json();

        if (res.ok) {

            console.log("🔍 Searching nearby hospitals...");

            // 🔥 SINGLE POLLING INSTANCE
            window.sosPolling = setInterval(async () => {

                try {

                    const statusRes = await fetch(`${BASE_URL}/status/${user_id}/`);
                    const statusData = await statusRes.json();

                    if (statusData.status === "ASSIGNED") {

                        alert(`🏥 ${statusData.hospital} is responding. Help is on the way!`);

                        clearInterval(window.sosPolling);
                    }

                } catch (err) {
                    console.log("Status check failed");
                }

            }, 2000);

        } else {
            alert(data.error || "SOS failed");
        }

    } catch (err) {
        alert("Location error or permission denied");
    }
}

// ===============================
// 🏥 ACCEPT REQUEST (FINAL)
// ===============================
async function acceptEmergency(requestId) {

    const hospital_id = localStorage.getItem("hospital_id");

    if (!hospital_id) {
        alert("Please login as hospital first");
        return;
    }

    const res = await fetch(`${BASE_URL}/hospital/accept/${requestId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            hospital_id: hospital_id
        })
    });

    const data = await res.json();

    if (res.ok) {
        alert(`✅ Patient Assigned!
        
        Check dashboard for full details.`);
    } else {
        alert(data.error || "Already assigned");
    }
}