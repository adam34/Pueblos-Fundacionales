//categorias.js con funciones para los forms de eventos

//Funciones para el modelo de contratos
$(function()
{
    //Codigo que registra el evento de keypress a los campos del form.
	var $elem=$('form');
	var id=$elem.attr('id');
	if(id=='categoria_form')
	{
        $('input[name="_addanother"]').on('click',agregar);
        $('input[name="_continue"]').on('click',agregar);
        $('input[name="_save"]').on('click',agregar);
        $('#id_NOMBRE').on('keypress',validar_nombre_pueblo);
        function validar_nombre_pueblo(e)
        {
            $temp=$(e.target);
            texto= $temp.val();
            //var patt=new RegExp("[A-Za-z0-9]+");
            var patt=/[A-Za-zñÑáéíóúÁÉÍÓÚ0-9 ]+/;
            var caracter = String.fromCharCode(e.charCode);
            if(!patt.test(caracter))
            {
                return false;
            }
            texto=texto+caracter;
            if(texto.length>30)
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
    if(valor.length<4)
    {
        errores.push('El tamaño del nombre no puede ser menor de 4 caracteres.');
    }
    if(valor.length>30)
    {
        errores.push('El tamaño del nombre no puede ser mayor de 30 caracteres.');
    }
    patt= /^([A-Za-zñÑáéíóúÁÉÍÓÚ]{3,})+((\s{1})[A-Za-zñÑáéíóúÁÉÍÓÚ]{3,})*$/;
    if(!patt.test(valor))
    {
        errores.push('El campo de nombre(s) no tiene el formato correcto. Asegurese de introducir nombres compuestos sólo por letras, de 3 caracteres como mínimo, separados por un "sólo" espacio y de proporcionar tanto el/los nombre(s) como el/los apellido(s).');
    }
    return errores;
}

//Fin de funciones para el modelo de Users