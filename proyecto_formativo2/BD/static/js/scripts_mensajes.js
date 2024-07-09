//este apartado captura los parametros del mensaje y los manda a una funcion
//que los muetsra en una ventana emergente
document.querySelectorAll('.far_vista').forEach(button => {
    button.addEventListener('click', function() {
        const id = this.getAttribute('data-id');
        const nomb = this.getAttribute('data-nomb');
        const apel = this.getAttribute('data-apel');
        const mens = this.getAttribute('data-mens');
        const fech = this.getAttribute('data-fech');
        // Llamar a la función mostrarMensaje con los datos obtenidos
        mostrarMensaje(id, nomb, apel, mens, fech);
    });
});

// Funcion para mostrar el mensaje en una ventana 
function mostrarMensaje(id, nomb, apel, mens, fech) {
    Swal.fire({
        customClass: {
            popup: 'ventana'
        },
        html: `
        <div class="fecha">${fech}</div>
        <div class="contenedor">
            <p><b>De:</b> ${nomb} ${apel} </p>
            <p><b>Mensaje:</b> ${mens}</p>
        </div>
        `,
        showCloseButton: true,
        confirmButtonText: 'Responder',
        showDenyButton: true,
        denyButtonText: 'Eliminar',
        denyButtonColor: '#ed5564',
    }).then((result) => {
        if (result.isConfirmed) {
            var botones = document.querySelectorAll('.far_gmail');
            botones.forEach(function(boton) {
                boton.click();
            });
        } else if (result.isDenied) {
            validacion(id);
        }
    });
}

//funcion para mostrar la notificacion de cancelación
function mensajeCancelacion() {
    const Toast = Swal.mixin({
        toast: true,
        position: "bottom-end",
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.onmouseenter = Swal.stopTimer;
            toast.onmouseleave = Swal.resumeTimer;
        }
    });
    Toast.fire({
        icon: "error",
        title: "Operación Cancelada",
    });
}

//funcion que valida eliminar un registro
function validacion(id) {
    console.log(id); 
    Swal.fire({
        title: "¿Seguro?",
        text: "Esta acción eliminará el registro permanentemente.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "¡Sí, borrar!",
        cancelButtonText: 'Cancelar',
    }).then((result) => {
        if (result.isConfirmed) {
            eliminarRegistro(id);
        } else {
            mensajeCancelacion();
        }
    });
}

//este apartado captura el id del registro a eliminar, e inicia la secuencia de
//validacion
document.querySelectorAll('.far_eliminar').forEach(button => {
    button.addEventListener('click', function() {
        const id = this.getAttribute('data-id');
        validacion(id);
    });
});

//funcion que llama a la url de eliminar 
function eliminarRegistro(id) {
    window.location.href = `/Eliminar-Mensaje/${id}`;
}

//este apartado captura los datos necesarios para responder al correo
document.querySelectorAll('.far_gmail').forEach(button => {
    button.addEventListener('click', function() {
        const correo = this.getAttribute('data-correo');
        responderCorreo(correo);
    });
});

function responderCorreo(correo){
    window.open(`https://mail.google.com/mail/?view=cm&fs=1&to=${correo}&su=Respuesta&body=`)
}




