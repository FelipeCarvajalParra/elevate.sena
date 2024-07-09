// Función para agregar documento a la lista si no es nulo o vacío
function agregarDocumento(doc, documentos) {
    if (doc) {
        documentos.push(doc);
    }
    return documentos
}

document.querySelectorAll('.far_vista').forEach(button => {
    button.addEventListener('click', function() {
        const tdoc_aspir = this.getAttribute('data-tdoc_aspir');
        const docu_aspir = this.getAttribute('data-docu_aspir');
        const pnom_aspir = this.getAttribute('data-pnom_aspir');
        const snom_aspir = this.getAttribute('data-snom_aspir');
        const pape_aspir = this.getAttribute('data-pape_aspir');
        const sape_aspir = this.getAttribute('data-sape_aspir');
        const gene_aspir = this.getAttribute('data-gene_aspir');
        const pais_aspir = this.getAttribute('data-pais_aspir');
        const fech_aspir = this.getAttribute('data-fech_aspir');
        const nive_aspir = this.getAttribute('data-nive_aspir');
        const area_aspir = this.getAttribute('data-area_aspir');
        const carg_aspir = this.getAttribute('data-carg_aspir');
        const sect_aspir = this.getAttribute('data-sect_aspir');
        const empl_aspir = this.getAttribute('data-empl_aspir');
        const arl_aspir = this.getAttribute('data-arl_aspir');
        const curs_ficha = this.getAttribute('data-curs_ficha');
        const doc0 =  this.getAttribute('data-doc0');
        const doc1 =  this.getAttribute('data-doc1');
        const doc2 =  this.getAttribute('data-doc2');
        const doc3 =  this.getAttribute('data-doc3');

        // Array para almacenar los nombres de los documentos
        let documentos = [];

        // Agregar documentos según el curso
        if (curs_ficha == 2) {
            agregarDocumento(this.getAttribute('data-doc4'), documentos);
        } else if (curs_ficha == 3) {
            agregarDocumento(this.getAttribute('data-doc4'), documentos);
            agregarDocumento(this.getAttribute('data-doc5'), documentos);
        } else if (curs_ficha == 4) {
            agregarDocumento(this.getAttribute('data-doc4'), documentos);
            agregarDocumento(this.getAttribute('data-doc5'), documentos);
            agregarDocumento(this.getAttribute('data-doc6'), documentos);
            agregarDocumento(this.getAttribute('data-doc7'), documentos);
            agregarDocumento(this.getAttribute('data-doc8'), documentos);
            agregarDocumento(this.getAttribute('data-doc9'), documentos);
            agregarDocumento(this.getAttribute('data-doc10'), documentos);
            agregarDocumento(this.getAttribute('data-doc11'), documentos);
        } else if (curs_ficha == 5) {
            agregarDocumento(this.getAttribute('data-doc4'), documentos);
        } else if (curs_ficha == 6) {
            console.log("entro")
            agregarDocumento(this.getAttribute('data-doc4'), documentos);
            agregarDocumento(this.getAttribute('data-doc5'), documentos);
        }

        // Llamar a la función mostrarMensaje con los datos obtenidos
        mostrarMensaje(
            tdoc_aspir, 
            docu_aspir, 
            pnom_aspir, 
            snom_aspir, 
            pape_aspir, 
            sape_aspir, 
            gene_aspir, 
            pais_aspir, 
            fech_aspir, 
            nive_aspir, 
            area_aspir, 
            carg_aspir, 
            sect_aspir,
            empl_aspir, 
            arl_aspir,
            doc0,
            doc1,
            doc2,
            doc3,
            documentos
        );
    });
});

function mostrarMensaje(
    tdoc_aspir, 
    docu_aspir, 
    pnom_aspir, 
    snom_aspir, 
    pape_aspir, 
    sape_aspir, 
    gene_aspir, 
    pais_aspir, 
    fech_aspir, 
    nive_aspir, 
    area_aspir, 
    carg_aspir, 
    sect_aspir,
    empl_aspir, 
    arl_aspir,
    doc0,
    doc1,
    doc2,
    doc3,
    documentos
) {
    console.log(documentos); // Mostrar en consola los documentos para verificar

    // Construir la lista de documentos en HTML
    let documentosHTML = '';
    documentos.forEach(doc => {
        documentosHTML += `<li><a href="/media/${doc}" target="_blank"><p>${obtenerNombreDocumento(doc)}</p></a></li>`;
    });
    Swal.fire({
        customClass: {
            popup: 'ventana'
        },
        html: `
        <div class="contenedor">
            <h2>Informacion</h2>
            <p><b>Tipo de documento:</b> ${tdoc_aspir}</p>
            <p><b>Documento:</b> ${docu_aspir}</p>
            <p><b>Nombre/s:</b> ${pnom_aspir} ${snom_aspir}</p>
            <p><b>Apellidos:</b> ${pape_aspir} ${sape_aspir}</p>
            <p><b>Género:</b> ${gene_aspir}</p>
            <p><b>País:</b> ${pais_aspir}</p>
            <p><b>Fecha de nacimiento:</b> ${fech_aspir}</p>
            <p><b>Nivel:</b> ${nive_aspir}</p>
            <p><b>Área:</b> ${area_aspir}</p>
            <p><b>Cargo:</b> ${carg_aspir}</p>
            <p><b>Empleado:</b> ${empl_aspir}</p>
            <p><b>ARL:</b> ${arl_aspir}</p>
            <p><b>Sector:</b> ${sect_aspir}</p><br>
            <h2>Documentos</h2>
            <ol>
                <li><a href="/media/${doc1}" target="_blank"><p>Cedula</p></a></li>
                <li><a href="/media/${doc2}" target="_blank"><p>Examen aptitud en alturas</p></a></li>
                <li><a href="/media/${doc3}" target="_blank"><p>Pago seguridad social y ARL</p></a></li>
                ${documentosHTML}
                <li><a href="/media/${doc0}" target="_blank"><p>Requisitos previos</p></a></li>
            </ol>
            
            
            
            
        </div>
        `,

        denyButtonColor: '#ed5564',
    }).then((result) => {
        if (result.isConfirmed) {
            var botones = document.querySelectorAll('.far_gmail');
            botones.forEach(function(boton) {
                boton.click();
            });
        } else if (result.isDenied) {
            validacion(docu_aspir);
        }
    });
}



// Función para obtener el nombre del documento a partir de su ruta
function obtenerNombreDocumento(path) {
    const parts = path.split('/');
    return parts[parts.length - 1];
}




















function eliminarRegistro(registro, ficha) {
    window.location.href = `/eliminarRegistro/${registro}/${ficha}` ;
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
function validacion(registro, ficha) {
    Swal.fire({
        title: "¿Seguro?",
        text: `Esta acción eliminará el estudiante de la ficha.`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "¡Sí, borrar!",
        cancelButtonText: 'Cancelar',
    }).then((result) => {
        if (result.isConfirmed) {
            eliminarRegistro(registro, ficha);
        } else {
            mensajeCancelacion();
        }
    });
}