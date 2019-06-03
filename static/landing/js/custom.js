jQuery.noConflict();
jQuery(function($) {  

var $ajaxformlabel = $('#ajaxform label'),
	$hiddenform = $('#hiddenform'),
	$ajaxformsubmit = $('#ajaxform input.ajaxsubmit');
	
$ajaxformsubmit.css('opacity', '0.5');
$ajaxformlabel.on('click', function(){
	if($(this).find('input').prop("checked")) { $(this).addClass('activelabel').find('.button').html('Удалить');  } else { $(this).removeClass('activelabel').find('.button').html('Добавить в расчет'); }
	if ($ajaxformlabel.hasClass("activelabel")) {
		if($hiddenform.is(':hidden')) { $hiddenform.slideDown(200); $ajaxformsubmit.removeAttr('disabled').css('opacity', '1');  }
	} else {
		if($hiddenform.is(':visible')) { $hiddenform.slideUp(200); $ajaxformsubmit.attr('disabled', 'disabled').css('opacity', '0.5'); }
	}
	var $activelabel = $('#ajaxform label.activelabel').length;
	var $countactivelabel;
	if ($activelabel == 0) { $countactivelabel = $activelabel+' систем'; }
	if ($activelabel == 1) { $countactivelabel = $activelabel+' систему'; }
	if ($activelabel == 2 || $activelabel == 3 || $activelabel == 4 ) { $countactivelabel = $activelabel+' системы'; }
	if ($activelabel > 4 ) { $countactivelabel = $activelabel+' систем'; }
	$('#countactivelabel').html($countactivelabel);
});



/***********************************************
SMOOTH SCROLL TO ID
***********************************************/

// handle links with @href started with '#' only
$(document).on('click', 'a[href^="#"]', function(e) {
    // target element id
    var id = $(this).attr('href');

    // target element
    var $id = $(id);
    if ($id.length === 0) {
        return;
    }

    // prevent standard hash navigation (avoid blinking in IE)
    e.preventDefault();

    // top position relative to the document
	if ($('#singlepostcont>.box').hasClass('box_open')) {
		var doc = $('#singlepostcont');
		var pos = $(id).position().top;
	} else {
		var doc = $('body');
		var pos = $(id).offset().top;
	}

    // animated top scrolling
    doc.animate({scrollTop: pos});
});

});