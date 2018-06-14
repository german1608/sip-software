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

$(function() {
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
