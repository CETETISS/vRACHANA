$(document).ready(function(){
    var slider = new Swiper ('.gallery-slider', {
        slidesPerView: 1,
        centeredSlides: true,
        loop: true,
        loopedSlides: 6,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });
    
    //thumbs
    var thumbs = new Swiper ('.gallery-thumbs', {
        slidesPerView: 'auto',
        spaceBetween: 10,
        centeredSlides: true,
        loop: true,
        slideToClickedSlide: true,
    });
    
    //3
    //slider.params.control = thumbs;
    //thumbs.params.control = slider;
    
    //4
    slider.controller.control = thumbs;
    thumbs.controller.control = slider;
    //ready ends
});

