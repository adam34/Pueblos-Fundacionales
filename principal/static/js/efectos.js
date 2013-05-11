function mostrarPueblos(){
	var pueblos, url, libros;
	$("#purisima").on("click", quePueblos);
	$("#loreto").on("click", quePueblos);
	//Librería
	$("#libro_purisima").on("click", libreria);
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