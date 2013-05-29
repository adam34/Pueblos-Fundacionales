//Grupos.js con funciones para los forms de users.

//Funciones para el modelo de idiomas
$(function()
{
    //Codigo que registra el evento de keypress a los campos del form.
	var $elem=$('form');
	var id=$elem.attr('id');
	if(id=='pueblo_form')
	{
		$('#id_NOMBRE').on('keypress',validar_nombre_pueblo);
        $('input[name="_addanother"]').on('click',agregar);
        $('input[name="_continue"]').on('click',agregar);
        $('input[name="_save"]').on('click',agregar);
		function validar_nombre_pueblo(e)
		{
            $temp=$('#id_name');
            if($temp.val().length>30)
            {
                return false;
            }
			//var patt=new RegExp("[A-Za-z0-9]+");
			var patt=/[A-Za-zñÑáéíóúÁÉÍÓÚ ]+/;
			var caracter = String.fromCharCode(e.charCode);
			if(!patt.test(caracter))
			{
				//e.preventDefault();Metodo para evitar que se guarde el valor en el input
				//e.preventDefault() 
				//e.stopPropagation()
				return false;
			}
		}
        $('.field-DESCRIPCION .controls .tab-pane').each(function(index,value)
            {
                $valor = $(value);
                id = $valor.attr('id')
                $textbox = $algo.find('textarea');
                $textbox.on('keypress',validar_idiomas)
                function validar_idiomas(e)
                {
                    var patt=/[\wñÑáéíóúÁÉÍÓÚ ]+/;
                    caracter = String.fromCharCode(e.charCode);
                    if(!patt.test(caracter))
                    {
                        //e.preventDefault();Metodo para evitar que se guarde el valor en el input
                        //e.preventDefault() 
                        //e.stopPropagation()
                        return false;
                    }
                }
            }
        });
	}
    else
    {
        alert('Error inesperado al tratar de asociar los eventos al formulario correcto. Contacte a su administrador para mayores informes.')
    }
});
//Metodo utilizado para controlar el guardado de los datos con el servidor por Ajax.
function agregar(e,form,ruta)
{
    var arreglo=validar_formulario_grupo();
    if(arreglo.length!=0)
    //if(false)
    {
        var str='<p>Ocurrieron los siguientes errores en el formulario:</p> \n';
        var x;
        for(x=0;x<arreglo.length;x++)
        {
            str+="<p>error ["+x+"]: "+arreglo[x]+"<p>\n";

        }
        $('#cuerpo-modal').html(str);
        $('#titulo-modal').html('Errores en el formulario de usuarios.')
        $('#modal_sitio').modal('show',{
            keyboard: true
        });
        return false;
    }

}
function validar_formulario_grupo()
{
    //Se validan los campos de username, password, password2, nombre(s),apellido(s) y email
    //Se valida el username
    var errores = new Array();
    str1=$('#id_name').val();
    if(str1.length>30)
    {
        errores.push('La longitud del nombre de usuario no puede ser mayor a 30 caracteres.');
    }
    if(str1.length<4)
    {
        errores.push('La longitud del nombre de usuario no puede ser menor de 4 caracteres.');
    }
    if($("#id_TIPO").value()=="")
    {
        errores.push('Seleccione un tipo de pueblo, por favor.');   
    }
    if($('div#Español textarea').val()=="")
    {
        errores.push('Es necesaria una descripción del pueblo en el idioma original (Español).');
    }
    $('.field-DESCRIPCION .controls .tab-pane').each(function(index,value)
        {
            $valor = $(value);
            id = $valor.attr('id')
            texto = $algo.find('textarea').val();

            if(texto!="")
            {
                var patt=/[\wñÑáéíóúÁÉÍÓÚ ]+/;
                if(!patt.test(texto))
                {
                    //e.preventDefault();Metodo para evitar que se guarde el valor en el input
                    //e.preventDefault() 
                    //e.stopPropagation()
                    errores.push('Sólo se aceptan los caracteres de la A a la Z (mayúscula y minúscula), del 0 al 9 y _ ('+id+').');
                }
            }
        }
    });
    return errores;
}

//Fin de funciones para el modelo de Users