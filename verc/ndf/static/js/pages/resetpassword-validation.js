
	  $(document).ready(function(){
		
		function checkvalidation() {
       //alert('hello');
            var isperfect = true;
            var info ="";
            var objdata ={isperfect:"", info:""};
            
    //check field validations here


     //password check
      var resetpassword_1 = $("#resetPassword").val();
      var resetpassword_2 = $("#resetPasswordconfirm").val();
      if ($('.pr-password').attr('data-pr-password') != '1'){
        info += "Password Validation failed<br>";
        isperfect = false;
      }
      else if (resetpassword_1 != resetpassword_2) {
        info += "Confirm password didn't Match.<br>";
        isperfect = false;
      }


      

         //check field validation ends
            
         objdata.isperfect = isperfect;
         objdata.info = info;
         //checkvalidation function ends
         
         return objdata;
       }   
		
		//form submit handler
          
            $('#resetpassword_form').submit(function (e) {
              e.preventDefault();
              var validData = checkvalidation();
              if (validData.isperfect===false) {
                 
                  //alert(validData.info);
                  //console.log('Hello');
                  var html_alert_content = `<div class="alert alert-danger d-flex align-items-center" role="alert">
                                            <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>
                                            <div class="alert-content">
                                            `+validData.info+`
                                            </div>
                                          </div>`;
                           $('.alerts-container').html(html_alert_content);
                           $(myToastEl).find('.toast-body').html(validData.info);
                           myToast.show();
                  //$('.infobox').html(validData.info);
              }
            });
        


        var myToastEl = document.getElementById('myToastEl')
        var myToast = bootstrap.Toast.getOrCreateInstance(myToastEl) // Returns a Bootstrap toast instance
        
        $(".pr-password").passwordRequirements();

        //Confirm Password 
  $("#toggle-password-btn1").on('click', function() {
    $(this).toggleClass("btn-outline-secondary btn-danger");
    $(this).find('i').toggleClass("fa-eye fa-eye-slash");
    var input = $($(this).attr("data-toggle"));
    if (input.attr("type") == "password") {
      input.attr("type", "text");
    } else {
      input.attr("type", "password");
    }
  });
		
	   //ready ends
	  });
