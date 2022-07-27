
	  $(document).ready(function(){
		
		function checkvalidation() {
       //alert('hello');
            var isperfect = true;
            var info ="";
            var objdata ={isperfect:"", info:""};
            
    //check field validations here
    //firstname
		  var pro_person_name = $("#profile_firstname").val();
		   if (pro_person_name === '') {
                    info += "Please enter your first name<br>";
                    isperfect = false;
            }
		  
      //lastname
		   var pro_last_name = $('#profile_lastname').val();
            if (pro_last_name === '') {
                    info += "Please enter your last name<br>";
                    isperfect = false;
      }
		 
		  
      //email
       var pro_user_email = $("#profile_useremail").val();
		   if (pro_user_email === '') {
                    info += "Please Enter your email address<br>";
                    isperfect = false;
            }
      

    
            var username = $("#profile_username").val();
            if (username === '') {
             info += "Please Enter your Username<br>";
             isperfect = false;
           }
           else if (username.match(/^([$&+,:;=?@#|'<>.-^*()%!])+$/)) {
             info += "Please enter A-Z.<br>";
             isperfect = false;
           }
     


      //selectbox role
      var pro_select_role = document.getElementById("profile_selectRole");
      if (pro_select_role.selectedIndex <=0) {
            info += "Please Select Valid Role<br>";
            isperfect = false;
      }


       //selectbox month
      var pro_select_month = document.getElementById("profile_selectMonth");
      if (pro_select_month.selectedIndex <=0) {
            info += "Please Select Valid Month<br>";
            isperfect = false;
      }


       //selectbox year
      var pro_select_year = document.getElementById("profile_selectYear");
      if (pro_select_year.selectedIndex <=0) {
            info += "Please Select Valid Year<br>";
            isperfect = false;
      }




         //check field validation ends
            
         objdata.isperfect = isperfect;
         objdata.info = info;
         //checkvalidation function ends
         
         return objdata;
       }   
		
		//form submit handler
          
            $('#profile_form').submit(function (e) {
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



	   //ready ends
	  });
