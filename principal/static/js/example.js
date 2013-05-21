$(document).ready(function(){

	var forcedaytime = 'night';
	var forcewcode = 389;
	var forcecurtemp = 40;
	var forcewindy = 'true';

	$('#weatherslider').weatherSlider({
		WWOAPIKey : '7ab69fab1f233943111612',
		imgPath : '/static/weatherslider/img/'
	});

	$('.ws-widget:eq(0)').weatherSlider({
		WWOAPIKey : '7ab69fab1f233943111612',
		imgPath : '/static/weatherslider/img/',		
		enableSearchField : false,
		responsive : false	
	});
	$('.ws-widget:eq(1)').weatherSlider({
		WWOAPIKey : '7ab69fab1f233943111612',
		imgPath : '/static/weatherslider/img/',		
		enableSearchField : false,
		enableForecast : false,
		refreshInterval : 20000,
		measurement : 'imperial',
		responsive : false
	});
	$('.ws-widget:eq(2)').weatherSlider({
		WWOAPIKey : '7ab69fab1f233943111612',
		imgPath : '/static/weatherslider/img/',		
		enableSearchField : false,
		slideDelay : 10000,
		timeFormat : 24,
		responsive : false		
	});
	$('.ws-widget:eq(3)').weatherSlider({
		WWOAPIKey : '7ab69fab1f233943111612',
		imgPath : '/static/weatherslider/img/',		
		enableSearchField : false,
		enableForecast : false,
		timeFormat : 24,
		measurement : 'imperial',
		showHum : false,
		showPrec : false,
		showWind : false,
		showPress : false,
		showVis : false,
		responsive : false		
	});
	customWeather();

	var isOldIE = $.browser.msie && $.browser.version < 9 ? true : false;

	$('.ws-ex').live('click',function(e){
		e.preventDefault();

		if(!$(this).parent().hasClass('ws-active')){

			if( !isOldIE ){
				var a = $('.examples li.ws-active').index();
				for(var x=0;x<$('.ws-example').length;x++){
					if( x != a ){
						$('.ws-ex-inner:eq('+x+')').css({
							visibility : 'hidden',
							opacity : 0
						});
					}
				}
				var w = $('#ws-examples').width();
				var l = parseInt($('#ws-examples .inner').css('left'));

				var fadeOut =  ( ( w - l ) / w ) - 1;
				var fadeIn =  Math.abs(parseInt($(this).attr('href')));

				$('#ws-examples .inner .ws-example:eq('+fadeOut+') .ws-ex-inner').fadeTo(500, 0, 'easeInQuad', function(){
					$(this).css({
						visibility : 'hidden'
					});
				});

				$('#ws-examples .inner .ws-example:eq('+fadeIn+') .ws-ex-inner').css({
					visibility : 'visible'
				}).delay(750).fadeTo(500, 1, 'easeInQuad');				
			}

			$('li').removeClass('ws-active');
			$(this).parent().addClass('ws-active');

			$('#ws-examples .inner').stop().animate({
				left : ( parseInt( $(this).attr('href') ) * $('#ws-examples').width() ) + 'px'
			}, 1500, 'easeInOutQuart');						
		}
	});

	$('input[name="forcedaytime"]').click(function(){
		forcedaytime = $(this).attr('value');		
		customWeather();
	});
	$('input[name="forcewcode"]').click(function(){
		forcewcode = $(this).attr('value');		
		customWeather();
	});
	$('input[name="forcecurtemp"]').click(function(){
		forcecurtemp = $(this).attr('value');		
		customWeather();
	});
	$('input[name="forcewindy"]').click(function(){
		forcewindy = $(this).attr('value');		
		customWeather();
	});

	function customWeather(){

		$('#ws-weathers *').stop().remove();

		$('#ws-weathers').weatherSlider({
			WWOAPIKey : '7ab69fab1f233943111612',
			imgPath : '/static/weatherslider/img/',		
			enableSearchField : false,
			enableWeatherInfo : false,
			locations : ['Loreto, Baja California Sur'],
			forcedaytime : forcedaytime,
			forcewcode : forcewcode,
			forcecurtemp : forcecurtemp,
			forcewindy : forcewindy == 'true' ? true : false
		});
	}
});