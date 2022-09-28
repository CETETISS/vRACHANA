$(document).ready(function(){
    //Form Validation Start
  function checkvalidation() {
    alert('hello');
         var isperfect = true;
         var info ="";
         var objdata ={isperfect:"", info:""};
         
 //check field validations here
 //firstfield
   var fs_title = $("#fd-title").val();
    if (fs_title === '') {
                 info += "Please enter the title<br>";
                 isperfect = false;
         }
   
   //lastname
    var last_name = $('#lastname').val();
         if (last_name === '') {
                 info += "Please enter your last name<br>";
                 isperfect = false;
   }
  
   
   //email
    var user_email = $("#useremail").val();
    if (user_email === '') {
                 info += "Please Enter your email address<br>";
                 isperfect = false;
         }
   

 
   //username 
    var username = $("#username").val();
    if (username === '') {
     info += "Please Enter your Username<br>";
     isperfect = false;
   }
   else if (username.match(/^([$&+,:;=?@#|'<>.-^*()%!])+$/)) {
     info += "Please enter A-Z.<br>";
     isperfect = false;
   }


   //password check
   var password_1 = $("#resgisterPassword").val();
   var password_2 = $("#resgisterPasswordconfirm").val();
   if ($('.pr-password').attr('data-pr-password') != '1'){
     info += "Password Validation failed<br>";
     isperfect = false;
   }
   else if (password_1 != password_2) {
     info += "Confirm password didn't Match.<br>";
     isperfect = false;
   }


   //selectbox role
   var select_role = document.getElementById("selectRole");
   if (select_role.selectedIndex <=0) {
         info += "Please Select Valid Role<br>";
         isperfect = false;
   }


    //selectbox month
   var select_month = document.getElementById("selectMonth");
   if (select_month.selectedIndex <=0) {
         info += "Please Select Valid Month<br>";
         isperfect = false;
   }


    //selectbox year
   var select_year = document.getElementById("selectYear");
   if (select_year.selectedIndex <=0) {
         info += "Please Select Valid Year<br>";
         isperfect = false;
   }


   //privacy policy checkbox
   var policy_check = document.getElementById("Policycheck");
   if (policy_check.checked == false) {
    // alert("checked") ;
         info += "Please Check the Privacy Policy filed filed<br>";
         isperfect = false;
   }
   //subscribe checkbox
   // var subscribe_check = document.getElementById("Subscribecheck");
   // if (subscribe_check.checked == false) {
   //       info += "Check the filed<br>";
   //       isperfect = false;
   // }



      //check field validation ends
         
      objdata.isperfect = isperfect;
      objdata.info = info;
      //checkvalidation function ends
      
      return objdata;
    }   
    $('#cms_form').submit(function (e) {
      e.preventDefault();
      var validData = checkvalidation();
      if (validData.isperfect===false) {
         
          alert(validData.info);
          console.log('Hello');
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


});