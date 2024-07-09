function eliminarRegistro(ficha, curso) {
    window.location.href = `/eliminarFicha/${ficha}/${curso}` ;
}

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
function validacion(ficha, curso) {
    Swal.fire({
        title: "¿Seguro?",
        text: `Esta acción eliminará la ficha ${ficha} permanentemente.`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "¡Sí, borrar!",
        cancelButtonText: 'Cancelar',
    }).then((result) => {
        if (result.isConfirmed) {
            eliminarRegistro(ficha, curso);
        } else {
            mensajeCancelacion();
        }
    });
}