const cars = document.querySelectorAll(".hero-car-slide");

let current = 0;


setInterval(()=>{

    cars[current].classList.remove("active");
    cars[current].classList.add("exit");


    current++;

    if(current >= cars.length){
        current = 0;
    }


    cars[current].classList.add("active");


    setTimeout(()=>{

        cars.forEach(car=>{
            car.classList.remove("exit");
        });

    },1000);


},4000);