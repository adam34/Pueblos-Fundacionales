//pueblos.js con funciones para los forms de pueblos

//Funciones para el modelo de idiomas
$(function()
{
    //Codigo que registra el evento de keypress a los campos del form.
	var $elem=$('form');
	var id=$elem.attr('id');
	if(id=='pueblo_form')
	{
		$('#id_NOMBRE').on('keypress',validar_nombre_pueblo);
        $('input[name="_addanother"]').on('click',agregar);
        $('input[name="_continue"]').on('click',agregar);
        $('input[name="_save"]').on('click',agregar);
		function validar_nombre_pueblo(e)
		{
            $temp=$(e.target);
            texto= $temp.val();
			//var patt=new RegExp("[A-Za-z0-9]+");
			var patt=/[A-Za-zñÑáéíóúÁÉÍÓÚ ]+/;
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
    tinymce.init({
        selector: "textarea",
        theme: "modern",
        width: 700,
        height: 300,
        plugins: [
             "advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker",
             "searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking",
             "save table contextmenu directionality emoticons template paste textcolor"
       ],
       toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | print preview media fullpage | forecolor backcolor emoticons", 
     });
    $editors =$(tinymce.editors);
    $editors.each(function(index,value){
        $control=$(value.getElement())
        contenido = $control.val();
        if(contenido!="")
        {
            value.setContent(contenido);
            $control.val('')
        }
    });

});
//Metodo utilizado para controlar el guardado de los datos con el servidor por Ajax.
function agregar(e,form,ruta)
{
    var arreglo=validar_formulario_grupo();
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
function validar_formulario_grupo()
{
    //Se validan los campos de username, password, password2, nombre(s),apellido(s) y email
    //Se valida el username
    var errores = new Array();
    str1=$('#id_NOMBRE').val();
    if(str1.length>30)
    {
        errores.push('La longitud del nombre de usuario no puede ser mayor a 30 caracteres.');
    }
    if(str1.length<4)
    {
        errores.push('La longitud del nombre de usuario no puede ser menor de 4 caracteres.');
    }
    if($("#id_TIPO").val()=="")
    {
        errores.push('Seleccione un tipo de pueblo, por favor.');   
    }
    if($("#id_ADMINISTRADOR").val()=="")
    {
        errores.push('Seleccione a un usuario para que sea el administrador del pueblo.');
    }
    if($('div#Español textarea').val()=="")
    {
        errores.push('Es necesaria una descripción del pueblo en el idioma original (Español).');
    }
    if(errores.length==0)
    {
        $editors =$(tinymce.editors);
        $editors.each(function(index,value)
        {
            contenido = value.getContent();
            if(contenido!="")
            {
                $control=$(value.getElement())
                $control.val(contenido);

            }
        });
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