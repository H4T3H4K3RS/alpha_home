jQuery(document).ready(function($){
	//open popup
	$('.modal_input2_open').on('click', function(event){
		event.preventDefault();
		$('#modal_input2').addClass('is-visible');
	});
	
	//close popup
	$('#modal_input2').on('click', function(event){
		if( $(event.target).is('#modal_input2_close') || $(event.target).is('#modal_input2') || $(event.target).is('#modal_input2_cancel') || $(event.target).is('#modal_input2_ok')) {
			event.preventDefault();
			$(this).removeClass('is-visible');
		}
	});
	//close popup when clicking the esc keyboard button
	$(document).keyup(function(event){
    	if(event.which==='27'){
    		$('#modal_input2').removeClass('is-visible');
	    }
    });
});
