//idiomas.js con funciones para los forms de idiomas.

//Funciones para el modelo de idiomas

$(function()
{
    //Codigo que registra el evento de keypress a los campos del form.
	var $elem=$('form');
	var id=$elem.attr('id');
	if(id=='idioma_form')
	{
		$('#id_NOMBRE').on('keypress',validar_captura_nombre_idioma);
		function validar_captura_nombre_idioma(e)
		{
            $temp=$('#id_NOMBRE');
            if($temp.val().length>20)
            {
                return false;
            }
			//var patt=new RegExp("[A-Za-z0-9]+");
			var patt=new RegExp("[A-Za-zñÑáéíóúÁÉÍÓÚ]+");
			var caracter = String.fromCharCode(e.charCode);
			if(!patt.test(caracter))
			{
				//e.preventDefault();Metodo para evitar que se guarde el valor en el input
				//e.preventDefault() 
				//e.stopPropagation()
				return false;
			}
		}
    }
    else
    {
    alert('Error inesperado al tratar de asociar los eventos al formulario correcto. Contacte a su administrador para mayores informes.')
    }
});

function agregar(e,form,ruta)
{
    alert('Se ejecuto el agregar del idiomas.js');
    var arreglo = validar_nombre_idioma();
    if(arreglo.length!=0)
    {
        var str='<p>Ocurrieron los siguientes errores en el formulario:</p> \n';
        var x;
        for(x=0;x<arreglo.length;x++)
        {
            str+="<p>Error ["+x+"]: "+arreglo[x]+"<p>\n";

        }
        $('#cuerpo-modal').html(str);
        $('#titulo-modal').html('Errores en el formulario de usuarios.')
        $('#modal_sitio').modal('show',{
            keyboard: true
        });
        return false;
    }
}
function validar_nombre_idioma()
{
    var errores = new Array();
    var str = $('#id_NOMBRE').val();
    if(str.length<=0)
    {
        errores.push('El campo del nombre del idioma es obligatorio. Favor de llenarlo.');
    }

    if(str.length>20)
    {
        errores.push('El campo no puede ser mayor de 20 carácteres.');
    }

    var patt=new RegExp("^[A-Za-zñÑáéíóúÁÉÍÓÚ]+$");
    if(!patt.test(str))
    {
        errores.push("El idioma debe tener solamente letras, sin espacios y números y ningún otro tipo de dato.");
    }
    return errores;
}

//Fin de funciones para el modelo de idiomas