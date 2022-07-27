$(window).on("load", function () {
var scrollSpy = new bootstrap.ScrollSpy(document.body, {
    target: '.spy-nav',
    offset: 160
  });

});


document.querySelectorAll('.spy-nav a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        $(this.getAttribute('href')).css('scroll-margin-top', '160px');
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    
    });
});
