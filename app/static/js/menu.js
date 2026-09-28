
function initializeMenu() {

    const mobileNav = document.querySelector("mobileNav");
    const openBtn = document.getElementById("openMenu");
    const closeBtn = document.getElementById("closeMenu");

    if(!mobileNav || !openBtn || !closeBtn) {

        openBtn.addEventListener("click", openMenu);
        closeBtn.addEventListener("click", closeMenu);
    }

    function openMenu() {

        mobileNav.classList.add("show-menu");
    }

    function closeMenu() {

        mobileNav.classList.remove("show-menu");
    }
}