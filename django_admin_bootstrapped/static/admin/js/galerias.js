//contratos.js con funciones para los forms de eventos

//Funciones para el modelo de contratos
$(function()
{
    //Codigo que registra el evento de keypress a los campos del form.
	var $elem=$('form');
	var id=$elem.attr('id');
	if(id=='galeria_form')
	{
        $('input[name="_addanother"]').on('click',agregar);
        $('input[name="_continue"]').on('click',agregar);
        $('input[name="_save"]').on('click',agregar);
        $('#id_NOMBRE').on('keypress',validar_captura_nombre_galeria);
        function validar_captura_nombre_galeria(e)
        {
            $temp=$('#id_NOMBRE');
            if($temp.val().length>40)
            {
                return false;
            }
            //var patt=new RegExp("[A-Za-z0-9]+");
            var patt=new RegExp("[A-Za-zñÑáéíóúÁÉÍÓÚ0-9 ]+");
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
    var arreglo=validar_formulario();
    if(arreglo.length!=0)
    //if(false)
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

    valor=$('#id_NOMBRE').val();
    if(valor=="" || valor.length>40)
    {
        errores.push('Introduzca un nombre para la galería no mayor de 40 caracteres, por favor.')
    }
    patt= /^([A-Za-zñÑáéíóúÁÉÍÓÚ0-9]{3,})+((\s{1})[A-Za-zñÑáéíóúÁÉÍÓÚ0-9]{3,})*$/;
    if(!patt.test(valor))
    {
        errores.push('El nombre tiene un formato incorrecto. Sólo se aceptan palabras de más de 3 caracteres y de letras y números.');
    }
    if(errores.length==0)
    {
        $permisos = $('#selection-ARCHIVOS .selection-elem');
        $('#selection-ARCHIVOS').blur();
        if($permisos.length>0)
        {
            $permisos.each(function(index,value){
                $valor = $(value);
                $valor.attr('selected','true');
                $valor.off('click');
                $valor.off('mouseover');
            });
        }
    }

    return errores;
}

//Fin de funciones para el modelo de Users