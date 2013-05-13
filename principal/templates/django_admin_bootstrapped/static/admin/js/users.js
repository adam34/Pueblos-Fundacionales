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
        $('#id_first_name').on('keypress',validar_nombres);
        function validar_nombres(e)
        {
            var patt=new RegExp("^[A-Za-zñÑáéíóúÁÉÍÓÚ ]+$");
            //var patt=new RegExp("^([A-Za-zñÑáéíóúÁÉÍÓÚ]+)+(\s+[A-Za-zñÑáéíóúÁÉÍÓÚ]+)?$");
            var caracter = String.fromCharCode(e.charCode);
            //var cad=$('#id_first_name').val();
            //cad+=caracter;
            if(!patt.test(caracter))
            {
                return false;
            }
            
        }
        $('#id_last_name').on('keypress',validar_apellidos);
        function validar_apellidos(e)
        {
            var patt=new RegExp("^[A-Za-zñÑáéíóúÁÉÍÓÚ ]+$");
            var caracter = String.fromCharCode(e.charCode);
            if(!patt.test(caracter))
            {
                return false;
            }
            
        }
        $('#id_email').on('keypress',validar_email);
        function validar_email(e)
        {
            var patt=new RegExp("^[A-Za-z0-9.-_@#$%&/()=]+$");
            var caracter = String.fromCharCode(e.charCode);
            if(!patt.test(caracter))
            {
                return false;
            } 
        }
	}
    else
    {
        alert('Error inesperado al tratar de asociar los eventos al formulario correcto. Contacte a su administrador para mayores informes.')
    }
});
//Metodo utilizado para controlar el guardado de los datos con el servidor por Ajax.
function agregar(e,form,ruta)
{
    debugger;
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
            //NO OLVIDAR QUITAR ESTE RETURN FALSE DESPUES.
            return false;
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
    }
}
function validar_formulario_usuario()
{
    //Se validan los campos de username, password, password2, nombre(s),apellido(s) y email
    //Se valida el username
    var errores = new Array();
    str1=$('#id_username').val();
    if(str1.length>30)
    {
        errores.push('La longitud del nombre de usuario no puede ser mayor a 30 caracteres.');
    }
    if(str1.length<6)
    {
        errores.push('La longitud del nombre de usuario no puede ser menor de 6 caracteres.');
    }
    //var patt=new RegExp("[A-Za-z0-9]+");
    var patt=new RegExp("[A-Za-zñÑáéíóúÁÉÍÓÚ]+");
    if(!patt.test(str1))
    {
        errores.push('El nombre de usuario sólo puede contener letras, ningún otro tipo de caracter.');
    }

    //Se valida los 2 campos para la contraseña.
    str1 = $('#id_password').val();
    str2 = $('#id_password2').val();

    if(str1.length<6)
    {
        errores.push('La longitud de la contraseña debe ser mayor o igual a 6 caracteres.');
    }

    if(str1.length!=str2.length)
    {
        errores.push('Las contraseñas no coinciden.');
    }

    //Se validan tanto los nombres como los apellidos
    str1 = $('#id_first_name').val()
    str2 =$('#id_last_name').val()
    if(str1!="" || str2!="")
    {
        var patt=new RegExp("^([A-Za-zñÑáéíóúÁÉÍÓÚ]{3,})+(\s+[A-Za-zñÑáéíóúÁÉÍÓÚ]{3,})*$");
        if(!patt.test(str1))
        {
            errores.push('El campo de nombre(s) no tiene el formato correcto. Asegurese de introducir nombres compuestos sólo por letras y separados por un espacio y de proporcionar tanto el/los nombre(s) como el/los apellido(s).');
        }
        if(!patt.test(str2))
        {
            errores.push('El campo de apellido(s) no tiene el formato correcto. Asegurese de introducir nombres compuestos sólo por letras y separados por un espacio y de proporcionar tanto el/los nombre(s) como el/los apellido(s).');
        }
    }
    //Se valida el formato del email.
    str =$('#id_email').val()
    if(str!="")
    {
        var patt=new RegExp('^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$');
        if(!patt.test(str))
        {
            errores.push('El formato del email es incorrecto. Favor de verificarlo.');
        }
    }     
    return errores;
}

//Fin de funciones para el modelo de Users