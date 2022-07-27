$(document).ready(function(){
    $('.notificaitons-dropdown').on('click',function(e){
       // e.stopPropagation();
       if($('.notificaitons-dropdown').hasClass('has_new_alerts')){
        $('.notificaitons-dropdown').removeClass('has_new_alerts');
       }
        
    });

    //for testing purpose

    function stopDummyInteveralSession() {
        clearInterval(notify_alerts_timer_interval);
      }
   
    let countNoty = 1;
    
    const notify_alerts_timer_interval = setInterval(function () {
        if(countNoty >= 10){
            stopDummyInteveralSession(notify_alerts_timer_interval)
        }
        //add notificaiton alerts
        if(!$('.notificaitons-dropdown').hasClass('has_new_alerts')){
            $('.notificaitons-dropdown').addClass('has_new_alerts');
           
          
           }

           //populate dummy data
           // insert new notificaitons - ajax call will be done here
             //href is dummy for testing
           let newNote = `<li>
          
           <a href="refirectingto/?reid=`+countNoty+`" class="top-text-block unread each-notificaiton" data-nid="`+ countNoty+ `">
             <div class="top-text-heading ">You have <b>3 new themes, id = `+ countNoty+ `</b> trending</div>
             <div class="d-flex justify-content-between align-items-center">
             <div class="top-text-light">15 minutes ago</div>
             <div class="read-status">
               <span class="badge rounded-pill bg-danger">Unread</span>
             </div>
           </div>
           </a> 
         </li>`;

          $(newNote).prependTo( ".notifications-bucket-list" );
          countNoty = countNoty +1; 

    }, 3000);

    

    $(document).on("click", "a.each-notificaiton", function(e){
        e.preventDefault();
     const targetLink =  $(this).attr('href');
     const targetId = $(this).attr('data-nid');
     //before redirecting mark as unread
     if($(this).hasClass('unread')){
        $(this).removeClass('unread');
        $(this).find(".read-status").html("");
       }
     alert('Data captured -you have clicked id no '+ targetId +', this click will be redirected to' + targetLink + '<br> do Ajax here');
});
    


});