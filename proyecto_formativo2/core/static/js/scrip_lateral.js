const iconoMenu = document.getElementById("icono_menu");
    const naveLateral = document.querySelector(".nave_lateral");

    iconoMenu.addEventListener("click", function() {
        if (naveLateral.classList.contains("expandida")) {
            naveLateral.classList.remove("expandida");
        } else {
            naveLateral.classList.add("expandida");
        }
    });