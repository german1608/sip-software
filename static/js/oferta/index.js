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


// Esta funcion sirve para mostrar las ofertas que estan presentes en la 
// base de datos. Esto lo hace cuando se carga la vista de las ofertas o 
// cuando se agrega una nueva oferta. 
function oferta_show(data){
    console.log(data)
    $(".oferta").remove()
    const $this = $(this)

    // Se obtiene el json que contiene la informacion de las ofertas que estan 
    // en la base de datos.
    const url_json = $('[name=json-url]').attr('value')
    // Se obtiene la url generica que servira para asignarle una url
    // especifica de eliminacion a cada oferta segun su id.
    var url_elim = $('[name=eliminar-url]').attr('value')

    // Este es el ajax para anadir las nuevas ofertas 
    $.ajax ({
        dataType: "json",
        url: url_json,
        data: data,
        success: function (json){
            // Aqui se recorren todas las ofertas y se van agregando 
            // al html para que se muestren por pantalla 
            json.data.forEach(oferta => {
                $('#oferta-box').append(`

                    <div class="col-12 col-sm-3 oferta oferta-child">
                          
                        <div class="flip3D">
                            <div class="back" id="editar-oferta-form-${oferta.id}">
                                
                            </div>
                           
                                <div class="front" id="editar-oferta-box-${oferta.id}">
                                
                                    <div class="management-btns">
                                        <a class="oferta-elim" data-url="${url_elim.replace('0', oferta.id)}">
                                            <span class="delete-btn"><i class="fa fa-window-close"></i></span>
                                        </a>
                                    </div>
                                    <a href="detalle/${oferta.id}"> <p class="front-text">${oferta.trimestre} <br> ${oferta.anio}</p></a>
                                    
                                </div>
                                
                        </div>
                        
                    </div>
               `)
                // En este if se verifica que la cantidas de ofertas que se tienen es multiplo de 4
                // si lo son se agrega un nuevo div que permite agrupar las ofertas en filas de 4
                if ($('.oferta-child').length % 4 === 0){
                    $('#oferta-box').append('<div class="w-100 oferta"></div>')
                }
            })
        },
        error: function(jqXHR, ...args) {
            // En esta parte del codigo se maneja los errores que se 
            // obtuvo y se muestran por pantalla 
            const err = jqXHR.responseJSON
            toastr.error('', err.error)
        }
    })
}

// Esta funcion esta encargada en manejar la edicion de una oferta 
function editar_oferta(id){
    // Se selecciona el div que contiene la oferta a editar
    const selector = "#oferta-editar-" + id
    const $this = $(selector)
    const url = $(selector).attr('data-url')

    // Aqui se ejecuta el ajax para hacer la modificacion de la oferta 
    // con los nuevos datos introducidos por el usuario.
    $.ajax({
        url: $this.attr('data-url'),
        method: 'GET',
        success: function (json) {
            // LLena el formulario
            $('#editar-oferta-form-' + id).html(json)
            $('#editar-oferta-form-' + id + ' form').attr('action', url)
            // Voltea la carta
            $('#editar-oferta-box-' + id).parent().addClass('active')
            $('#boton-agregar').attr("hidden", true)
            $('#boton-editar').attr("hidden", false)
        }
    })
}

function actualizar(){
    // $( "#mes_inicio" ).val(), $( "#ano_inicio" ).val(), $( "#mes_final" ).val(), $( "#ano_final" ).val()
    oferta_show({
        'trim_inicio': $('#trim_inicio').val(),
        'anio_inicio': $('#anio_inicio').val(),
        'trim_final': $('#trim_final').val(),
        'anio_final': $('#anio_final').val()
    });    
}


$(function() {

    // Se llama a la funcion oferta_show() para 
    // mostrar todas las ofertas por pantalla 
    oferta_show()

    // Este selector implementa la funcionalidad de la carta 
    // anadir 
    $('#oferta-add').on('click', function(e) {
        const $this = $(this)
        // Este ajax se encarga de crear el formulario y agregarlo a la cartica 
        // de agregar 
        $.ajax({
            url: $this.attr('data-url'),
            method: 'GET',
            success: function (json) {
                // LLena el formulario
                $('#create-oferta-form').html(json)
                // Voltea la carta
                $('#create-oferta-box').parent().addClass('active')
            }
        })
    })


    // Selector que maneja el evento de cuando el usuario anade una nueva 
    // oferta
    $(document).on('submit', '#form-oferta', function(e) {
        e.preventDefault()
        const $form = $(this)
        // Este ajax se encarga de mostrar si el proceso de anadir una nueva 
        // oferta ha sido realizado con exito si no se muestra un error 
        $.ajax({
            url: $form.attr('action'),
            method: $form.attr('method'),
            data: $form.serialize(),
            success: function (json) {
                // LLena el formulario
                // Voltea la carta
                $('#create-oferta-box').parent().removeClass('active')
                if ($('[name=id]').attr('value') === ''){
                    toastr.success('Oferta añadida con éxito', '')
                }
                else {
                    toastr.success('Oferta editada con éxito', '')
                }
                oferta_show()
            },
            error: function(jqXHR, ...args) {
                // En esta parte del codigo se maneja los errores que se 
                // obtuvo y se muestran por pantalla 
                const err = jqXHR.responseJSON
                for (let k in err){
                    err[k].forEach(error => {
                        toastr.error('', error)
                    })
                }
            }
        })
                
    })
})

// Selector que desencadena una llamada a AJAX al click en
// cualquier boton con la marca 'x' de las tarjetas de
// eliminacion de ofertas
$(document).on('click', '.oferta-elim', function(e) {
    const url_elim = $(this).attr('data-url');
    // Se realiza una llamada al controlador para renderizar
    // el modal de la oferta con los datos especificos de
    // esa oferta.
    $.ajax({
        url: url_elim,
        method: 'GET',
        success: function (json) {
            $("#oferta-modal-trimestre").html(json.trimestre);
            $("#oferta-modal-anio").html(json.anio);
            $("#oferta-modal-coordinacion").html(json.coordinacion);
            $("#form-eliminar-oferta").attr('action', url_elim);
            $("#dangerModal").modal('show');
        }
    })    
})

// Selector que desencadena una llamada a AJAX al hacer submit
// sobre botón de eliminar en el modal de eliminación de una oferta.
$(document).on('submit', '#form-eliminar-oferta', function(e) {
    e.preventDefault();
    const $form = $(this)

    // La llamada solicita al controlador la eliminacion de
    // la oferta seleccionada y devuelve una respuesta de
    // exito o fracaso.
    $.ajax({
        url: $form.attr('action'),
        method: $form.attr('method'),
        data: $form.serialize(),
        success: function (json) {
            // Al recibir una respuesta de la llamada, se 
            // cierra el modal y se muestra el mensaje
            // con el estado de la solicitud de eliminacion
            $("#dangerModal").modal('hide');
            if(json.ok){
                toastr.success('Oferta eliminada con éxito', '');
                oferta_show();
            }
            else{
                toastr.error('Se produjo un error al eliminar la oferta', '');
                oferta_show();
            }
            
        }
    })    
})