//contratos.js con funciones para los forms de eventos

//Funciones para el modelo de contratos
$(function()
{
    //Codigo que registra el evento de keypress a los campos del form.
	var $elem=$('form');
	var id=$elem.attr('id');
	if(id=='archivo_form')
	{
        $('input[name="_addanother"]').on('click',agregar);
        $('input[name="_continue"]').on('click',agregar);
        $('input[name="_save"]').on('click',agregar);
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
    valor=$('#id_RUTA').val();
    if(valor=="")
    {
        if($('.field-RUTA a').length==0)
        {
            errores.push('Seleccione un archivo, por favor.');
        }
    }
    if(errores.length==0)
    {
        $ruta = $($('#id_RUTA'))
        if($ruta.val()!="")
        {
            partes = $ruta.val().split("\\");
            archivo = partes[partes.length-1];
            if(archivo.length >50)
            {
                alert('El nombre del archivo no puede ser mayor a 50 caracteres, eso incluye la extensión.');
            }
            else
            {
                $('#id_NOMBRE').val(archivo);
            }
            
        }
    }

    return errores;
}

//Fin de funciones para el modelo de Users