$(document).ready(function() {

	// Оформление меню
	$('.menu-main td a, .menu-secondary td a, .menu-service1 td a, .menu-service2 td a, .menu-service3 td a, .menu-links1 td a, .menu-links2 td a').append('<span class="sep"></span><span class="bg_left"></span><span class="bg_right"></span>');
	$('.menu-main td:first, .menu-secondary td:first, .menu-service1 td:first, .menu-service2 td:first, .menu-service3 td:first, .menu-links1 td:first, .menu-links2 td:first').addClass('first');
	$('.menu-main td:last, .menu-secondary td:last, .menu-service1 td:last, .menu-service2 td:last, .menu-service3 td:last, .menu-links1 td:last, .menu-links2 td:last').addClass('last');
	
	// Скругленные картинки с эффектом тени
	$('.image-round1 a, .image-round2 a, .image-round3 a, .image-round4, .slider-photo, .image-round7 a').append('<span class="bg"></span>');
	
	// Разделители ссылок для постраниченой навигации
	$('.pagenavig a:not(:last)').append(' <span class="sep">|</span>');
	
	// Слайдер в статьях
	var length_img = $('.slider-photo .img img').length;
	var width_slider = $('.slider-photo').width();
	var x = 1;
	$('.slider-photo .bt_next').click(function() {
		if(x<length_img) {
			x++;
			$('.slider-photo .img').animate({'left':'-='+width_slider+'px'}, 400);
		} else if(x=length_img) {
			x=1;
			$('.slider-photo .img').animate({'left':'0px'}, 400);
		}
	});
	$('.slider-photo .bt_prev').click(function() {
		if(x!=1) {
			x--;
			$('.slider-photo .img').animate({'left':'+='+width_slider+'px'}, 400);
		} else if(x=1) {
			x = length_img;
			$('.slider-photo .img').animate({'left':'-='+width_slider*(length_img-1)+'px'}, 400);
		}
	});
	
	// Отправка формы по нажатию на ссылку с классом .submit
	$('.submit').live('click', function() {
		$(this).parents('form').submit();
		return false;
	});
	
	
	// Прозрачные кнопки
	$('.fade05 a').fadeTo(0, 0.5).css('cursor', 'default'); 
	
	
	// Появляющаяся кнопка для прокрутки страницы вверх
	$('body').upScrollButton({
		heightForButtonAppear:200,
		scrollToptIME: 1500
	});
	
	// Ссылка ответить
	$('.reply a').live('click', function() {
		$('.comments-container .added-textarea').before('<p class="reply"><a href="#">Ответить</a></p>').remove();
		$(this).parent().after('\
			<div class="added-textarea">\
				<div class="inp-text-container">\
					<textarea name="" cols="50" rows="2"></textarea>\
				</div><!--.inp-text-container-end-->\
				<div class="button block-right"><a href="#" class="submit">Комментировать</a></div><!--.button-end-->\
				<br class="clr"/>\
			</div>\
		');
		$(this).parent().remove();
		return false;
	});
	
});

$(window).load(function() {
	
	// Скрипт для скругления картинок
	$('.image-round').each(function() {
		var img_src = $(this).find('.img img').attr('src');
		var img_width = $(this).find('.img img').width();
		var img_height = $(this).find('.img img').height();
		$(this).find('.img').width(img_width).height(img_height).css('background-image', 'url('+img_src+')').find('img').remove();
	});
	
	// Вкладки
	$('.section .box-container').height($('.section .tabs').height()-6);
	$('.section .box-container .box').height($('.section .tabs').height()-8);
	$('.section .box-container .box').each(function() {
		var img_src2 = $(this).find('img').attr('src');
		$(this).css('background-image', 'url('+img_src2+')').find('img').remove();
	});
	$('ul.tabs').delegate('li:not(.active)', 'click', function() {
		$(this).addClass('active').siblings().removeClass('active')
		  .parents('div.section').find('div.box').hide().eq($(this).index()).fadeIn(500);
	});
	
	// Скрипт для подсказки
	$('.button:not(.fade05) a').hover(
		function() {
			var hint = $(this).parent().find('.hint');
			var hint_mt = (hint.height() / 2) - 4;
			var hint_right = hint.parent().width() + 10;
			hint.css({'margin-top':'-'+hint_mt+'px', 'right':hint_right+'px'});
			hint.fadeIn(400);
		},
		function() {
			$(this).parent().find('.hint').fadeOut(200);
		}
	);
	
});

$(document).ready(function(){
    $('.main-menu a').each(function () {      
        var location = window.location.href;
        var link = this.href               
        var result = location.match(link);  
        if(result != null) {                
            $(this).addClass('active');
        }
    });
    
})