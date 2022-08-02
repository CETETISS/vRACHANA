$(document).ready(function(){
    $('.side-sticky-btn').on('click',function(e){
        $(".quick-sticky-nav").toggleClass('open');
        $(this).find('i').toggleClass("fi-rs-list fi-rs-cross-circle");
    });
});
