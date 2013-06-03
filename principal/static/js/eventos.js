$(window).on("load", function() {
    console.log("Funciona");
    $('#eventos').glDatePicker(
    {
        showAlways: true,
        cssName: 'default',
        specialDates: 
        [
            {
                date: new Date(2013, 0, 8),
                data: { message: 'Reunión de Pueblos Fundacionales' },
                repeatMonth: true
            },
            {
                date: new Date(2013, 0, 1),
                data: { message: 'Feliz Año Nuevo!' },
                repeatYear: false
            },
        ],
        onClick: function(target, cell, date, data) {
            target.val(date.getFullYear() + ' - ' +
            date.getMonth() + ' - ' +
            date.getDate());
            if(data != null) {
                $("p.noticias").empty();
                $("p.noticias").append("El evento es:" + '\n' + data.message);
            }
        }
    });
});