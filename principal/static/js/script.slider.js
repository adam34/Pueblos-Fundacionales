$(document).on("ready", inicio);
    function inicio(){
        $('#arrow').on("click", transicion);
        $("#arrow").css({
             "transform": "rotate (180 deg)"
        });
        var subMenu = $("#page-wrap ul li ul li");
    	var linkClick = $("#page-wrap ul li").filter(":has(ul)");
        subMenu.hide();
        linkClick.click(function () {
        	$(this).find('ul li').slideToggle("fast, 100");
    	});
        $('#carousel').elastislide({
            minItems : 2  
        });
        $(".cosas").on("click", function(){
            $(".contenido_secciones_pueblos").load("/templates/cosas.html");
        });
        
    }
    function transicion() {
        $('.eng').toggle();    
    }
