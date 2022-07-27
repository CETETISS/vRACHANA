$(document).ready(function(){
    $(".side-close-btn, .side-slide-strip").on('click',function(){
        $('.side-canvas').toggleClass('show');
        $('.side-slide-strip').find('i').toggleClass("fi-rs-settings-sliders fi-rs-cross-circle");
    });
//end ready
});