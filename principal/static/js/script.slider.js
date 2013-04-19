$(document).on("ready", inicio);
    function inicio(){
        $('#arrow').on("click", transicion);
        $("#arrow").css({
             "transform": "rotate (180 deg)"
        });
    }

    function transicion() {
        $('.eng').toggle();    
    }