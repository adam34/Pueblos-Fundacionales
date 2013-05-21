function mostrarPueblos(){
	var pueblos, url, libros, video;
	$("#purisima").on("click", quePueblos);
	$("#loreto").on("click", quePueblos);
	//Librería
	$("#libro_purisima").on("click", libreria);
	$("#libro_loreto").on("click", libreria);
	$("#player").on("click", contenido_multimedia);
	$("#galeria").on("click", contenido_multimedia);
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