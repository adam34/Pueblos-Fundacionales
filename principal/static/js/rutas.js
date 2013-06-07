  var map;
  var route;
$(document).on("ready", function(){
    //prettyPrint();
    $('#forward').attr('disabled', 'disabled');
    $('#back').attr('disabled', 'disabled');
    $('#get_route').click(function(e){
      e.preventDefault();

        origin = map.markers[0].getPosition();
        destination = map.markers[map.markers.length-1].getPosition();

        map.getRoutes({
          origin: [origin.lat(), origin.lng()],
          destination: [destination.lat(), destination.lng()],
          travelMode: 'driving',
          callback: function(e){
            route = new GMaps.Route({
              map: map,
              route: e[0],
              strokeColor: '#336699',
              strokeOpacity: 0.5,
              strokeWeight: 10
            });
            $('#forward').removeAttr('disabled');
            $('#back').removeAttr('disabled');
          }
        });
         //Hotel 
    map.addMarker({
      lat:  24.1586,
        lng: -110.3198,
        title: 'Hotel Los Arcos',
      icon: '/static/img/iconos/hotel_5stars.png',
    });
    //La Purísima
    map.addMarker({
      lat:  26.185556,  
      lng: -112.075278,
      title: 'Misión de La Purísima',
      icon: '/static/img/iconos/misiones3.png',
      click: function(e) {
          alert('Aquí vive el profe Pedro y la maestra Quitty :D');
        }
    });
    //Mi casa xD 
    /*map.addMarker({
      lat: 24.13570,
      lng: -110.33032,
      title: 'Mi casa',
      click: function(e) {
          alert('Esta es mi casa.');
      }
    });*/
    //Sierra de San Francisco
    map.addMarker({
      lat: 27.597500,
        lng: -113.015833,
        title: 'Sierra de San Francisco',
      icon: '/static/img/iconos/misiones3.png',
    });
    //Loreto
    map.addMarker({
      lat:  26.0137, 
      lng: -111.3478,
      title: 'Loreto',
      icon: '/static/img/iconos/misiones3.png',
    });
     //Puerto Adolfo López Mateos
    map.addMarker({
      lat: 25.193889,
      lng: -112.112500,
      title: 'Puerto Adolfo López Mateos',
      icon: '/static/img/iconos/misiones3.png',
    });
    //San Miguel de Comondú
    map.addMarker({
      lat: 26.036667,
      lng: -111.834444,
      title: 'San Miguel de Comondú',
      icon: '/static/img/iconos/misiones3.png',
    });
    //San José de Comondú
    map.addMarker({
      lat: 26.059444,
      lng: -111.825278,
      title: 'San José de Comondú',
      icon: '/static/img/iconos/misiones3.png',
    });
    //San Javier
    map.addMarker({
      lat: 25.861389,
      lng: -111.543611,
      title: 'San Javier',
      icon: '/static/img/iconos/misiones3.png',
    });
    //San Isidro
    map.addMarker({
      lat: 26.2047, 
      lng: -112.0398,
      title: 'San Isidro',
      icon: '/static/img/iconos/misiones3.png',
    });
    //Ensenada Blanca
    map.addMarker({
      lat:  25.6912, 
      lng: -111.4552,
      title: 'Ensenada Blanca',
      icon: '/static/img/iconos/misiones3.png',
    });
    //Puerto Escondido
    map.addMarker({
      lat:  25.81, 
      lng: -111.3092,
      title: 'Puerto Escondido',
      icon: '/static/img/iconos/misiones3.png',
    });
     //Nopoló, Loreto
    map.addMarker({
      lat:  25.936111, 
      lng: -111.361111,
      title: 'Nopoló',
      icon: '/static/img/iconos/misiones3.png',
    });
    //San Juan Londó
    map.addMarker({
      lat:  26.224722, 
      lng: -111.475000,
      title: 'San Juan Londó',
      icon: '/static/img/iconos/misiones3.png',
    });
    //Puerto San Carlos
    map.addMarker({
      lat:  24.7934, 
      lng: -112.1057,
      title: 'Puerto San Carlos',
      icon: '/static/img/iconos/misiones3.png',
    });
    //San Nicolás
    map.addMarker({
      lat:  26.5347, 
      lng: -111.5467,
      title: 'San Nicolás',
      icon: '/static/img/iconos/misiones3.png',
    });
    //Mulegé
    map.addMarker({
      lat:  26.900946, 
      lng: -111.982269,
      title: 'Mulegé',
      icon: '/static/img/iconos/misiones3.png',
    });
    //Punta Chivato
    map.addMarker({
      lat:  27.070278, 
      lng: -111.968056,
      title: 'Punta Chivato',
      icon: '/static/img/iconos/misiones3.png',
    });
    //Laguna de San Ignacio
    map.addMarker({
      lat:  26.971038,
      lng: -113.233337,
      title: 'Laguna de San Ignacio',
      icon: '/static/img/iconos/misiones3.png',
    });
    //San Ignacio
    map.addMarker({
      lat:  26.669857,
      lng: -111.700745,
      title: 'San Ignacio',
      icon: '/static/img/iconos/misiones3.png',
    });
        $('#forward').click(function(e){
          e.preventDefault();
          route.forward();

          if(route.step_count < route.steps_length)
            $('#steps').append('<li>'+route.steps[route.step_count].instructions+'</li>');
        });
        $('#back').click(function(e){
          e.preventDefault();
          route.back();

          if(route.step_count >= 0)
            $('#steps').find('li').last().remove();
        });
      });
      map = new GMaps({
        div: '#map',
        lat:  26.185556,  
        lng: -112.075278,
        zoom: 8,
       // zoom: 16,
        click: function(e){
          map.addMarker({
            lat: e.latLng.lat(),
            lng: e.latLng.lng()
       });
      }
   });
     $('#geocoding_form').submit(function(e){
      e.preventDefault();
      GMaps.geocode({
        address: $('#address').val().trim(),
        callback: function(results, status){
          if(status=='OK'){
                    var latlng = results[0].geometry.location;
                    map.setCenter(latlng.lat(), latlng.lng());
                    map.addMarker({
                      lat: latlng.lat(),
                      lng: latlng.lng()
              });
            }
         }
      });
    });
    GMaps.geolocate({
      success: function(position) {
      map.setCenter(position.coords.latitude, position.coords.longitude);
      },
      error: function(error) {
      alert('Geolocation failed: '+error.message);
      },
      not_supported: function() {
      alert("Your browser does not support geolocation");
      },
  });
   
   
});