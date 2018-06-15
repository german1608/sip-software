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

function oferta_show(){
    $(".oferta").remove()
    const $this = $(this)
    const url_json = $('[name=json-url]').attr('value')
    
    $.ajax ({
        dataType: "json",
        url: url_json,
        // 
        success: function (json){
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
                                <span class="delete-btn"><i class="fa fa-window-close"></i></span>
                                <span class="edit-btn"><i class="fa fa-pencil-alt"></i></span>
                            </div>
                            <p class="front-text">${oferta.trimestre} <br> ${oferta.anio}</p>
                        </div>
                    </div>
                </div>`)
                console.log($('.oferta-child').length)
                if ($('.oferta-child').length % 4 === 0){
                    $('#oferta-box').append('<div class="w-100 oferta"></div>')
                }
            })
        }
    })

    
    
}

$(function() {
    oferta_show()
    $('#oferta-add').on('click', function(e) {
        const $this = $(this)
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

    $(document).on('submit', '#form-oferta', function(e) {
        e.preventDefault()
        const $form = $(this)

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
