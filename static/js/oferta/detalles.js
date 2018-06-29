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
        success: function(data) {
            console.log(data)
        }
    })
}

$(function() {
    $(".sortable").sortable({
      connectWith: ".sortable",
      handle: '.handle'
    }).disableSelection();
    $(document).on('click', '#editar', function() {
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
        } else {
            submitForm()
        }
        editable = !editable
    })
})

$(function() {
	// Declare variables
	var ul, li, icon, i, is_invisible;
	is_invisible = $('#todas-asignaturas').hasClass('invisible');
	if (!is_invisible){
		// Loop through all list items, and show hamburguers to drag if
		// below list is not hidden
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
    str.forEach((letter, index) => {
        let i = accents.indexOf(letter);
        if (i != -1) {
            str[index] = accentsOut[i];
        }
    })
    return str.join('');
}

function myFunction() {
    // Declare variables
    var input, filter, ul, li, i;
    input = document.getElementById('myInput');
    filter = removeAccents(input.value.toUpperCase());
    ul = document.querySelector(".tabla-asignaturas-oferta ul");
    li = ul.getElementsByTagName('li');

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
            if (removeAccents(li[i].innerHTML.toUpperCase()).indexOf(filter) > -1) {
                    li[i].style.display = "";
            } else {
                    li[i].style.display = "none";
            }
    }
}
function myFunction2() {
    // Declare variables
    var input, filter, ul, li, i;
    input = document.getElementById('myInput');
    filter = removeAccents(input.value.toUpperCase());
    ul = document.querySelector("#todas-asignaturas ul");
    li = ul.getElementsByTagName('li');

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
        if (removeAccents(li[i].innerHTML.toUpperCase()).indexOf(filter) > -1) {
                li[i].style.display = "";
        } else {
                li[i].style.display = "none";
        }
    }
}
