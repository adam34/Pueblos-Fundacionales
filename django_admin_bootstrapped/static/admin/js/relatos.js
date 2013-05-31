//eventos.js con funciones para los forms de eventos

//Funciones para el modelo de eventos
$(function()
{
    //Codigo que registra el evento de keypress a los campos del form.
	var $elem=$('form');
	var id=$elem.attr('id');
	if(id=='relato_form')
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

    if($("#id_USUARIO").val()=="")
    {
        errores.push('Seleccione un usuario por favor.');
    }
    if($("#id_PUEBLO").val()=="")
    {
        errores.push('Seleccione un pueblo por favor.');
    }

    if($("input[name='TITULO']").val()=="")
    {
        errores.push('Es obligatorio introducir un título en el idioma original del sistema.');
    }
    if($("textarea[name='DESCRIPCION']").val()=="")
    {
        errores.push('Es obligatorio introducir una descripción en el idioma original del sistema.');
    }
    var date = new Date();
    cadenafecha= date.getDate()+"/"+date.getTwoDigitMonth()+"/"+date.getFullYear()+" "+date.getTwoDigitHour()+":"+date.getTwoDigitMinute()+":"+date.getTwoDigitSecond();
    $('#id_FECHA_P').val(cadenafecha);

    return errores;
}

//Fin de funciones para el modelo de Users