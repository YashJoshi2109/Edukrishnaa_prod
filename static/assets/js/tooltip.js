$(window).on("load", function(){
	$('[data-toggle="tooltip"]').tooltip().mouseover();
	setTimeout(function(){ $('[data-toggle="tooltip"]').tooltip('hide'); }, 3000);
});
