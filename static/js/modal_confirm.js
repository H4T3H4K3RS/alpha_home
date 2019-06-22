jQuery(document).ready(function($){
	//open popup
	$('.modal_confirm_open').on('click', function(event){
		event.preventDefault();
		$('#modal_confirm').addClass('is-visible');
	});
	
	//close popup
	$('#modal_confirm').on('click', function(event){
		if( $(event.target).is('#modal_confirm_close') || $(event.target).is('#modal_confirm') || $(event.target).is('#modal_confirm_cancel') || $(event.target).is('#modal_confirm_ok')) {
			event.preventDefault();
			$(this).removeClass('is-visible');
		}
	});
	//close popup when clicking the esc keyboard button
	$(document).keyup(function(event){
    	if(event.which==='27'){
    		$('#modal_confirm').removeClass('is-visible');
	    }
    });
});
