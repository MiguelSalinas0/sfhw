window.addEventListener("DOMContentLoaded", function () {
    $("#tab2").DataTable({
        pageLength: 25,
        pagingType: "full_numbers",
        language: {
            decimal: ",",
            emptyTable: "No hay información",
            info: "Mostrando _START_ a _END_ de _TOTAL_ entradas",
            infoEmpty: "Mostrando 0 to 0 de 0 Entradas",
            infoFiltered: "(Filtrado de _MAX_ entradas totales)",
            infoPostFix: "",
            thousands: ".",
            lengthMenu: "Mostrar _MENU_ Entradas",
            loadingRecords: "Cargando...",
            processing: "Procesando...",
            search: "Buscar:",
            zeroRecords: "Sin resultados encontrados",
            paginate: {
                first: "Primero",
                last: "Ultimo",
                next: "Siguiente",
                previous: "Anterior",
            },
        },
    });
});

document.getElementById('sidebarCollapse').addEventListener('click', function () {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('active');
    const sidebarActive = sidebar.classList.contains('active');
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    if (sidebarActive) {
        sidebarCollapse.style.right = '250px';
    } else {
        sidebarCollapse.style.right = '0';
    }
});
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        const sidebar = document.getElementById('sidebar');
        sidebar.classList.remove('active');
        const sidebarCollapse = document.getElementById('sidebarCollapse');
        sidebarCollapse.style.right = '0';
    }
});
$(document).ready(function () {
    $("#miFormulario").submit(function (event) {
        event.preventDefault();
        $.ajax({
            type: "POST",
            url: "/procesar_formulario",
            data: $(this).serialize(),
            success: function (response) {
                $("#search-results").html(response.resultado);
            }
        });
    });
});