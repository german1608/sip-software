$(document).ready( function () {
    // Inicializar Datable para asignaturas
    $('#t_asignaturas').DataTable();
    const horarioPrefix = $('[name=horario_formset_prefix]').val()
    const programaPrefix = $('[name=programa_formset_prefix]').val()
    $('#horario .form-row').formset({
        prefix: horarioPrefix,
        formCssClass: 'dynamic-formset1',
        'addText': 'Añadir horario',
        'addCssClass': 'btn btn-success'
    })
    $('#programa .form-group').formset({
        prefix: programaPrefix,
        formCssClass: 'dynamic-formset2',
        'addText': 'Añadir programa',
        'addCssClass': 'btn btn-success'
    })
} );

/**
 * Mostrar modal para eliminar asignatura.
 * @param btn Botón presionado
 */
function show_eliminar_modal(btn) {
    // Obtener código de asignatura
    let codasig = $(btn).data('codasig');
    console.log(codasig);
    // Actualizar data del modal
    $('.asignatura-a-eliminar').html(codasig);
    $('#confirmar-eliminar-modal input[name=codasig]').val(codasig);
}

/**
 * Mostrar el modal para mostrar la informacion de la asignatura 
 * @param a Link de la tabla de asignaturas 
 */
function show_informacion_modal(a){
    let nombre = $(a).data('nombre');
    console.log(nombre);

    // Se anade las clases readonly al input para que no sea modificable
    $('#nombre-asig').val(nombre);
    $('.mostrar-only').attr('readonly', "");
    $('.mostrar-only').attr('class', "mostrar-only form-control-plaintext");
}

/**
 * Habilitar los input para modificar los campos 
 * @param btn Boton para habilitar la edicion de la asignatura 
 */
function habilitar_edicion(btn){
    $('.mostrar-only').removeAttr('readonly');
    $('.mostrar-only').attr('class', "mostrar-only form-control");
}
