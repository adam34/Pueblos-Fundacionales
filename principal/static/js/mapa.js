$(function() {
	var loreto = new google.maps.LatLng(26.013132,-111.347895),
		pointToMoveTo, 
       	first = true,
       	curMarker = new google.maps.Marker({}),
       	$el;
    var myOptions = {
      	zoom: 10,
       	center: loreto,
       	mapTypeId: google.maps.MapTypeId.ROADMAP
   	};
    //Modificación - Localizaciones 
   	var map = new google.maps.Map($("#map_canvas")[0], myOptions);
   	$("#locations li").mouseenter(function() {
   		$el = $(this);
   		if (!$el.hasClass("hover")) {
            $("#locations li").removeClass("hover");
          	$el.addClass("hover");
          	if (!first) { 
            	// Clear current marker
            	curMarker.setMap(); 
            	// Set zoom back to Chicago level
            	map.setZoom(14);
            }
          		// Move (pan) map to new location
          		pointToMoveTo = new google.maps.LatLng($el.attr("data-geo-lat"), $el.attr("data-geo-long"));
          		map.panTo(pointToMoveTo);
          		// Add new marker
          		curMarker = new google.maps.Marker({
            	position: pointToMoveTo,
            	map: map,
            	icon: "/static/img/marker.png"
          	});
          		// On click, zoom map
          		google.maps.event.addListener(curMarker, 'click', function() {
            	map.setZoom(50);
        });
          // Fill more info area
        $("#more-info").find("h2").html($el.find("h3").html()).end().find("p").html($el.find(".longdesc").html());
          // No longer the first time through (re: marker clearing)        
          first = false; 
        }
        
      });
      
      $("#locations li:first").trigger("mouseenter");
});