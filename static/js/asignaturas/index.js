$(document).ready( function () {
    // Inicializar Datable para asignaturas
    $('#t_asignaturas').DataTable();
} );

// $('#eliminar_asignatura').on('click', () => {
//     console.log(this.id);
//     $('#nombre').attr("value");
// })

$("button.editar_asignatura").on('click', () => {
    console.log("gila");
    $("#nombre").attr("value");
})