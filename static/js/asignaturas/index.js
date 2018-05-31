toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": false,
    "positionClass": "toast-top-right",
    "preventDuplicates": true,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}
const asigIdContainer = '#asig-container'
var tablaAsignaturas
$(document).ready( function () {
    // Inicializar Datable para asignaturas
    const tablaUrl = $('[name="tabla-json"]').val()
    tablaAsignaturas = $('#t_asignaturas').DataTable({
        'ajax': tablaUrl
    });

    $(asigIdContainer).on('submit', '#form-modal', function (e) {
        const $form = $(this)
        e.preventDefault()
        $.ajax({
            url: $form.attr('action'),
            method: $form.attr('method'),
            data: $form.serialize(),
            success: function (json) {
                const html = json.html,
                    valid = json.valid

                if (!valid) {
                    toastr["error"]("", "Tiene errores en el formulario")
                    $(asigIdContainer).html(html)
                    activarPlugins()
                } else {
                    toastr["success"]("", "Materia creada")
                    $('#agregar-modal').modal('hide')
                    tablaAsignaturas.ajax.reload()
                }
            }
        })
    })
} );

var edit_mode = false;
function activarPlugins() {
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
    $('.fselect').fSelect({
        placeholder: 'Escoja al menos un profesor',
        numDisplayed: 3,
        overflowText: '{n} seleccionados',
        searchText: 'Buscar',
        showSearch: true
    });
    $.fn.datepicker.defaults.format = "dd/mm/yyyy";

    $('.datepicker').datepicker()
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
    edit_mode = true;
    $('.editar_asignatura').toggleClass('active');
}

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

    $('.delete-form input').attr('type', 'button');

    console.log('agregar', agregar)
    if (!agregar) {
        $('#submit-btn').addClass('d-none');
        $('.asignatura-btn').removeClass('d-none');
    }
    else {
        activarPlugins()

        $('#submit-btn').removeClass('d-none');
        $('.asignatura-btn').addClass('d-none');
    }
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
        success: (form) => {
            $(asigIdContainer).html(form);
            show_informacion_modal(agregar);
            edit_mode = false;
        },
        error: (err) => {
            console.log(err)
        }
    })
}
