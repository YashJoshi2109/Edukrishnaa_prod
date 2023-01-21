$(document).ready(function() {
	$('.chat_icon').click(function() {
		$('.chat_box').toggleClass('active');
	});

	$('.my-conv-form-wrapper').convform({selectInputStyle: 'disable'})
});

$(window).on("load", function(){
	$('[data-toggle="tooltip"]').tooltip().mouseover();
	setTimeout(function(){ $('[data-toggle="tooltip"]').tooltip('hide'); }, 3000);
});

    // $(window).on("scroll", function(){
    //    $('[data-toggle="tooltip"]').tooltip().mouseover();
    //    setTimeout(function(){ $('[data-toggle="tooltip"]').tooltip('hide'); }, 3000);
    // });
