//users.js con funciones para los forms de users.

//Funciones para el modelo de idiomas
$(function()
{
    //Codigo que registra el evento de keypress a los campos del form.
	var $elem=$('form');
	var id=$elem.attr('id');
	if(id=='user_form')
	{
		$('#id_username').on('keypress',validar_nombre_usuario);
		function validar_nombre_usuario(e)
		{
            $temp=$('#id_username');
            if($temp.val().length>30)
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
        $('#id_password2').on('focusout',validar_contrasenas);
        function validar_contrasenas(e)
        {
            $pass1=$('#id_password');
            $pass2=$('#id_password2');
            if($pass1.val()!=$pass2.val())
            {
                alert('Las contraseñas no son las mismas. Favor de verificarlo')
                $pass1.focus();
            }
            return false;
        }
	}
    else
    {
        alert('Error inesperado al tratar de asociar los eventos al formulario correcto. Contacte a su administrador para mayores informes.')
    }
});
function agregar(e,form,ruta)
{
    alert('Se ejecutó el agregar del users.js');
    var arreglo=validar_formulario_usuario();
    if(arreglo.length==0)
    {
        forma=$(form);
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
                data:forma.serialize()+datos,
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
function validar_formulario_usuario()
{
    var errores = new Array();
    $temp=$('#id_username');
    if($temp.val().length>30)
    {
        errores.push('La longitud del nombre de usuario no puede ser mayor a 30 caracteres');
    }
    //var patt=new RegExp("[A-Za-z0-9]+");
    var patt=new RegExp("[A-Za-zñÑáéíóúÁÉÍÓÚ]+");
    var str = $temp.val();
    if(!patt.test(str))
    {
        errores.push('El nombre de usuario sólo puede contener letras, ningún otro tipo de caracter.');
    }
    $pass1=$('#id_password');
    $pass2=$('#id_password2');
    if($pass1.val()!=$pass2.val())
    {
        errores.push('Las contraseñas no coinciden.');
    }
    return errores;
}
//Fin de funciones para el modelo de idiomas