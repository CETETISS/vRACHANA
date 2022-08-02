$(document).ready(function(){
    $('.bookmark').on('click',function(e){
        e.stopPropagation();
        alert('clicked');
        let elm = $(this);
        let isSaved = false;
        let fetchedId = elm.data('rid'); 
        //$(this).attr('title','Add to Bookmark')
       let title = "Add to Bookmark";
        
        if(elm.hasClass( "saved" ))
        {
            isSaved = true;
           // $(this).attr('title','Remove from Bookmark');
        }
   
        
       

        elm.toggleClass('saved');
        elm.find('i').toggleClass('fa-regular fa-solid');
        //this will retrun number if anything else is use please use attr - eg -below

        if(elm.hasClass( "saved" ))
        {
            title = "Saved to your bookmark";
        }
        elm.attr('title', title).attr('data-bs-original-title', title).tooltip('show');
       
        setTimeout(function(){
            title = "Remove from bookmark";
            elm.tooltip('hide')
            if(elm.hasClass( "saved" )){
                elm.attr('title', title).attr('data-bs-original-title', title);
            }
            
        }, 3000);
        //$(this).attr('data-fruit','7');
        alert(fetchedId + " is saved " + isSaved);
        
    });

    $('#page_bookmark').on('click',function(e){
        e.stopPropagation();
        alert('clicked');
        let elm = $(this);
        let isSaved = false;
        let fetchedId = elm.data('rid'); 
        let title = "Add to Bookmark";
        
        if(elm.hasClass( "active" ))
        {
            isSaved = true;
           // $(this).attr('title','Remove from Bookmark');
        }

        elm.toggleClass('active');
        if(elm.hasClass( "active" ))
        {
            title = "Saved to your bookmark";
        }
        elm.attr('title', title).attr('data-bs-original-title', title).tooltip('show');
       
        setTimeout(function(){
            title = "Remove from bookmark";
            elm.tooltip('hide')
            if(elm.hasClass( "active" )){
                elm.attr('title', title).attr('data-bs-original-title', title);
            }
            
        }, 3000);
        //$(this).attr('data-fruit','7');
        alert(fetchedId + " is saved " + isSaved);
    });

    $('#page_like').on('click',function(e){
        e.stopPropagation();
        alert('clicked');
        let elm = $(this);
        let isSaved = false;
        let fetchedId = elm.data('rid'); 
        let title = "Add to Bookmark";
        
        if(elm.hasClass( "active" ))
        {
            isSaved = true;
           // $(this).attr('title','Remove from Bookmark');
        }

        elm.toggleClass('active');
        if(elm.hasClass( "active" ))
        {
            title = "Liked";
        }
        elm.attr('title', title).attr('data-bs-original-title', title).tooltip('show');
       
        setTimeout(function(){
            title = "Unlike";
            elm.tooltip('hide')
            if(elm.hasClass( "actives" )){
                elm.attr('title', title).attr('data-bs-original-title', title);
            }
            
        }, 3000);
        //$(this).attr('data-fruit','7');
        alert(fetchedId + " is saved " + isSaved);
    });

});