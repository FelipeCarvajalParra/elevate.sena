document.addEventListener('DOMContentLoaded', function() {
    var enlacesEspecificos = document.querySelectorAll('.redireccion');
    enlacesEspecificos.forEach(function(enlace) {
        enlace.addEventListener('click', function() {
            window.open('https://oferta.senasofiaplus.edu.co/sofia-oferta/', '_blank'); // URL a la que quieres redirigir
        });
    });
});