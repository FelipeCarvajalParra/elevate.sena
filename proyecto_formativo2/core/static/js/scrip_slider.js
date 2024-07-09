const boton1 = document.querySelector("#btn_slider1");
const boton2 = document.querySelector("#btn_slider2");
const boton3 = document.querySelector("#btn_slider3");
const slider = document.querySelector("#slider");
const sliderSection = document.querySelectorAll(".slider-section");

let operacion = 0,
    counter = 0,
    widthImg = 100 / sliderSection.length;

function moveToRight() {
    if (counter >= sliderSection.length - 1) {
        counter = 0;
        operacion = 0;
    } else {
        counter++;
        operacion = operacion + widthImg;
    }
    updateSlider();
}

function moveToLeft() {
    counter--;
    if (counter < 0) {
        counter = sliderSection.length - 1;
        operacion = widthImg * (sliderSection.length - 1);
    } else {
        operacion = operacion - widthImg;
    }
    updateSlider();
}

function updateSlider() {
    slider.style.transform = `translate(-${operacion}%)`;
    slider.style.transition = "all ease .6s";

    // Remover todas las clases de botones activos
    document.querySelectorAll(".boton-slider").forEach(boton => {
        boton.classList.remove("boton-slider-activo");
    });

    // Agregar clase activa al botón correspondiente
    if (counter === 0) {
        boton1.classList.add("boton-slider-activo");
    } else if (counter === 1) {
        boton2.classList.add("boton-slider-activo");
    } else if (counter === 2) {
        boton3.classList.add("boton-slider-activo");
    }
}

// Evento de click para botón 1
boton1.addEventListener("click", function() {
    counter = 0;
    operacion = 0;
    updateSlider();
});

// Evento de click para botón 2
boton2.addEventListener("click", function() {
    counter = 1;
    operacion = widthImg;
    updateSlider();
});

// Evento de click para botón 3
boton3.addEventListener("click", function() {
    counter = 2;
    operacion = widthImg * 2;
    updateSlider();
});

// Automáticamente mover al siguiente slider cada 9 segundos
setInterval(() => {
    moveToRight();
}, 9000);

// Al cargar la página, actualizar el slider y botones
updateSlider();










