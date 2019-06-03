$(function(){

	var resizeTimer;

	$(window).on('resize', function(e) {

		/* resizing */
		$('.js-resize').css({'opacity': '0'});

		clearTimeout(resizeTimer);
		resizeTimer = setTimeout(function() {

			/* done */
			$('.js-resize').css({'opacity': '1'});

		}, 250);

	});

});