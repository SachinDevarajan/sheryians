/* =========================
   MOBILE MENU
========================= */

function openMobileMenu() {
    const menu = document.getElementById("mobileMenu");

    if (menu) {
        menu.classList.add("open");
        document.body.style.overflow = "hidden";
    }
}


function closeMobileMenu() {
    const menu = document.getElementById("mobileMenu");

    if (menu) {
        menu.classList.remove("open");
        document.body.style.overflow = "";
    }
}


/* =========================
   CALLBACK MODAL
========================= */

function openCallbackModal() {
    const modal = document.getElementById("callbackModal");

    if (modal) {
        modal.classList.add("show");
        document.body.style.overflow = "hidden";
    }
}


function closeCallbackModal() {
    const modal = document.getElementById("callbackModal");

    if (modal) {
        modal.classList.remove("show");
        document.body.style.overflow = "";
    }
}


const callbackModal = document.getElementById("callbackModal");

if (callbackModal) {
    callbackModal.addEventListener("click", function (event) {

        if (event.target === callbackModal) {
            closeCallbackModal();
        }

    });
}


/* =========================
   PROFILE DROPDOWN
========================= */

function toggleProfileMenu(event) {

    event.stopPropagation();

    const dropdown = document.getElementById("profileDropdown");
    const chevron = document.getElementById("profileChevron");

    if (dropdown) {
        dropdown.classList.toggle("show");
    }

    if (chevron) {
        chevron.classList.toggle("rotate");
    }
}


document.addEventListener("click", function (event) {

    const dropdown = document.getElementById("profileDropdown");
    const wrapper = document.querySelector(".profile-menu-wrapper");

    if (
        dropdown &&
        wrapper &&
        !wrapper.contains(event.target)
    ) {

        dropdown.classList.remove("show");

        const chevron =
            document.getElementById("profileChevron");

        if (chevron) {
            chevron.classList.remove("rotate");
        }
    }

});


/* =========================
   FAQ
========================= */

const faqItems =
    document.querySelectorAll(".faq-item");


faqItems.forEach(function (item) {

    const question =
        item.querySelector(".faq-question");

    if (!question) {
        return;
    }

    question.addEventListener("click", function () {

        faqItems.forEach(function (faq) {

            if (faq !== item) {
                faq.classList.remove("active");
            }

        });

        item.classList.toggle("active");

    });

});


/* =========================
   ESCAPE KEY
========================= */

document.addEventListener("keydown", function (event) {

    if (event.key === "Escape") {

        closeMobileMenu();
        closeCallbackModal();

        const dropdown =
            document.getElementById("profileDropdown");

        if (dropdown) {
            dropdown.classList.remove("show");
        }
    }
});