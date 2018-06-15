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
function oferta_show(){
    // Primero se borran las ofertas que estan en la pagina en ese momento 
    // si no se acumulan porque cuando se agregan las nuevas se vuelven agregar
    // las anteriores
    $(".oferta").remove()
    const $this = $(this)
    // Se obtiene el json que contiene la informacion de las ofertas que estan 
    // en la base de datos.
    const url_json = $('[name=json-url]').attr('value')
    var url_elim = $('[name=eliminar-url]').attr('value')

    // Este es el ajax para anadir las nuevas ofertas 
    $.ajax ({
        dataType: "json",
        url: url_json,
        // 
        success: function (json){
            // Aqui se recorren todas las ofertas y se van agregando 
            // al html para que se muestren por pantalla 
            json.data.forEach(oferta => {
                $('#oferta-box').prepend(`
                <div class="col-3 oferta oferta-child">
                    <div class="flip3D">
                        <div class="back">
                            <form action="#" method="POST" id="">
                
                            <div class="form-group">
                                <label for="trimestre"><span class=""></span> Trimestre: </label>
                                <select>
                                    <option>Ene-Mar</option>
                                    <option>Abr-Jul</option>
                                    <option>Sep-Dic</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label for="anio"><span class=""></span> Año: </label>
                                <input type="number" name="">
                
                            </div>
                
                            </form>
                        </div>
                        <div class="front">
                            <div class="management-btns">
                                <a class="oferta-elim" data-url="${url_elim.replace('0', oferta.id)}">
                                    <span class="delete-btn"><i class="fa fa-window-close"></i></span>
                                </a>
                                <span class="edit-btn"><i class="fa fa-pencil-alt"></i></span>
                            </div>
                            <p class="front-text">${oferta.trimestre} <br> ${oferta.anio}</p>
                        </div>
                    </div>
                </div>`)
                // En este if se verifica que la cantidas de ofertas que se tienen es multiplo de 4
                // si lo son se agrega un nuevo div que permite agrupar las ofertas en filas de 4
                if ($('.oferta-child').length % 4 === 0){
                    $('#oferta-box').append('<div class="w-100 oferta"></div>')
                }
            })
        }
    })

    
    
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
                toastr.success('Oferta añadida con éxito', '')
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

$(document).on('click', '.oferta-elim', function(e) {
    const url_elim = $(this).attr('data-url');
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

$(document).on('submit', '#form-eliminar-oferta', function(e) {
    e.preventDefault();
    const $form = $(this)

    $.ajax({
        url: $form.attr('action'),
        method: $form.attr('method'),
        data: $form.serialize(),
        success: function (json) {
            $("#dangerModal").modal('hide');
            console.log(json.ok)
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