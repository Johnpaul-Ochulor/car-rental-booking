
function initializeNavigation() {

    const signUpButtons = document.querySelectorAll(".Sign");
    const signInButtons = document.querySelectorAll(".SignIn");

    signUpButtons.forEach(button => {
        button.addEventListener("click", () => {
            window.location.href = "./SignUp/SignUp.html";
        });
    });

    signInButtons.forEach(button => {
        button.addEventListener("click", () => {
            window.location.href = "./SignIn/SignIn.html";
        });
    });

}

function initializeNavbar() {

    const navbar = document.querySelector(".navbar");

    window.addEventListener("scroll", () => {

        if(window.scrollY > 40){

            navbar.classList.add("scrolled");

        }else{

            navbar.classList.remove("scrolled");

        }

    });

}