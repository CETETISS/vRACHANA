$(document).ready(function(){



//------filter buttons----------//
var filterActive;
var category;

function filterCategory(category) {
    if (filterActive != category) {
        
        // reset results list
        $('.filter-cat-results .f-cat').removeClass('active');
        
        // elements to be filtered
        $('.filter-cat-results .f-cat')
            .filter('[data-cat="' + category + '"]')
            .addClass('active');
        
        // reset active filter
        filterActive = category;
        $('.filtering button').removeClass('active');
    }
}

$('.f-cat').addClass('active');

$('.filtering button').click(function() {
    if ($(this).hasClass('cat-all')) {
        $('.filter-cat-results .f-cat').addClass('active');
        filterActive = 'cat-all';
        $('.filtering button').removeClass('active');
    } else {
        filterCategory($(this).attr('data-cat'));
    }
    $(this).addClass('active');
});

//---------- load more--------------//

var counter=0;
var PRELOAD_FROM_BOTTOM = 100;
var loading = false;


        $(window).scroll(function () {
            
            if (($(window).scrollTop() >= $(document).height() - $(window).height() - ($('header').height()*2) - PRELOAD_FROM_BOTTOM) && counter < 2) {
                appendData();
            }
            // var currentHeaderHeight = $('header').height();
            // $('.btn-filters-layer').css('top', currentHeaderHeight);
        });
        function appendData() {
            //$(".infinite-loader").show();
            //stumilate

            if (loading) {
                return;
              }
              // Show loading icon.
              loading = true;
              
              $(".infinite-loader").show();

            window.setTimeout(function() {
                loading = false;
                            
                            //ajax call here
            var html = '';
            for (i = 0; i < 10; i++) {
                html += `<div class="card each-notificaiton-card f-cat active" data-cat="unread">
                <div class="card-body">
                  <h5 class="card-title">Card type 1=>`+i+` - ajax</h5>
                  <!-- <h6 class="card-subtitle mb-2 text-muted">Card subtitle</h6> -->
                  <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                  <div class="d-flex justify-content-between align-items-center">
                  <span>
                  <span class="text-muted fst-italic">15 minutes ago</span>
                  <span class="badge bg-danger ms-2">Unread</span>
                  </span>
                  <a href="#" class="card-link">View Notificaiton</a>
                  </div>
                </div>
              </div>`;
            }
            $('.list-of-notificaitons').append(html);
			counter++;
			
			if(counter==2){
               
                $('.load-more-action').html('<button class="btn btn-outline-secondary mx-auto" id="load-more-btn">Load More...</button>');
            }
            

            //hook
            filterActive = 'cat-all';
            if (filterActive != category) {
            $('.filtering button').removeClass('active');
            $('.filtering button.cat-all').addClass('active');

            //
            $(".infinite-loader").hide();
            }

        }
        , 1000);

        }

        $(document).on('click', '#load-more-btn', function(){
            
            //appendData();

            //if no more data
            $('#load-more-btn').hide();
            htmlc = `<div class="card  text-danger border-0 mb-3">
            <div class="card-body">
             
              <p class="card-text">All done. No more notifcications.</p>
            </div>
          </div>`;

          setTimeout(function(){
            $('.list-of-notificaitons').append(htmlc);
        }
        , 1500);
        });


    });