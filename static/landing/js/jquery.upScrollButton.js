/**
 * код взят из блога Александра Шуйского http://shublog.ru/ajax/jquery/kak-sdelat-knopku-naverkh-kak-vkontakte/
 * код оформил EGORR
 * Date: 16.07.11
 */
$.fn.upScrollButton = function( options ) {
	var options = $.extend( {

		heightForButtonAppear : 100, // дистанция от верхнего края окна браузера, при превышении которой кнопка становится видимой
		heightForScrollUpTo : 0, // дистанция от верхнего края окна браузера к которой будет прокручена страница
		scrollTopTime : 900, // длительность прокрутки
		upScrollButtonId : 'move_up', // id кнопки
		upScrollButtonFadeInTime :0, // длительность эффекта появления кнопки
		upScrollButtonFadeOutTime :300,// длительность ффекта исчезновения кнопки	

	}, options );
	return this.each(function() {
	
		$('body').append( '<a id="' + options.upScrollButtonId + '" href="#"></a>' );
		$( window ).scroll( function () {
			if ( $( this ).scrollTop()  > options.heightForButtonAppear )
				$( 'a#' + options.upScrollButtonId  ).fadeIn(options.upScrollButtonFadeInTime );
			else
				$( 'a#' + options.upScrollButtonId ).fadeOut( options.upScrollButtonFadeOutTime );
		});
		$( 'a#' + options.upScrollButtonId ).click( function ( ) {
			$( 'body,html' ).animate( {
				scrollTop: options.heightForScrollUpTo
			}, options.scrollTopTime );
			return false;
		});
	});

}