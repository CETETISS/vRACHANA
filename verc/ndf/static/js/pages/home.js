$(document).ready(function(){
      
    

    const swiperFeaturedResource = new Swiper(".resource-slider", {
        slidesPerView: 4,
        spaceBetween: 30,
        preventClicks:false,
        preventClicksPropagation:false,
        pauseOnMouseEnter: true,
        centeredSlidesBounds: true,
        loop: true,
        slidesOffsetAfter:0,
        slidesOffsetBefore:0,
        //shortSwipes: false,
        autoplay: {
            delay: 3000,
        },
       // autoplay:false,
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
          },
           //pagination
          //  pagination: {
          //   el: ".swiper-pagination",
          //   clickable: true,
          // },
        // Responsive breakpoints
        breakpoints: {
            // when window width is >= 320px
            320: {
            slidesPerView: 1,
            spaceBetween: 20
            },
            // when window width is >= 480px
            480: {
            slidesPerView: 1,
            spaceBetween: 30,
            
            },
            // when window width is >= 640px
            640: {
            slidesPerView: 2,
            spaceBetween: 40
            },
            // when window width is >= 1200px
            1200: {
                slidesPerView: 3,
                spaceBetween: 20
                },
                // when window width is >= 1200px
            1366: {
                slidesPerView: 4,
                spaceBetween: 18
                }
        },
        on: {
          afterInit: function () {
             //match height initialize
          //  $('.featured-swiper .display-card').matchHeight();
          }
        }
      });

     


    const swiperFeaturedSubject = new Swiper(".subject_Swiper", {
        slidesPerView: 6,
        spaceBetween: 30,
        centeredSlides: true,
        loop: true,
        pagination: {
          el: ".swiper-pagination2",
          clickable: true,
        },
        autoplay: {
            delay: 3000,
        },
        // Responsive breakpoints
        breakpoints: {
            // when window width is >= 320px
            320: {
            slidesPerView: 2,
            spaceBetween: 20
            },
            // when window width is >= 480px
            480: {
            slidesPerView: 2,
            spaceBetween: 30
            },
            // when window width is >= 640px
            640: {
            slidesPerView: 3,
            spaceBetween: 40
            },
            // when window width is >= 1200px
            1200: {
                slidesPerView: 4,
                spaceBetween: 40
                },
                // when window width is >= 1200px
            1366: {
                slidesPerView: 6,
                spaceBetween: 40
                }
        }
      });

      const swiperFeaturedBlog = new Swiper(".blog-slider", {
        slidesPerView: 3,
        spaceBetween: 30,
        preventClicks:false,
        preventClicksPropagation:false,
        pauseOnMouseEnter: true,
        centeredSlidesBounds: true,
        loop: true,
        slidesOffsetAfter:0,
        slidesOffsetBefore:0,
        autoplay: {
            delay: 3000,
        },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
          },
          pagination: {
            el: ".swiper-pagination4",
            clickable: true,
          },
        // Responsive breakpoints
        breakpoints: {
            // when window width is >= 320px
            320: {
            slidesPerView: 1,
            spaceBetween: 20
            },
            // when window width is >= 480px
            480: {
            slidesPerView: 1,
            spaceBetween: 30
            },
            // when window width is >= 640px
            640: {
            slidesPerView: 3,
            spaceBetween: 40
            },
            // when window width is >= 1200px
            1200: {
                slidesPerView: 3,
                spaceBetween: 20
                },
                // when window width is >= 1200px
            1366: {
                slidesPerView: 3,
                spaceBetween: 18
                }
        },
        on: {
          afterInit: function () {
             //match height initialize
           // $('.featured-swiper .display-card').matchHeight();
          }
        }
      });

      const swiperFeaturedEvents = new Swiper(".events-slider", {
        slidesPerView: 3,
        spaceBetween: 30,
        preventClicks:false,
        preventClicksPropagation:false,
        pauseOnMouseEnter: true,
        centeredSlidesBounds: true,
        loop: true,
        slidesOffsetAfter:0,
        slidesOffsetBefore:0,
        autoplay: {
            delay: 3000,
        },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
          },
          pagination: {
            el: ".swiper-pagination3",
            clickable: true,
          },
        // Responsive breakpoints
        breakpoints: {
            // when window width is >= 320px
            320: {
            slidesPerView: 1,
            spaceBetween: 20
            },
            // when window width is >= 480px
            480: {
            slidesPerView: 1,
            spaceBetween: 30
            },
            // when window width is >= 640px
            640: {
            slidesPerView: 3,
            spaceBetween: 40
            },
            // when window width is >= 1200px
            1200: {
                slidesPerView: 3,
                spaceBetween: 20
                },
                // when window width is >= 1200px
            1366: {
                slidesPerView: 3,
                spaceBetween: 18
                }
        },
        on: {
          afterInit: function () {
             //match height initialize
          //  $('.featured-swiper .display-card').matchHeight();
          }
        }
      });

      const swiperFeaturedTestimonials= new Swiper(".testimonials-slider", {
        slidesPerView: 3,
        spaceBetween: 30,
        preventClicks:false,
        preventClicksPropagation:false,
        centeredSlides:true,
        centeredSlidesBounds: true,
        loop: true,
        slidesOffsetAfter:0,
        slidesOffsetBefore:0,
        autoplay: {
            delay: 3000,
        },
        navigation: {
            nextEl: ".swiper-button-next",
            prevEl: ".swiper-button-prev",
          },
          pagination: {
            el: ".swiper-pagination5",
            clickable: true,
          },
        // Responsive breakpoints
        breakpoints: {
            // when window width is >= 320px
            320: {
            slidesPerView: 1,
            spaceBetween: 20
            },
            // when window width is >= 480px
            480: {
            slidesPerView: 1,
            spaceBetween: 30
            },
            // when window width is >= 640px
            640: {
            slidesPerView: 3,
            spaceBetween: 40
            },
            // when window width is >= 1200px
            1200: {
                slidesPerView: 3,
                spaceBetween: 20
                },
                // when window width is >= 1200px
            1366: {
                slidesPerView: 3,
                spaceBetween: 90
                }
        },
        on: {
          afterInit: function () {
             //match height initialize
          $('.testimonials-slider .display-card').matchHeight();
          }
        }
      });


//
(function () {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })
})()


var modalMsg = new bootstrap.Modal(document.getElementById('msgModel'));
//on subscribe - if true
$( "#subscribe-form" ).submit(function( event ) {
  event.preventDefault();


modalMsg.show();

});

var modalcardlang = new bootstrap.Modal(document.getElementById('cardLangModel'));
$(".card-lang-link").on('click',function(e){
  e.preventDefault();
  let fetchedId = $(this).data('rid'); 
  //below fetch is for demo purpose - do a ajax call and update body as requried.
  $('#cardLangModel').find('.modal-title').append(" for id : " + fetchedId);

  modalcardlang.show();
});
    //doc ready ends  
    });