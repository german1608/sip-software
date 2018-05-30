$(document).ready( function () {
    // Inicializar Datable para asignaturas
    $('#t_asignaturas').DataTable();
    activarFormSets();
} );

var edit_mode = false;

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
function show_informacion_modal(){
    $('#agregar-modal').modal();
    activarFormSets();
    deshabilitarForm();
}

function deshabilitarForm() {
    // Se anade las clases readonly al input para que no sea modificable
    $('.anadir-horario-btn').addClass('disabled');
    $('.mostrar-only').attr('readonly', "");
    $('.mostrar-only').attr('disabled', '');
    $('.mostrar-only').attr('class', "mostrar-only form-control-plaintext");
}

function activarFormSets() {
    const horarioPrefix = $('[name=horario_formset_prefix]').val()
    const programaPrefix = $('[name=programa_formset_prefix]').val()
    $('#horario .form-row').formset({
        prefix: horarioPrefix,
        formCssClass: 'dynamic-formset1',
        'addText': 'Añadir horario',
        'addCssClass': 'btn btn-success anadir-horario-btn'
    })
    $('#programa .form-group').formset({
        prefix: programaPrefix,
        formCssClass: 'dynamic-formset2',
        'addText': 'Añadir programa',
        'addCssClass': 'btn btn-success  anadir-horario-btn'
    })
}

/**
 * Habilitar los input para modificar los campos 
 * @param btn Boton para habilitar la edicion de la asignatura 
 */
function habilitar_edicion(btn){
    switch (edit_mode) {
        case false:
            $('.anadir-horario-btn').removeClass('disabled');
            $('.mostrar-only').removeAttr('readonly');
            $('.mostrar-only').removeAttr('disabled');
            $('.mostrar-only').attr('class', "mostrar-only form-control");
            break;
        case true:
            deshabilitarForm();
            break;
    }
    edit_mode = !edit_mode;
    $('.editar_asignatura').toggleClass('active');
}


/**
 * Obtener del backend información de la asignatura cuando
 * se abre el modal para editar.
 */
function obtenerAsignatura(btn) {
    $.ajax({
        url: '/asignaturas/editar',
        method: 'GET',
        data: {
            codasig: $(btn).data('codasig')
        },
        success: (data) => {
            asig = JSON.parse(data[0])[0];
            let form = data[1];
            console.log(form);
            $('#agregar-modal').replaceWith(form);
            show_informacion_modal();
        }
    })
}