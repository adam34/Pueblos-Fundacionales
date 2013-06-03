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
			var patt=/[A-Za-z0-9]+/;
			var caracter = String.fromCharCode(e.charCode);
			if(!patt.test(caracter))
			{
				//e.preventDefault();Metodo para evitar que se guarde el valor en el input
				//e.preventDefault() 
				//e.stopPropagation()
				return false;
			}
		}
        $('#id_password').on('focusout',validar_contrasena);
        function validar_contrasena(e)
        {
            str=$('#id_password').val();
            if(str.length==0)
            {
                alert('La contraseña no puede quedar en blanco. Es obligatoria.')
            }
            return false;
        }
        $('#id_password2').on('focusout',validar_contrasenas);
        function validar_contrasenas(e)
        {
            $pass1=$('#id_password');
            $pass2=$('#id_password2');
            if($pass1.val()!=$pass2.val())
            {
                alert('Las contraseñas no son las mismas. Favor de verificarlo.')
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
            var patt=new RegExp("^[A-Za-z0-9.-_@]+$");
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
    var arreglo=validar_formulario();
    if(arreglo.length!=0)
    //if(true)
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
function validar_formulario()
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
    var patt=/^[A-Za-z0-9]+$/;
    if(!patt.test(str1))
    {
        errores.push('El nombre de usuario sólo puede contener letras y números, ningún otro tipo de caracter.');
    }

    //Se valida los 2 campos para la contraseña.
    str1 = $('#id_password').val();
    str2 = $('#id_password2').val();

    if(str1.length<6)
    {
        errores.push('La longitud de la contraseña debe ser mayor o igual a 6 caracteres.');
    }
    else
    {
        patt=/(?=.*\d)(?=.*[a-z])/;
        if(!patt.test(str1))
        {
            errores.push('La contraseña debe estar compuesta de números y letras, por seguridad.');
        }
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
        //patt=new RegExp("^([A-Za-zñÑáéíóúÁÉÍÓÚ]+)+(\s+[A-Za-zñÑáéíóúÁÉÍÓÚ]+)*$");
        patt= /^([A-Za-zñÑáéíóúÁÉÍÓÚ]{3,})+((\s{1})[A-Za-zñÑáéíóúÁÉÍÓÚ]{3,})*$/;
        if(!patt.test(str1))
        {
            errores.push('El campo de nombre(s) no tiene el formato correcto. Asegurese de introducir nombres compuestos sólo por letras, de 3 caracteres como mínimo, separados por un "sólo" espacio y de proporcionar tanto el/los nombre(s) como el/los apellido(s).');
        }
        if(!patt.test(str2))
        {
            errores.push('El campo de apellido(s) no tiene el formato correcto. Asegurese de introducir nombres compuestos sólo por letras y separados por un "sólo" espacio y de proporcionar tanto el/los nombre(s) como el/los apellido(s).');
        }
    }
    //Se valida el formato del email.
    str =$('#id_email').val()
    if(str!="")
    {
        var patt= /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        if(!patt.test(str))
        {
            errores.push('El formato del email es incorrecto. Favor de verificarlo.');
        }
    }     
    return errores;
}

//Fin de funciones para el modelo de Users