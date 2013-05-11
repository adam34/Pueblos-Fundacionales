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
    if(arreglo.length==0)
    {
        a=10;
        form=$(form);
        var datos="";
        if(e.target.name=='_addanother')
        {
            datos="&_addanother=submit"
        }
        else if(e.target.name=='_continue')
        {
            datos="&_continue=submit"
        }
        else if(e.target.name=='_save')
        {
            datos="&_save=submit"
        }
        else
        {
            alert('Ocurrió un error inesperado al momento de guardar/modificar/guardar y continuar el registro. Contacte al administrador.')
            return false;
        }
        if(ruta!='')
        {
            $.ajax({
                async:false,
                url:ruta,
                data:form.serialize()+datos,
                type:'POST',
                //dataType:
                success:function(response)
                {
                    if(response!='')
                    {
                        $('#content-main').hide(500,function()
                            {
                                $('#content-main').html(response);
                                $('#content-main').show(1000);
                            });
                    }
                    else
                    {
                        alert('No hubo respuesta por parte del servidor.');
                    }
                },
                error:function(jqXHR, status, error)
                {
                    alert(jqXHR.responseText+'\n'+status+'\n'+ error);
                },
                // complete:function(jqXHR, status)
                // {
                //     alert(jqXHR.responseText+'\n'+status)
                // },
            });
        }
        else
        {
            alert('Error inesperado al tratar de cargar el modulo deseado. Consulte a su administrador.');
        }
    }
    else
    {
        var str='Ocurrieron los siguientes errores en el formulario: \n';
        var x;
        for(x=0;x<arreglo.length;x++)
        {
            str+="error ["+x+"]: "+arreglo[x]+"\n";

        }
        alert(str);
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

    var patt=new RegExp("[A-Za-zñÑáéíóúÁÉÍÓÚ]+");
    if(!patt.test(str))
    {
        errores.push("El idioma debe tener solamente letras, sin espacios y números y ningún otro tipo de dato.");
    }
    return errores;
}

//Fin de funciones para el modelo de idiomas