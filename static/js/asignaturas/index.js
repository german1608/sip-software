$(document).ready( function () {
    // Inicializar Datable para asignaturas
    $('#t_asignaturas').DataTable();
} );

var edit_mode = false;

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

/**
 * Mostrar el modal para mostrar la informacion de la asignatura 
 * @param agregar booleano que dice si es un modal para agregar una nueva asignatura
 */
function show_informacion_modal(agregar){
    $('#agregar-modal').modal();
     /**
     * Se setean los rangos
     */
    $('#creditos').attr('min', '0');
    $('#creditos').attr('max', '10');

    $('.horario-input').attr('min', '1');
    $('.horario-input').attr('max', '12');

    $('.delete-form input').attr('type', 'button');

    activarFormSets();
    console.log('agregar', agregar)
    if (!agregar) {
        deshabilitarForm();
        $('#submit-btn').addClass('d-none');
        $('.asignatura-btn').removeClass('d-none');
    }
    else {
        $('#submit-btn').removeClass('d-none');
        $('.asignatura-btn').addClass('d-none');
    }
}

function deshabilitarForm() {
    // Se anade las clases readonly al input para que no sea modificable
    $('.anadir-horario-btn').addClass('disabled');
    $('.mostrar-only').attr('readonly', "");
    $('.mostrar-only').attr('disabled', '');
    $('.mostrar-only').attr('class', "mostrar-only form-control-plaintext");
    $('.delete-row').addClass('d-none');
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
    console.log(edit_mode)
    switch (edit_mode) {
        case false:
            $('.anadir-horario-btn').removeClass('disabled');
            $('.mostrar-only').removeAttr('readonly');
            $('.mostrar-only').removeAttr('disabled');
            $('.mostrar-only').attr('class', "mostrar-only form-control");
            $('.delete-row').removeClass('d-none');

            /**
             * Se coloca un icono de guardado
             */
            $('.editar_asignatura').html('<i class="far fa-save"></i>');
            $('.editar_asignatura').removeClass('btn-success');
            $('.editar_asignatura').addClass('btn-primary');
            break;
        case true:
            $('#submit-btn').click();
            break;
    }
    edit_mode = !edit_mode;
    $('.editar_asignatura').toggleClass('active');
}


/**
 * Obtener del backend información de la asignatura cuando
 * se abre el modal para editar.
 * @param btn botón presionado
 * @param url url a donde hacer el GET request
 * @param agregar booleano que dice si es un modal para agregar
 */
function obtenerAsignatura(btn, url, agregar) {
        $.ajax({
        url: url,
        method: 'GET',
        data: {
            codasig: $(btn).data('codasig')
        },
        success: (form) => {
            $('#agregar-modal').replaceWith(form);
            show_informacion_modal(agregar);
            edit_mode = false;
        }
    })
}
