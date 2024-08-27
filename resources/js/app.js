document.addEventListener('DOMContentLoaded', function() {
    const formularioUrl = document.getElementById('formularioUrl');
    const tablaResultado = document.getElementById('tablaResultado');
    const cuerpoTablaResultado = document.getElementById('cuerpoTablaResultado');
    const spinner = document.getElementById('spinner');

    if (!formularioUrl || !tablaResultado || !cuerpoTablaResultado || !spinner) {
        console.error('Uno o más elementos no se encontraron.');
        return;
    }

    formularioUrl.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevenir el compartamiento por defecto de la página

        const url = document.getElementById('entradaUrl').value;
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

        // Mostrar el spinner solo cuando se ha enviado el formulario
        spinner.classList.remove('hidden');
        tablaResultado.classList.add('hidden');

        fetch(window.Routes.procesarSolicitud, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-TOKEN': csrfToken
            },
            body: JSON.stringify({ url: url })
        })
        .then(response => response.json())
        .then(data => {
            cuerpoTablaResultado.innerHTML = ''; // Limpiar la tabla

            if (data.length === 0) {
                tablaResultado.classList.add('hidden'); // Ocultar la tabla si no hay datos
            } else {
                data.forEach(item => {
                    const fila = document.createElement('tr');
                    fila.classList.add('bg-white', 'border-b', 'dark:bg-gray-800', 'dark:border-gray-700');

                    // Crear celdas basadas en los datos del JSON
                    Object.values(item).forEach(valor => {
                        const celda = document.createElement('td');
                        celda.classList.add('px-6', 'py-4');
                        celda.textContent = valor;
                        fila.appendChild(celda);
                    });

                    cuerpoTablaResultado.appendChild(fila);
                });

                tablaResultado.classList.remove('hidden'); // Mostrar la tabla si hay datos
            }

            // Ocultar el spinner cuando se ha cargado la tabla
            spinner.classList.add('hidden');
        })
        .catch(error => {
            console.error('Error:', error);
            spinner.classList.add('hidden'); // Ocultar el spinner en caso de error
        });
    });
});