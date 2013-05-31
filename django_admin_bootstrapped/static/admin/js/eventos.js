//eventos.js con funciones para los forms de eventos

//Funciones para el modelo de eventos
$(function()
{
    //Codigo que registra el evento de keypress a los campos del form.
	var $elem=$('form');
	var id=$elem.attr('id');
	if(id=='evento_form')
	{
        $('input[name="_addanother"]').on('click',agregar);
        $('input[name="_continue"]').on('click',agregar);
        $('input[name="_save"]').on('click',agregar);
        $('#id_NOMBRE').on('keypress',validar_nombre_evento);
        function validar_nombre_evento(e)
        {
            //var patt=new RegExp("[A-Za-z0-9]+");
            var patt=/[A-Za-zñÑáéíóúÁÉÍÓÚ0-9 ]+/;
            var caracter = String.fromCharCode(e.charCode);
            if(!patt.test(caracter))
            {
                return false;
            }
        }
        $('#id_FECHA_0').on('focusout',validar_fecha);
        function validar_fecha(e)
        {
            //var patt=new RegExp("[A-Za-z0-9]+");
            $temp=$('#id_FECHA_0');
            var patt=/^(?:(?:0?[1-9]|1\d|2[0-8])(\/|-)(?:0?[1-9]|1[0-2]))(\/|-)(?:[1-9]\d\d\d|\d[1-9]\d\d|\d\d[1-9]\d|\d\d\d[1-9])$|^(?:(?:31(\/|-)(?:0?[13578]|1[02]))|(?:(?:29|30)(\/|-)(?:0?[1,3-9]|1[0-2])))(\/|-)(?:[1-9]\d\d\d|\d[1-9]\d\d|\d\d[1-9]\d|\d\d\d[1-9])$|^(29(\/|-)0?2)(\/|-)(?:(?:0[48]00|[13579][26]00|[2468][048]00)|(?:\d\d)?(?:0[48]|[2468][048]|[13579][26]))$ /;
            if(!patt.test($temp.val()))
            {
                alert('El formato de la fecha es incorrecto. El formato correcto es: dd/mm/yyyy');
            }
        }
        $('#id_FECHA_1').on('focusout',validar_hora);
        function validar_hora(e)
        {
            $temp=$('#id_FECHA_1');
            var patt=/^([0-1][0-9]|[2][0-3]):([0-5][0-9]):([0-5][0-9])$/;
            if(!patt.test($temp.val()))
            {
                alert('El formato de la hora es incorrecto. El formato correto es : hh:mm:ss a 24 hrs.');
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
function validar_formulario()
{
    //Se validan los campos de username, password, password2, nombre(s),apellido(s) y email
    //Se valida el username
    var errores = new Array();

    var patt= /^([A-Za-zñÑáéíóúÁÉÍÓÚ]{2,})+((\s{1})[A-Za-zñÑáéíóúÁÉÍÓÚ]{2,})*$/;
    if(!patt.test($("#id_NOMBRE").val()))
    {
        errores.push('El nombre sólo puede estar compuesto de letras y números separados por un espacio entre palabras.');
    }
    if($("#id_PUEBLO").val()=="")
    {
        errores.push('Seleccione un pueblo por favor.');
    }

    if($("input[name='LUGAR']").val()=="")
    {
        errores.push('Es obligatorio introducir un lugar en el idioma original del sistema.');
    }
    if($("textarea[name='DESCRIPCION']").val()=="")
    {
        errores.push('Es obligatorio introducir una descripción en el idioma original del sistema.');
    }
    $temp=$('#id_FECHA_0');
    var patt=/^(?:(?:0?[1-9]|1\d|2[0-8])(\/|-)(?:0?[1-9]|1[0-2]))(\/|-)(?:[1-9]\d\d\d|\d[1-9]\d\d|\d\d[1-9]\d|\d\d\d[1-9])$|^(?:(?:31(\/|-)(?:0?[13578]|1[02]))|(?:(?:29|30)(\/|-)(?:0?[1,3-9]|1[0-2])))(\/|-)(?:[1-9]\d\d\d|\d[1-9]\d\d|\d\d[1-9]\d|\d\d\d[1-9])$|^(29(\/|-)0?2)(\/|-)(?:(?:0[48]00|[13579][26]00|[2468][048]00)|(?:\d\d)?(?:0[48]|[2468][048]|[13579][26]))$ /;
    if(!patt.test($temp.val()))
    {
        errores.push('El formato de la fecha es incorrecto. El formato correcto es: dd/mm/yyyy.');
    }
    $temp=$('#id_FECHA_1');
    var patt=/^([0-1][0-9]|[2][0-3]):([0-5][0-9]):([0-5][0-9])$/;
    if(!patt.test($temp.val()))
    {
        alert('El formato de la hora es incorrecto. El formato correto es : hh:mm:ss a 24 hrs.');
    }

    if(errores.length==0)
    {
        if(map!=undefined)
        {
            cantidad = map.markers.length;
            if(cantidad!=0)
            {
                for(i=0;i<cantidad;i++)
                {
                    latitud= map.markers[i].position.lat();
                    longitud= map.markers[i].position.lng();
                    $('#id_LATITUD').val(latitud);
                    $('#id_LONGITUD').val(longitud);
                }
            }
        }
    }
    return errores;
}

//Fin de funciones para el modelo de Users