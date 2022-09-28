$(document).ready(function () {
  var collectionModalEl = document.querySelector('#collectionModal');
  var col_Modal = bootstrap.Modal.getOrCreateInstance(collectionModalEl);
  function ToggleBGColour(item) {
      var td = $(item).parent();      
      if (td.is('.rowSelected'))      
          td.removeClass("rowSelected");      
      else        
          td.addClass("rowSelected");     
  }

  //clear modal selection
  $("#clear_selected").on('click',function() {
  $('.all-collection-container input[type=checkbox]').prop('checked',false);
  });
   
  $("#add_collection_btn").on('click',function() {
    var arr = $(".all-collection-container input:checkbox:checked").map(function() { return $(this).parent().parent().prop("outerHTML") }).get();
    $("#selectedCards").html(arr.join(''));
    col_Modal.hide();
  });
  $(document).on('click','.btn-del-collection',function(e) {
   
    $(this).closest('.each-collection-card').remove();
  });

//extra
$('#collection-read-btn').on('click',function() {
  var arr_confirmed = $(".selected-collection-container input:checkbox").map(function() { return $(this).attr('id') }).get();
    $("#selectedCards_input").val(arr_confirmed.join(','));
});
//extra ends

  
  });

  

  
  

  
     
