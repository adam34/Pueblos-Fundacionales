//Grupos.js con funciones para los forms de users.

//Funciones para el modelo de idiomas
$(function()
{
    //Codigo que registra el evento de keypress a los campos del form.
	var $elem=$('form');
	var id=$elem.attr('id');
	if(id=='group_form')
	{
		$('#id_name').on('keypress',validar_nombre_grupo);
        $('input[name="_addanother"]').on('click',agregar);
        $('input[name="_continue"]').on('click',agregar);
        $('input[name="_save"]').on('click',agregar);
		function validar_nombre_grupo(e)
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
    //if(arreglo.length!=0)
    if(false)
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
    $permisos = $('#selection-permissions .selection-elem');
    $('#selection-permissions').blur();
    if($permisos.length>0)
    {
        $permisos.each(function(index,value){
            $valor = $(value);
            $valor.attr('selected','true');
            $valor.off('click');
            $valor.off('mouseover');
        });
    }

    return errores;
}

//Fin de funciones para el modelo de Users