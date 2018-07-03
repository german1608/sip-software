
// Este es un plugin que se encarga de mostrar los errores del formulario 
// de una manera estilizada 
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
// Función que es inicializada al cargar la página de asignaturas
// para renderizar la tabla con la lista de todas las asignaturas
// y activar el selector que detecta la acción de agregar una
// asignatura o editarla.
const asigIdContainer = '#asig-container'
var tablaAsignaturas
$(document).ready( function () {
    // Inicializar Datable para asignaturas
    const tablaUrl = $('[name="tabla-json"]').val()
    tablaAsignaturas = $('#t_asignaturas').DataTable({
        'ajax': tablaUrl
    });

    if ($('#new').attr('data-activar')){
        console.log($('#new').attr('data-activar'))
        var url = '/asignaturas/detalles/' + $('#new').attr('data-id')
        obtenerAsignaturaOferta(url, false);
    } 
    // Selector que desencadena una llamada AJAX al hacer clic
    // en el botón de agregar una asignatura verificando
    // si los campos introducidos son válidos. En caso de ser
    // validos dichos datos la asignatura es añadida a la base
    // de datos y el modal se cierra y se muestra un 
    // mensaje de exito. En caso contrario, se muestra un 
    // mensaje de error para que el usuario verifique los datos
    // introducidos.
    $(asigIdContainer).on('submit', '#form-modal', function (e) {
        const $form = $(this)
        e.preventDefault()
        $.ajax({
            url: $form.attr('action'),
            method: $form.attr('method'),
            data: $form.serialize(),
            success: function (json) {
                const html = json.html,
                    valid = json.valid,
                    errors = json.errors
                if (!valid) {
                    $(asigIdContainer).html(html)
                    $('#info-pan').tab('show');
                    if ($('#form-modal [name=id]').val() === '') {
                        $('#submit-btn').removeClass('d-none')
                    }
                    activarPlugins()
                    toastr['error']('', errors[0][0])
                    for (key in errors.slice(1)) {
                        console.log(key)
                        if (errors[key][0].length)
                            toastr["error"]("", errors[key][0])
                    }
                } else {
                    toastr["success"]("", "Procedimiento exitoso")
                    $('#agregar-modal').modal('hide')
                    tablaAsignaturas.ajax.reload()
                }
            }
        })
    })

    // Selector para enviar mediante AJAX la solicitud de eliminación de 
    // una asignatura al pulsar el botón de eliminar. En éxito, se 
    // recarga la lista de asignaturas 
    $('#form-eliminar').on('submit', function (e) {
        e.preventDefault()
        const form = $(this)
        $.ajax({
            method: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function (res) {
                toastr["success"]("", "Asignatura Eliminada")
                $("#confirmar-eliminar-modal").modal('hide')
                $('#agregar-modal').modal('hide')
                tablaAsignaturas.ajax.reload()
            },
            error: function (e) {
            }
        })
    })
} );

var edit_mode = false;
// Activa los plugins necesarios para la selección múltiple
// de horarios, programas y profesores en el formulario de
// asignaturas.
function activarPlugins() {
    const horarioPrefix = $('[name=horario_formset_prefix]').val()
    const programaPrefix = $('[name=programa_formset_prefix]').val()
    $('#horario .form-row').formset({
        prefix: horarioPrefix,
        formCssClass: 'dynamic-formset1',
        'addText': 'Añadir horario',
        'addCssClass': 'btn btn-success anadir-horario-btn'
    })
    // Al igual 
    $('#programa .form-group').formset({
        prefix: programaPrefix,
        formCssClass: 'dynamic-formset2',
        'addText': 'Añadir programa',
        'addCssClass': 'btn btn-success  anadir-horario-btn'
    })
    // Es un cuadro que permite seleccionar distintos profesores para
    // una asignatura 
    $('.fselect').fSelect({
        placeholder: 'Escoja al menos un profesor',
        numDisplayed: 3,
        overflowText: '{n} seleccionados',
        searchText: 'Buscar',
        showSearch: true
    });
    // Este es el plugin del calendario para escoger una fecha
    $.fn.datepicker.defaults.format = "dd/mm/yyyy";

    $('.datepicker').datepicker()
}

/**
 * Habilitar los input para modificar los campos
 * @param btn Boton para habilitar la edicion de la asignatura
 */
// Esto se hace cuando se presiona el boton de editar
function habilitar_edicion(btn){
    if (!edit_mode) {
        $.ajax({
            url: $(btn).attr('data-url'),
            data: {
                'id': $(btn).attr('data-id'),
            },
            method: 'GET',
            success: function (form) {
                $(asigIdContainer).html(form)
                $('#info-pan').tab('show')
                activarPlugins()
                /**
                 * Se coloca un icono de guardado
                 */
                $('.editar_asignatura').html('<i class="far fa-save"></i>');
                $('.editar_asignatura').removeClass('btn-success');
                $('.editar_asignatura').addClass('btn-primary');
            }
        })
    }
    else {
        $('#submit-btn').click();
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
        console.log("proeans")
        $('#submit-btn').addClass('d-none');
        $('.asignatura-btn').removeClass('d-none');
        $('.editar_asignatura').html('<i class="far fa-edit"></i>');
        $('.editar_asignatura').addClass('btn-success');
        $('.editar_asignatura').removeClass('btn-primary');

        $('#eliminar-btn').attr('data-codasig', $('[name="detail_codasig"]').val())
        $('.editar_asignatura').attr('data-id', $('[name="detail_id"]').val())
    }
    else {
        // activarPlugins()
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
            console.log(form)
            $(asigIdContainer).html(form);
            // $('#info-pan').tab('show')
            show_informacion_modal(agregar);
            edit_mode = false;
        },
        error: (err) => {
            console.log(err)
        }
    })
}

// Esta funcion permite que cuando se haga click en una asignatura desde la vista 
// de oferta se rediriga a la vista de asignaturas y se abra el modal que muestra 
// la informacion de la asignatura en cuestion
// Se usa ajax para poder hacerlo
/**
 * 
 * @param url direccion donde se obtiene la materia al cual se le dio click 
 * @param agregar este parametro le permite saber si el modal que se va a mostrar es de edicion o no 
 */
function obtenerAsignaturaOferta(url, agregar) {
    $.ajax({
        url: url,
        method: 'GET',
        success: (form) => {
            $(asigIdContainer).html(form);
            $('#info-pan').tab('show')
            show_informacion_modal(agregar);
            edit_mode = false;
        },
        error: (err) => {
            console.log(err)
        }
    })
}
