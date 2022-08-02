$(document).ready(function(){
    setTimeout(function(){
        $(".se-pre-con").fadeOut("slow");
    },3000);
    


    const display_time_container = document.getElementsByClassName('ist');
    //get current time
    setInterval(function () {
                let currenttime = moment().format('MMM Do YY, h:mm:ss a');
                
                display_time_container[0].innerHTML = (currenttime);
            }, 1000);
    // get current time ends

    //css mode
    let isLightCssMode;
    let isTrueSetLightMode;
    function fetchCurrentCssMode(){
        //below line is used while testing purpose
        //localStorage.removeItem("savedCssMode");
        if (typeof(Storage) !== "undefined") {
          
            if (localStorage.savedCssMode) {
                isTrueSetLightMode = (localStorage.savedCssMode === 'true');
                isLightCssMode = isTrueSetLightMode;
                //alert('fetching again = ' + isLightCssMode);

                
                if(isTrueSetLightMode==false){
                    //alert('toogle change = ' + isLightCssMode);
                document.getElementById("flexSwitchCheckChecked").checked = true;
                }
              } else {
                isLightCssMode=true;
                localStorage.savedCssMode = isLightCssMode;
                //alert('first time' + localStorage.savedCssMode);
              }
          } else {
            console.log('Sorry! No Web Storage support..');
          }
    }

    function setCurrentCssMode(){
        let mode_element = document.getElementById('modeLabel');
       
        if(isLightCssMode){
            mode_element.innerHTML = "Light";
            if (document.body.classList.contains('dark')) {
                document.body.classList.remove('dark');
            }
        }else{
            mode_element.innerHTML = "Dark";
            if (!document.body.classList.contains('dark')) {
                document.body.classList.add('dark');
            }

            
        }
       //document.getElementsByTagName('body').classList.toggle("dark");
    }

    function setBodyPadding(){
        $('body').css('padding-top',$('header').height());
        manage_filter_section();
    }
    window.addEventListener('resize', function(event) {
        setBodyPadding();
    }, true);

    //run for 1sttime
    fetchCurrentCssMode();
    setCurrentCssMode();
    setBodyPadding();
   
    // on mode toggle clicked
            checkCssMode = document.getElementById('flexSwitchCheckChecked').addEventListener('click', event => {
              
                if(event.target.checked) {
                    isLightCssMode = false;
                }else{ 
                    isLightCssMode = true;
                }
                localStorage.savedCssMode = isLightCssMode;
                //alert('changed to = ' + isLightCssMode);
                setCurrentCssMode();
            });

    

    //css mode ends
    
    //font size change
    const baseFonSize = 16;
    const baseFontPercent = 100;
    $('#_biggify').on('click', function() {
        changeFontSize(4);
        setBodyPadding();
      })
      
      $('#_smallify').on('click', function() {
        changeFontSize(-4);
        setBodyPadding();
      })
      
      $('#_reset').on('click', function() {
        $('html').css('font-size', baseFonSize + 'px');
        if (typeof(Storage) !== "undefined") {
        localStorage.removeItem("savedFontSize"); 
        
        //$(generalToast).find('.toast-body').html('Default font size of '+baseFonSize+'px initiated.');
        $(generalToast).find('.toast-body').html('Default font size of '+baseFontPercent+'% initiated.');
                    $(generalToast).toast('show');
        }
        setBodyPadding();
      })

      
     
   

      function changeFontSize(direction){
        let fontSize = parseInt($('html').css('font-size'));
        
        if ((fontSize + direction) >=12 && (fontSize + direction) <= 32) {
            let newFontSize = fontSize+direction;
            setCurrentFontSize(newFontSize);
        }

        
        
    }

    
    var generalToast = document.getElementById('general-toast');
    //font size change
    function setCurrentFontSize(sentFontSize){
       
            
        if (typeof(Storage) !== "undefined") {
            if(typeof(sentFontSize)!== "undefined"){
            localStorage.savedFontSize = sentFontSize;
            $('html').css('font-size', localStorage.savedFontSize+'px');
                   // $(generalToast).find('.toast-body').html('Font size set to ' + sentFontSize +'px as per user defined settings');

                    let convertTopercent = ((100*sentFontSize)/baseFonSize)
                    $(generalToast).find('.toast-body').html('Font size set to ' + convertTopercent +'% as per user defined settings');
                    $(generalToast).toast('show');
            }

            
           
        }else {
            console.log('Sorry! No Web Storage support..');
          }
        
    }

//run for 1sttime
 //testing line below
 //localStorage.removeItem("savedFontSize"); 
setCurrentFontSize(localStorage.savedFontSize);

    //font size change ends

    //sticky header
    
        var pageScroll = 10;
        var moreScroll = 200;
        let pastScroll = 0;
         $(window).scroll(function() {
           var scroll = getCurrentScroll();
          
             if ( scroll >= pageScroll ) {
                //   $('header').addClass('sticky-header').delay(1000).queue(function(){
                //     $(this).addClass("scroll-effect").dequeue();
                // });
                $('header').addClass('sticky-header');
                  
                    if ( scroll >= pageScroll + moreScroll ) {
                   
                        if( scroll >= pastScroll ) {
                            $('.sticky-section').queue(function(){
                                $(this).slideUp().dequeue();
                            });
                          }else{
                            $('.sticky-section').queue(function(){
                                $(this).slideDown().dequeue();
                            });
                          }
                          
                        
                    }
                    
                }

               else {
                   $('header').removeClass('sticky-header');
               }
               pastScroll = scroll;
               setTimeout(setBodyPadding, 2000);
               
               
         });
       function getCurrentScroll() {
           return window.pageYOffset || document.documentElement.scrollTop;
           }
       
    //sticky header ends

     /* ==========================================
    Back To Top
    ========================================== */
    if ($('#back-to-top').length) {
        var scrollTrigger = 400, // px
            backToTop = function () {
                var scrollTop = $(window).scrollTop();
                if (scrollTop > scrollTrigger) {
                    $('#back-to-top').addClass('show');
                } else {
                    $('#back-to-top').removeClass('show');
                }
            };
        backToTop();
        $(window).on('scroll', function () {
            backToTop();
        });
        $('#back-to-top').on('click', function (e) {
            e.preventDefault();
            $('html,body').animate({
                scrollTop: 0
            }, 700);
        });
    }

    //tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

//menu search close
var searchCollapse = document.getElementById('collapseSearchBox');
var bsCollapse = new bootstrap.Collapse(searchCollapse, {
  toggle: false
})
$('#search-close-btn').on('click',function(e){
    //collapseSearchBox
    bsCollapse.hide();
});

$(document).click(function() {
    var searchContainer = $(".top-search-box");
    if (!searchContainer.is(event.target) && !searchContainer.has(event.target).length) {
        //searchContainer.hide();
        bsCollapse.hide();
    }
});

//manage filter section
function manage_filter_section(){
    
    if($('.page-content').hasClass('has-filter-layer')){
        
        setTimeout(function(){
            var currentHeaderHeight = $('header').height();
        $('.btn-filters-layer').css('top', currentHeaderHeight);
        },1000);
        
    }
}
//manage filter section ends


//login 

var loginModel = new bootstrap.Modal(document.getElementById('loginModel'));
//call login code below
//loginModel.show();

//login toogle password
$("#toggle-password-btn").on('click', function() {
    $(this).toggleClass("btn-outline-secondary btn-danger");
    $(this).find('i').toggleClass("fa-eye fa-eye-slash");
    var input = $($(this).attr("data-toggle"));
    if (input.attr("type") == "password") {
      input.attr("type", "text");
    } else {
      input.attr("type", "password");
    }
  });

//toogle password ends

//manage like click
$(document).on('click', '.manageLike', function(e){
    e.preventDefault();
    //colllect id
    let rid = $(this).attr("data-rid");
    $(this).toggleClass("liked");
    if($(this).hasClass("liked")){
        $(this).find("span").html('Liked');
        $(this).attr("data-bs-original-title","Remove Like");
        //store ajax variable
    }else{
        $(this).find("span").html('Like');
        $(this).attr("data-bs-original-title", "Like it");
        //store ajax variable
    }
    
    $(this).find("i").toggleClass("fa-solid fa-regular");

    //do ajax call
});

//card share button pop up initalize
var shareModelElem = document.getElementById('shareModal');
if (shareModelElem !== null)
{
//if stqarts above

var shareModel = new bootstrap.Modal(document.getElementById('shareModal'));

$(document).on('click', '.share-card-btn', function(e){
    e.preventDefault();
    //colllect id
    let rid = $(this).attr("data-rid");
    let hlink = $(this).attr("data-hlink");
    $("#shareModal .copy-input").val(hlink);
   
    shareModel.show();
    setShareLinks(hlink)
});

const popup = document.querySelector("#shareModal"),
        field = popup.querySelector(".field"),
      input = field.querySelector(".copy-input"),
      copy = field.querySelector(".copy-btn");

copy.onclick = ()=>{
    input.select(); //select input value
    if(document.execCommand("copy")){ //if the selected text copy
      field.classList.add("active");
      copy.innerText = "Copied";
      setTimeout(()=>{
        window.getSelection().removeAllRanges(); //remove selection from document
        field.classList.remove("active");
        copy.innerText = "Copy";
      }, 3000);
    }
  }

//share social media
setShareLinks();
//https://github.com/bradvin/social-share-urls#telegramme
    function socialWindow(url) {
        
    var left = (screen.width -570) / 2;
    var top = (screen.height -570) / 2;
    var params = "menubar=no,toolbar=no,status=no,width=570,height=570,top=" + top + ",left=" + left;  window.open(url,"NewWindow",params);
}

function setShareLinks(sharelink) {
   // var pageUrl = encodeURIComponent(document.URL);
   var url ='';
   var pageUrl = encodeURIComponent(sharelink);
    var tweet = encodeURIComponent($("meta[property='og:description']").attr("content"));

$(".social-share.facebook").on("click", function(e) { 
    url="https://www.facebook.com/sharer.php?u=" + pageUrl;

    socialWindow(url);
});

$(".social-share.twitter").on("click", function(e) {

    url = "https://twitter.com/intent/tweet?url=" + pageUrl + "&text=" + tweet;
    socialWindow(url);
});

$(".social-share.linkedin").on("click", function(e) {

    url = "https://www.linkedin.com/shareArticle?mini=true&url=" + pageUrl;
    socialWindow(url);
});

$(".social-share.telegram").on("click", function(e) {

    url = "https://telegram.me/share/url?url="+ pageUrl+"&text="+ tweet;
    socialWindow(url);

});

$(".social-share.whatsapp").on("click", function(e) {

    url = "https://api.whatsapp.com/send/?text="+ pageUrl;
    socialWindow(url);
});

$(".social-share.mail").on("click", function(e) {

const ulink = $("#shareModal .copy-input").val();
url = "mailto:?subject=Shared via Vrachna&body=Hi,I found this website and thought you might like it "+ ulink + '.';
    socialWindow(url);
    
});


}
    

//if ends below
}

//moreless-button
$('.moreless-button').click(function() {
   
    if ($(this).text() == "Read more") {
      $(this).text("Read less")
    } else {
      $(this).text("Read more")
    }
  });

    //ready ends below
});