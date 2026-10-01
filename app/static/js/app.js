
document.addEventListener("DOMContentLoaded", () => {

    initializeMenu();
    initializeRevealAnimation();
    initializeNavigation();
     initializeNavbar();
     initializeSearch();
});

const cars = [ 

{
name:"Lamborghini Huracan",
image:"/static/Images/cars/back1.jpg",
description:"Experience luxury, speed and comfort wherever you go.",
power:"602 HP",
gear:"Automatic",
price:"₦250,000"
},


{
name:"BMW X5",
image:"/static/Images/cars/back2.jpg",
description:"A perfect combination of luxury and performance.",
power:"335 HP",
gear:"Automatic",
price:"₦150,000"
},


{
name:"Range Rover Sport",
image:"/static/Images/cars/back3.jpg",
description:"Premium SUV built for every journey.",
power:"355 HP",
gear:"Automatic",
price:"₦180,000"
},


{
name:"Mitbuishi Concept RA",
image:"/static/Images/cars/Dark.jpg",
description:"Feel the power of Japanese engineering.",
power:"565 HP",
gear:"Automatic",
price:"₦200,000"
}

];



let currentCar = 0;



const hero = document.querySelector(".hero-bg");

const dotsContainer = document.querySelector("#dots");



// create dots
cars.forEach((car,index)=>{

let dot=document.createElement("span");


dot.classList.add("dot");


dot.onclick=()=>{

currentCar=index;
changeCar();

};


dotsContainer.appendChild(dot);


});





function changeCar(){


let car=cars[currentCar];


// fade out

hero.style.opacity="0";

document.querySelector(".hero-content").style.opacity="0";



setTimeout(()=>{


hero.style.backgroundImage=
`url('${car.image}')`;



let carNameEl = document.getElementById("carName");
let descEl = document.getElementById("description");
let speedEl = document.getElementById("speed");
let gearEl = document.getElementById("gear");
let priceEl = document.getElementById("price");

if (carNameEl) carNameEl.textContent = car.name;
if (descEl) descEl.textContent = car.description;
if (speedEl) speedEl.textContent = car.power;
if (gearEl) gearEl.textContent = car.gear;
if (priceEl) priceEl.textContent = car.price;



hero.style.opacity="1";


document.querySelector(".hero-content").style.opacity="1";



updateDots();



},500);



currentCar++;


if(currentCar>=cars.length){

currentCar=0;

}


}




function updateDots(){


document.querySelectorAll(".dot")
.forEach((dot,index)=>{


dot.classList.toggle(
"active",
index===currentCar
);


});


}



changeCar();


setInterval(changeCar,5000);