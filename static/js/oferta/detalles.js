// Aqui se importa toastr que es lo que hace posible mostrar los errores o exitos
// como cuadros en la esquina superior derecha del navegador
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

// Esta variable va almacenar el evento de que si el usuario presiono el boton de editar 
// una oferta o no 
let editable = false

function submitForm() {
    $('.tabla-asignaturas-oferta li').each(function(idx, elem) {
        const id = $(elem).attr('data-id')
        $('#input-container').append(`<input type="hidden" name="asignaturas-${idx}-id" value="${id}" />`)
    })

    $('[name="asignaturas-TOTAL_FORMS"]').val($('.tabla-asignaturas-oferta li').length)
    const $form = $('form')
    const url = $form.attr('action')
    const method = $form.attr('method')
    const data = $form.serialize()
    $.ajax({
        method: method,
        data: data,
        url: url,
        success: function(json) {
            const valid = json.valid,
            errors = json.errors.__all__
            // Verifica que no se presente errores 
            if (!valid) {
                // Si se presentan errores entonces se muestra un mensaje de error con el 
                // siguiente contenido
                toastr['error']('', 'Oferta con este Trimestre, Año y Coordinacion ya existe')
            } else {
                // Si no se presenta errores entonces se procede a mandar la informacion 
                // para que sea guardada 
                const $btn = $('#editar')
                const trimestre = $('#id_trimestre')
                const anio = $('#id_anio')
                const otrasAsignaturas = $('#todas-asignaturas')
                otrasAsignaturas.addClass('invisible')
                trimestre.attr('disabled', 'true')
                anio.attr('disabled', 'true')
                $('.tabla-asignaturas-oferta span').addClass('hide')
                $('#helper').addClass('d-none')
                $('#myInput').attr('onkeyup', 'myFunction()')
                $('#myInput').val('')
                $btn.find('span').removeClass('fa-save')
                $btn.find('span').addClass('fa-edit')
                toastr.success("Operación exitosa",'' )
                editable = !editable
            }


        }
    })
}

$(function() {
    $(".sortable").sortable({
      connectWith: ".sortable",
      handle: '.handle'
    }).disableSelection();
    // Maneja el evento de que si se dio click al boton de editar
    $(document).on('click', '#editar', function() {
        $('#myInput').val('')
        myFunction()
        myFunction2()
        // si no es editable entonces se muestra la informacion de la oferta 
        // nada mas y se esconde la lista de todas las asignaturas 
        if (!editable) {
            const $btn = $(this)
            const trimestre = $('#id_trimestre')
            const anio = $('#id_anio')
            const otrasAsignaturas = $('#todas-asignaturas')
            otrasAsignaturas.removeClass('invisible')
            trimestre.removeAttr('disabled')
            anio.removeAttr('disabled')
            $('.tabla-asignaturas-oferta .hide').removeClass('hide')
            $('#helper').removeClass('d-none')
            $('#myInput').attr('onkeyup', 'myFunction2()')
            $(this).find('span').removeClass('fa-edit')
            $(this).find('span').addClass('fa-save')
            editable = !editable
        } else {
            // si es editable entonces se procede a guardar lo cambiado en la oferta 
            // se hace submit al formulario 
            submitForm()
        }
    })
})

$(function() {
    // Declara las variables que van a almacenar la lista de asignaturas 
	var ul, li, icon, i, is_invisible;
	is_invisible = $('#todas-asignaturas').hasClass('invisible');
	if (!is_invisible){
        // Itera sobre toda la lista de asignaturas de la oferta, y muestra permite arrastrar si la
        // lista de todas las asignaturas no esta escondida
		ul = document.getElementById("myUL");
		li = ul.getElementsByTagName('li');
		for (i = 0; i < li.length; i++) {
			icon = li[i].getElementsByTagName("i")[0];
			icon.classList.remove("hide");
		}
	}

});

/**
 * Funcion que quita los acentos de un string
 * @param {string} str string a quitar acento
 */
function removeAccents(str) {
    let accents = 'ÀÁÂÃÄÅàáâãäåßÒÓÔÕÕÖØòóôõöøÈÉÊËèéêëðÇçÐÌÍÎÏìíîïÙÚÛÜùúûüÑñŠšŸÿýŽž';
    let accentsOut = "AAAAAAaaaaaaBOOOOOOOooooooEEEEeeeeeCcDIIIIiiiiUUUUuuuuNnSsYyyZz";
    str = str.split('');
    // Este loop recorre todas las letras de una cadena si consigue una con acento la 
    // reemplaza con la misma pero sin acento
    str.forEach((letter, index) => {
        let i = accents.indexOf(letter);
        if (i != -1) {
            str[index] = accentsOut[i];
        }
    })
    return str.join('');
}
/**
 * Esta funcion implementa la busqueda sobre la lista de 
 * asignaturas de una oferta
 */
function myFunction() {
    // Declara las variables
    // Aqui se toma tanto la busqueda que se va a hacer 
    // y la lista donde se hace la busqueda 
    var input, filter, ul, li, i;
    input = document.getElementById('myInput');
    filter = removeAccents(input.value.toUpperCase());
    ul = document.querySelector(".tabla-asignaturas-oferta ul");
    li = ul.getElementsByTagName('li');

    // Itera sobre todas los elementos de la lista de asignaturas y descarta aquellos que no 
    // coincidan con la busqueda
    // Esto se hace cada vez que se introduce una letra al cuadro de input de buscar
    for (i = 0; i < li.length; i++) {
            if (removeAccents(li[i].innerHTML.toUpperCase()).indexOf(filter) > -1) {
                    li[i].style.display = "";
            } else {
                    li[i].style.display = "none";
            }
    }
}

/**
 * Esta funcion implementa la busqueda sobre la lista de todas las asignaturas 
 * que estan registradas 
 */
function myFunction2() {
    // Declara las variables 
    // Aqui se toma la busqueda que se va hacer que es la informacion introducida 
    // por el usuario en el box de buscar
    // Y la lista de todas las asignaturas 
    var input, filter, ul, li, i;
    input = document.getElementById('myInput');
    filter = removeAccents(input.value.toUpperCase());
    ul = document.querySelector("#todas-asignaturas ul");
    li = ul.getElementsByTagName('li');

    // Aqui se itera sobre toda la lista y se ve quitando las asignaturas que no 
    // coincidan con la busqueda que esta realizando el usuario
    for (i = 0; i < li.length; i++) {
        if (removeAccents(li[i].innerHTML.toUpperCase()).indexOf(filter) > -1) {
                li[i].style.display = "";
        } else {
                li[i].style.display = "none";
        }
    }
}
