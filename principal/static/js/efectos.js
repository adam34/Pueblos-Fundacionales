function mostrarPueblos(){
	var pueblos, url, libros, video, base;
	$("#purisima").on("click", quePueblos);
	$("#loreto").on("click", quePueblos);
	//Librería
	$("#libro_purisima").on("click", libreria);
	$("#libro_loreto").on("click", libreria);
	$("#player").on("click", contenido_multimedia);
	$("#galeria").on("click", contenido_multimedia);
	//Información básica
	$("#cosas").on("click", contenidoBasico)
	$("#exp").on("click", expresiones)
	$("#fra").on("click", frases)
	$("#proy").on("click", proyecto)

}

function quePueblos(enlace){
	enlace.preventDefault();
	pueblos = $(this).attr("id");
	url = pueblos;
	$(".contenedor_tabs").load(url);
}
function libreria(enlace){
	enlace.preventDefault();
	libros = $(this).attr("id");
	url = libros;
	console.log(url);
	$(".pueblos").load(url);
}

function contenido_multimedia(enlace){
	enlace.preventDefault();
	video = $(this).attr("id");
	console.log(video);
	$(".contenido_multimedia").load(video);
}

function contenidoBasico(enlace){
	enlace.preventDefault();
	base =$(this).attr("id");
	$("#cosasqds").toggle('slow');
}

function expresiones(enlace){
	enlace.preventDefault();
	base =$(this).attr("id");
	$("#expresiones").toggle('slow');
}

function frases(enlace){
	enlace.preventDefault();
	base =$(this).attr("id");
	$("#frases").toggle('slow');
}

function proyecto(enlace){
	enlace.preventDefault();
	base =$(this).attr("id");
	$("#proy_b").toggle('slow');
}