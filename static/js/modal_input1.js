jQuery(document).ready(function($){
	//open popup
	$('.modal_input1_open').on('click', function(event){
		event.preventDefault();
		$('#modal_input1').addClass('is-visible');
	});
	
	//close popup
	$('#modal_input1').on('click', function(event){
		if( $(event.target).is('#modal_input1_close') || $(event.target).is('#modal_input1') || $(event.target).is('#modal_input1_cancel') || $(event.target).is('#modal_input1_ok')) {
			event.preventDefault();
			$(this).removeClass('is-visible');
		}
	});
	//close popup when clicking the esc keyboard button
	$(document).keyup(function(event){
    	if(event.which==='27'){
    		$('#modal_input1').removeClass('is-visible');
	    }
    });
});
