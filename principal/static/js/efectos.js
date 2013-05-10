function mostrarPueblos(){
	var pueblos, url;
	$("#purisima").on("click", quePueblos);
	$("#loreto").on("click", quePueblos);
}

function quePueblos(enlace){
	enlace.preventDefault();
	pueblos = $(this).attr("id");
	url = pueblos;
	$(".contenedor_tabs").slideUp(2000, function(){
		$(this).load(url);
	}).slideDown(2000);
}