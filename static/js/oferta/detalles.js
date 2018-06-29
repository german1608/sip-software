var hidden = false;
function action() {
    hidden = !hidden;
    if(hidden) {
        document.getElementById('editar').style.visibility = 'hidden';
        document.getElementById('guardar').style.visibility = 'visible';
        document.getElementById("mySelect").disabled=false;
        document.getElementById("anio").contentEditable = true;
        document.getElementById("table").style.visibility = "visible";



    } else {
        document.getElementById('editar').style.visibility = 'visible';
        document.getElementById('guardar').style.visibility = 'hidden';
        document.getElementById("mySelect").disabled=true;
        document.getElementById("anio").contentEditable = false;
        document.getElementById("table").style.visibility = "hidden";

    }
}

function toggleEditable() {

	let editBtn = document.querySelector('.btn--edit');

	if (editBtn.style.display === 'none') {

        let editables = document.querySelectorAll('.editable');
        contenteditable = 'true';

        editables.forEach((el, i) => {
            el.style.border = '';
            el.setAttribute('readonly','readonly');
        });

        document.querySelector('.btn--submit').style.display = '';
        document.querySelector('.btn--edit').style.display = '';
    }
    else {

        let editables = document.querySelectorAll('.editable');

        editables.forEach((el, i) => {
            el.style.border = '1px solid #aaa';
            el.removeAttribute('readonly');
        });

        document.querySelector('.btn--submit').style.display = 'block';
        document.querySelector('.btn--edit').style.display = 'none';
    }
}


function saveChanges(e) {
	e.preventDefault();
  toggleEditable();
}


document.querySelector('.btn--edit').addEventListener('click', toggleEditable);
document.querySelector('.btn--submit').addEventListener('click', saveChanges);

$(function() {
    $(".sortable").sortable({
      connectWith: ".sortable",
      handle: '.handle'
    }).disableSelection();
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
