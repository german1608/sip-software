$(document).ready( function () {
    // Inicializar Datable para asignaturas
    $('#t_asignaturas').DataTable();
} );

/**
 * Mostrar modal para eliminar asignatura.
 * @param btn Botón presionado
 */
function show_eliminar_modal(btn) {
    // Obtener código de asignatura
    let codasig = $(btn).data('codasig');

    // Actualizar data del modal
    $('.asignatura-a-eliminar').html(codasig);
    $('#confirmar-eliminar-modal input[name=codasig]').val(codasig);
}