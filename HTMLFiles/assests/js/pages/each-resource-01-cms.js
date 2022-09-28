$(document).ready(function () {
  $("#fd-excerpt").textcounter({
    max: 15,
    stopInputAtMaximum: false,
    countDownText: "%d characters remaining",
  });
  //tags - multiselct
  $(".tagsInput, .multipleSelect").fastselect();

  //replicate content to other text-field 

  $("#fd-title").on('keyup',function(event) {
    var stt = $(this).val();
    $("#mfd-title").val(stt);
  });

  //date picker demo
  //$('#datepicker').datepicker('setDate', 'now');
  //var date = new Date();
  //   var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
  //   var end = new Date(date.getFullYear(), date.getMonth(), date.getDate());
  $("#datepicker").datepicker({
    format: "dd/mm/yyyy",
    todayHighlight: true,
  });
  $("#datepicker").datepicker("setDate", "now");

  //add team members
  $(document)
    .on("click", ".team_container .add_member_btn", function (e) {
      e.preventDefault();
      //alert('hi');
        var input_value = $(".team_container .input_value");
        var is_input_value_empty = false;
        for (var i = 0; i < input_value.length; i++) {
          if($(input_value[i]).val() === ""){
            is_input_value_empty = true;
          }
         
        }
        if(is_input_value_empty === false){
      var member_container_html =
      `<div class="row each-form-set mb-3">
      <div class="col-sm-10">
       
          <div class="input-group">
            
            <input type="text" aria-label="First name" name="input1[]" class="form-control input_value samefiledscheck roleche" placeholder="Name">
            <input type="text" aria-label="Last name" name="input2[]" class="form-control  input_value samefiledscheck roleche" placeholder="Role">
          </div>
        </div>
        <div class="col-sm-2">
        <button class="btn btn-danger member-del">
            <i class="fa-solid fa-minus"></i>
          </button>
        </div>
        </div>`;
        $(".each_member_container").prepend(member_container_html);
          
        }
        else{
          $(myToastEl).find(".toast-body").html('Please enter some data');
          myToast.show();
        }
        
        
    });
  $(document)
    .on("click", ".team_container .each-form-set .member-add", function (e) {
      e.preventDefault();
      //var current_obj = $(this).closest(".each-form-set");
      //check if blank current obj
    
     
     
      // alert('hi');
      // console.log(current_obj.find('.input_value').val());

      
    })
    .on("click", ".team_container .each-form-set .member-del", function (e) {
      e.preventDefault();
      $(this).closest(".each-form-set").remove();
      return false;
    });
  //add team members end

  
  //Add Content Available Langauge
  $(document)
.on("click", ".lang_container .add_lgn_btn", function (e) {
  e.preventDefault();
  // alert('hi');
    var langinput_value = $(".lang_container .input_value");
    var is_langinput_value_empty = false;
    for (var i = 0; i < langinput_value.length; i++) {
      if($(langinput_value[i]).val() === ""){
        is_langinput_value_empty = true;
      }
     
    }
    if(is_langinput_value_empty === false){
  var lang_container_html =
    `  <div class="row langbx">
                         
    <div class="col-sm-10">
       <div class="mb-3">
           <label for="languagesecc3" class="form-label">Article Language<span class="text-danger">*</span> </label>
           <select class="form-select form-control input_value" aria-label="Default select example" id="languagesecc3">
             <option value="">Open this select menu</option>
             <option value="1">English</option>
             <option value="3">Hindi</option>
             <option value="2">Urdu</option>
             <option value="3">Marthi</option>
           </select>
           </div>
           <div class="mb-3">
               <label for="fd-url-link" class="form-label">URL</label> <span class="text-danger">*</span>
               <input type="text" class="form-control input_value" id="fd-url-link" placeholder="URL">
             </div>
       </div>
   
   <div class="col-sm-2">
       <button class="btn btn-danger member-del">
         <i class="fa-solid fa-minus"></i>
       </button>
       </div>
   </div>`;
    $(".lang_url_container").prepend(lang_container_html);
      
    }
    else{
      $(myToastEl).find(".toast-body").html('Please select a Language');
      myToast.show();
    }
    
    
});
$(document)
.on("click", ".lang_container .add_lgn_btn", function (e) {
  e.preventDefault();

  
})
.on("click", ".langbx .member-del", function (e) {
  e.preventDefault();
  $(this).closest(".langbx").remove();
  return false;
});
//Add Content Available Langauge
  //add sponsors
  $(document)
    .on("click", ".sponsor_container .member-add", function (e) {
      e.preventDefault();
      // alert('hi');
        var spoinput_value = $(".sponsor_container .input_value");
        var is_spoinput_value_empty = false;
        for (var i = 0; i < spoinput_value.length; i++) {
          if($(spoinput_value[i]).val() === ""){
            is_spoinput_value_empty = true;
          }
         
        }
        if(is_spoinput_value_empty === false){
      var sponsor_container_html =
      `<div class="row each-form-set mb-3">
      <div class="col-sm-12 mb-3">
        <input type="file" name="sponsor_files[]" class="input_value file_uploader">
      </div>
    <div class="col-sm-10 mb-3">
         
          <input type="text" aria-label="Sponsor title" name="input2[]" class="form-control input_value" placeholder="Sponsor Title">
        
      </div>
      <div class="col-sm-2">
      <button class="btn btn-danger member-del">
        <i class="fa-solid fa-minus"></i>
      </button>
      </div>
      <hr>
      </div>`;
        $(".each_sponsor_container").prepend(sponsor_container_html);
          
        }
        else{
          $(myToastEl).find(".toast-body").html('Please upload a image & title');
          myToast.show();
        }
        
        
    });
  $(document)
    .on("click", ".sponsor_container .member-add", function (e) {
      e.preventDefault();
    
      
    })
    .on("click", ".sponsor_container .each-form-set .member-del", function (e) {
      e.preventDefault();
      $(this).closest(".each-form-set").remove();
      return false;
    });
  //add sponsor members end
  
//check_type
$(document)
.on("change", ".help_container .check_type", function (e) {
  let topset = $(this).closest(".each-form-set");
  let cur_val = $(this).val();
  topset.find('.inp-sec-1').remove();
  topset.find('.inp-sec-2').remove();

  let html_inp_sec_1 = `
  <div class="inp-sec-1">
    <label for="help_thumbimg" class="col-sm-12 col-form-label mb-3">Upload Thumb</label>
    <input class="form-control  file_uploader inp-1" type="file" id="help_thumbimg" name="gallery_files[]">
  </div>
  `;

  let html_inp_sec_2 = `
  <div class="inp-sec-2">
  <label for="help_url" class="col-form-label mb-3 ">URL</label> <span class="text-secondary fst-italic txt-sm-85">(* If content is of type url or youtube video link is provided)</span>
    <input type="text" aria-label="Sponsor title" name="inputg3[]" class="form-control  col-sm-12 input_value member_url" placeholder="Desc or URL link" id="help_url">
    </div>
  `;

  

  if(cur_val==='image' || cur_val==='resource'){
    topset.find('.var_html').append(html_inp_sec_1);
  }else{
    topset.find('.inp-sec-1').remove();
  }

  if(cur_val==='video' || cur_val==='url'){
    //topset.find('.inp-sec-2').show();
    topset.find('.var_html').append(html_inp_sec_2);
  }else{
    topset.find('.inp-sec-2').hide();
  }
 
  
});
//add help
$(document)
.on("click", ".help_container .member-add", function (e) {
  e.preventDefault();
  // alert('hi');
    var helpinput_value = $(".help_container .input_value");
    var is_helpinput_value_empty = false;
    for (var i = 0; i < helpinput_value.length; i++) {
      if($(helpinput_value[i]).val() === ""){
        is_helpinput_value_empty = true;
      }
     
    }
    if(is_helpinput_value_empty === false){
  var help_container_html =
  `<div class="row each-form-set mb-3">

  <div class="col-sm-10 mb-3">
    
    <label for="uploadThumb_file" class="col-sm-12 col-form-label mb-3">Type</label>
    <select class="form-select input_value check_type" id="samefiledscheckbx" aria-label="Type" name="typeg1">
    <option value="">Select</option>
      <option value="image">Image</option>
      <option value="video">Video</option>
      <option value="url">URL</option>
      <option value="resource">File/Document</option>
    </select>

    <div class="var_html">
    </div>

   

        <label for="helpup_title" class="col-sm-12 col-form-label mb-3">Title</label>
        <input type="text" aria-label="title" name="inputg2[]" class="form-control input_value" placeholder="Title" id="helpup_title">

        <label for="helpuploadshort" class="col-sm-12 col-form-label mb-3">Short Desc</label>
        <textarea class="form-control input_value" id="helpuploadshort" rows="3" name="textareag1"></textarea>

        
    </div>
    <div class="col-sm-2 mb-3">
    <button class="btn btn-danger member-del">
    <i class="fa-solid fa-minus"></i>
  </button>
    </div>
    <hr>
    </div>`;
    $(".each_help_container").prepend(help_container_html);
    // $(".each_help_container").find('.each-form-set .inp-sec-1').hide();
    // $(".each_help_container").find('.each-form-set .inp-sec-2').hide();
    }
    else{
      $(myToastEl).find(".toast-body").html('Please upload a requried details');
      myToast.show();
    }
    
    
});
$(document)
.on("click", ".help_container .member-add", function (e) {
  e.preventDefault();

  
})
.on("click", ".help_container .each-form-set .member-del", function (e) {
  e.preventDefault();
  $(this).closest(".each-form-set").remove();
  return false;
});
//help ends


  //add gallery
  $(document)
.on("click", ".gallery_container .member-add", function (e) {
  e.preventDefault();
    var galleryinput_value = $(".gallery_container .input_value");
    var is_galleryinput_value_empty = false;
    for (var i = 0; i < galleryinput_value.length; i++) {
      if($(galleryinput_value[i]).val() === ""){
        is_galleryinput_value_empty = true;
      }
     
    }
    if(is_galleryinput_value_empty === false){
  var gallery_container_html =
  `<div class="row each-form-set mb-3">

  <div class="col-sm-10 mb-3">
    
    <label for="uploadThumb_file" class="col-sm-12 col-form-label mb-3">Type</label>
    <select class="form-select" aria-label="Type" name="typeg1">
      <option value="1">Image</option>
    </select>

    
    <label for="formFile" class="col-sm-12 col-form-label mb-3">Upload Thumb</label>
    <input class="form-control input_value file_uploader" type="file" id="formFile" name="gallery_files[]">
  

        <label for="uploadtitle" class="col-sm-12 col-form-label mb-3">Title</label>
        <input type="text" aria-label="title" name="inputg2[]" class="form-control input_value" placeholder="Title" id="uploadtitle">

       
    </div>
    <div class="col-sm-2 mb-3">
    <button class="btn btn-danger member-del">
    <i class="fa-solid fa-minus"></i>
  </button>
    </div>
    <hr>
    </div>`;
    $(".each_gallery_container").prepend(gallery_container_html);
      
    }
    else{
      $(myToastEl).find(".toast-body").html('Please upload a image & title');
      myToast.show();
    }
    
    
});
$(document)
.on("click", ".gallery_container .member-add", function (e) {
  e.preventDefault();

  
})
.on("click", ".gallery_container .each-form-set .member-del", function (e) {
  e.preventDefault();
  $(this).closest(".each-form-set").remove();
  return false;
});
//add sponsor members end
  //gallery ends

  //end ready function

  //Form Validation Start

  function checkvalidation() {
    //alert('hello');
    var isperfect = true;
    var info = "";
    var objdata = { isperfect: "", info: "" };

    //check field validations here
    //Basic Details
    var fs_title = $("#fd-title").val();
    if (fs_title === "") {
      info += "Please enter the title<br>";
      isperfect = false;
    }
    var fs_title = $("#fd-slug").val();
    if (fs_title === "") {
      info += "Please enter the URL Slug<br>";
      isperfect = false;
    }
    var fs_ext = $("#fd-excerpt").val();
    if (fs_ext === "") {
      info += "Please fill the Excerpt with max 360 words<br>";
      isperfect = false;
    }

    var fileInput = $("#uploadimg1").val();
    // Allowing file type
    var allowedExtensions =
      /(\.png|\jpe?g|\.odt|\.pdf|\.tex|\.txt|\.rtf|\.wps|\.docx|\.doc)$/i;
    if (fileInput === "") {
      info += "Please upload a the image<br>";
      isperfect = false;
    } else if (!allowedExtensions.exec(fileInput)) {
      info += "Please upload a valid file<br>";
      isperfect = false;
    }

    var select_role = document.getElementById("languagesecc");
    if (select_role.selectedIndex <= 0) {
      info += "Please Select Language<br>";
      isperfect = false;
    }
    //Meta1 Details
    var mfd_title = $("#mfd-title").val();
    if (mfd_title === "") {
      info += "Please enter the Meta title<br>";
      isperfect = false;
    }
    var mfd_exc = $("#mfd-excerpt").val();
    if (mfd_exc === "") {
      info += "Please enter the Meta description<br>";
      isperfect = false;
    }
    var fileInput = $("#mformFile-meta1").val();
    // Allowing file type
    var allowedExtensions =
      /(\.png|\jpe?g|\.odt|\.pdf|\.tex|\.txt|\.rtf|\.wps|\.docx|\.doc)$/i;
    if (fileInput === "") {
      info += "Please upload Meta Image<br>";
      isperfect = false;
    } else if (!allowedExtensions.exec(fileInput)) {
      info += "Please upload a valid field for Meta Image<br>";
      isperfect = false;
    }

    //Main Details
    var fd_mainexp = $("#fd-explore-link").val();
    if (fd_mainexp === "") {
      info += "Please enter Explore Link<br>";
      isperfect = false;
    }
   
    var fileInput = $("#formFile-main-download").val();
    // Allowing file type
    var allowedExtensions = /(\.zip)$/i;
    if (fileInput === "") {
      info += "Please upload Zip file for download<br>";
      isperfect = false;
    } else if (!allowedExtensions.exec(fileInput)) {
      info += "Please upload zip file for download<br>";
      isperfect = false;
    }
    
    var select_lang2 = document.getElementById("languagesecc3");
    if($(select_lang2).length){
    if (select_lang2.selectedIndex <=0) {
          info += "Please Select Language <br>";
          isperfect = false;
    }  
  }
  ////If langauge required////
  // else{
  //   info += "Please Select Language English<br>";
  //   isperfect = false;
  // }

      var lang_input_value = $(".lang_container .input_value");
      var is_lang_input_value_empty = false;
      for (var i = 0; i < lang_input_value.length; i++) {
        if($(lang_input_value[i]).val() === ""){
          is_lang_input_value_empty = true;

          info += "Please add URL for Article Language Option<br>";
          isperfect = false;
        }
      }

      var help_img_uploader = $(".help_container .input_value.file_uploader");
      var is_help_img_uploader_empty = false;
      let allowedExtensions2 =
          /(\.png|\jpe?g|\.odt|\.pdf|\.tex|\.txt|\.rtf|\.wps|\.docx|\.doc)$/i;
          
      for (var i = 0; i < help_img_uploader.length; i++) {
        let each_help_img_uploader = $(help_img_uploader[i]).val();
        //alert(each_help_img_uploader);
        if(each_help_img_uploader === ""){
          is_help_img_uploader_empty = true;
  
          info += "Please upload a file in Help section Image<br>";
          isperfect = false;
        }else if (!allowedExtensions2.exec(each_help_img_uploader)) {
          info += "Please upload a valid file Extension in Help Section<br>";
          isperfect = false;
  
        }
      }

      var help_input_value = $(".help_container .input_value");
      var is_help_input_value_empty = false;
      for (var i = 0; i < help_input_value.length; i++) {
        if($(help_input_value[i]).val() === ""){
          is_help_input_value_empty = true;

          info += "Please enter data for Help Section<br>";
          isperfect = false;
        }
      }





      var gallery_uploader = $(".gallery_container .input_value.file_uploader");
      var is_gallery_uploader_empty = false;
      let allowedExtensions4 =
          /(\.png|\jpe?g|\.odt|\.pdf|\.tex|\.txt|\.rtf|\.wps|\.docx|\.doc)$/i;
          
      for (var i = 0; i < gallery_uploader.length; i++) {
        let each_img_uploader = $(gallery_uploader[i]).val();
        //alert(each_help_img_uploader);
        if(each_img_uploader === ""){
          is_gallery_uploader_empty = true;
  
          info += "Please upload a file in Gallery section Image<br>";
          isperfect = false;
        }else if (!allowedExtensions4.exec(each_img_uploader)) {
          info += "Please upload a valid file Extension in Gallery Section<br>";
          isperfect = false;
  
        }
      }

      var resgallery_input_value = $(".gallery_container .input_value");
      var is_resgallery_input_value_empty = false;
      for (var i = 0; i < resgallery_input_value.length; i++) {
        if($(resgallery_input_value[i]).val() === ""){
          is_resgallery_input_value_empty = true;

          info += "Please enter data for Gallery Section<br>";
          isperfect = false;
        }
      }

      var sponsors_uploader = $(".sponsor_container .input_value.file_uploader");
      var is_sponsors_uploader_empty = false;
      let allowedExtensions6 =
          /(\.png|\jpe?g|\.odt|\.pdf|\.tex|\.txt|\.rtf|\.wps|\.docx|\.doc)$/i;
          
      for (var i = 0; i < sponsors_uploader.length; i++) {
        let speach_img_uploader = $(sponsors_uploader[i]).val();
        //alert(each_help_img_uploader);
        if(speach_img_uploader === ""){
          is_sponsors_uploader_empty = true;
          info += "Please upload a file in Sponsors section Image<br>";
          isperfect = false;
        }else if (!allowedExtensions6.exec(speach_img_uploader)) {
          info += "Please upload a valid file Extension in Sponsors Section<br>";
          isperfect = false;
  
        }
      }


      var team_input_value = $(".team_container .input_value");
      var is_team_input_value_empty = false;
      for (var i = 0; i < team_input_value.length; i++) {
        if($(team_input_value[i]).val() === ""){
          is_team_input_value_empty = true;

          info += "Please enter Team Member Name & Role<br>";
          isperfect = false;
        }
      }

      var sponn_input_value = $(".sponsor_container .input_value");
      var is_sponn_input_value_empty = false;
      for (var i = 0; i < sponn_input_value.length; i++) {
        if($(sponn_input_value[i]).val() === ""){
          is_sponn_input_value_empty = true;

          info += "Please enter Sponsors details<br>";
          isperfect = false;
        }
      }


    var select_lang = document.getElementById("languagesecc2");
    if (select_lang.selectedIndex <=0) {
          info += "Please Select Article Language<br>";
          isperfect = false;
    }
    var select_subj = document.getElementById("articlesubject");
    if (select_subj.selectedIndex <=0) {
          info += "Please Select Subject<br>";
          isperfect = false;
    }

    var select_topic = document.getElementById("articletopics");
    if (select_topic.selectedIndex <=0) {
          info += "Please Select Topics<br>";
          isperfect = false;
    }
    var select_projects = document.getElementById("articleprojects");
    if (select_projects.selectedIndex <=0) {
          info += "Please Select Projects<br>";
          isperfect = false;
    }
    var select_hour = document.getElementById("selecthours");
    if (select_hour.selectedIndex <=0) {
          info += "Please Select Hour<br>";
          isperfect = false;
    }
    var select_mins = document.getElementById("selectmins");
    if (select_mins.selectedIndex <=0) {
          info += "Please Select Mins<br>";
          isperfect = false;
    }
    var text_cops= $("#copyrightlicc").val();
    if (text_cops === "") {
      info += "Please Fill Copyrights details<br>";
      isperfect = false;
    }
    
    //Plus Fields Validation
    // var helpthumbImage = $("#help_thumbimg").val();
    // var allowedExtensions =
    //   /(\.png|\jpe?g|\.odt|\.pdf|\.tex|\.txt|\.rtf|\.wps|\.docx|\.doc)$/i;
    //   if( $(helpthumbImage).length === 0) {
        
    //     if(!allowedExtensions.exec(helpthumbImage)) {
    //       info += "Please upload  a valid format Purnima<br>";
    //       alert('working')
    //   }
    // }
    //   else if(helpthumbImage === "") {
    //     alert('hes')
    //     info += "Please upload a thumb image<br>";
    //     isperfect = true;
    //  }
        
    //check field validation ends

    objdata.isperfect = isperfect;
    objdata.info = info;
    //checkvalidation function ends

    return objdata;
  }
  $("#cms_form").submit(function (e) {
    e.preventDefault();
    $("#cms_form .form-control").removeClass("is-invalid");
    var validData = checkvalidation();
    if (validData.isperfect === false) {
      // alert(validData.info);
      // console.log('Hello');
      var html_alert_content =
        `<div class="alert alert-danger d-flex align-items-center" role="alert">
                                      <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Danger:"><use xlink:href="#exclamation-triangle-fill"/></svg>
                                      <div class="alert-content">
                                      `+validData.info +`
                                      </div>
                                    </div>`;
      $(".alerts-container").html(html_alert_content);
      $(myToastEl).find(".toast-body").html(validData.info);
      myToast.show();
      // $(".form-control").addClass("is-invalid");
    }
   
    
   //Bootstrap error validation 
      var form_validate = $("#cms_form .form-control");
     
      var is_form_validate_empty = true;
      for (var i = 0; i < form_validate.length; i++) {
        if($(form_validate[i]).val() === ""){
          is_form_validate_empty = true;
          $(form_validate[i]).addClass("is-invalid");
          console.log('meee')
        }
        else{
          $(form_validate[i]).removeClass("is-invalid");
        }
        
      }

  });

  var myToastEl = document.getElementById("myToastEl");
  var myToast = bootstrap.Toast.getOrCreateInstance(myToastEl); // Returns a Bootstrap toast instance
 

  // CK Editor 
  
  // ClassicEditor
  // .create( document.querySelector( '#editor' ) )
  // .catch( error => {
  //     console.error( error );
  // } );

  var myEditor;

// CKeditor
      // This sample still does not showcase all CKEditor 5 features (!)
          // Visit https://ckeditor.com/docs/ckeditor5/latest/features/index.html to browse all the features.
          CKEDITOR.ClassicEditor.create(document.getElementById("editor"), {
            // https://ckeditor.com/docs/ckeditor5/latest/features/toolbar/toolbar.html#extended-toolbar-configuration-format
            toolbar: {
                items: [
                "heading",
                "|",
                        "bold",
                        "italic",
                        "link",
                        "bulletedList",
                        "numberedList",
                        "|",
                        "indent",
                        "outdent",
                        "|",
                        "imageUpload",
                        "blockQuote",
                        "mediaEmbed",
                        "undo",
                        "redo",
                        "sourceEditing",
                ],
                shouldNotGroupWhenFull: true
            },
            // Changing the language of the interface requires loading the language file using the <script> tag.
            // language: 'es',
            list: {
                properties: {
                    styles: false,
                    startIndex: true,
                    reversed: true
                }
            },
            // https://ckeditor.com/docs/ckeditor5/latest/features/headings.html#configuration
            heading: {
                options: [
                    { model: 'paragraph', title: 'Paragraph', class: 'ck-heading_paragraph' },
                    { model: 'heading1', view: 'h1', title: 'Heading 1', class: 'ck-heading_heading1' },
                    { model: 'heading2', view: 'h2', title: 'Heading 2', class: 'ck-heading_heading2' },
                    { model: 'heading3', view: 'h3', title: 'Heading 3', class: 'ck-heading_heading3' },
                    { model: 'heading4', view: 'h4', title: 'Heading 4', class: 'ck-heading_heading4' },
                    { model: 'heading5', view: 'h5', title: 'Heading 5', class: 'ck-heading_heading5' },
                    { model: 'heading6', view: 'h6', title: 'Heading 6', class: 'ck-heading_heading6' }
                ]
            },
            // https://ckeditor.com/docs/ckeditor5/latest/features/editor-placeholder.html#using-the-editor-configuration
            placeholder: 'Your detail content here',
            // https://ckeditor.com/docs/ckeditor5/latest/features/font.html#configuring-the-font-family-feature
            fontFamily: {
                options: [
                    'default',
                    // 'Arial, Helvetica, sans-serif',
                    // 'Courier New, Courier, monospace',
                    // 'Georgia, serif',
                    // 'Lucida Sans Unicode, Lucida Grande, sans-serif',
                    // 'Tahoma, Geneva, sans-serif',
                    // 'Times New Roman, Times, serif',
                    // 'Trebuchet MS, Helvetica, sans-serif',
                    // 'Verdana, Geneva, sans-serif'
                ],
                supportAllValues: true
            },
            // https://ckeditor.com/docs/ckeditor5/latest/features/font.html#configuring-the-font-size-feature
            fontSize: {
                options: [ 10, 12, 14, 'default', 18, 20, 22 ],
                supportAllValues: true
            },
            // Be careful with the setting below. It instructs CKEditor to accept ALL HTML markup.
            // https://ckeditor.com/docs/ckeditor5/latest/features/general-html-support.html#enabling-all-html-features
            htmlSupport: {
                allow: [
                    {
                        name: /.*/,
                        attributes: true,
                        classes: true,
                        styles: true
                    }
                ]
            },
            // Be careful with enabling previews
            // https://ckeditor.com/docs/ckeditor5/latest/features/html-embed.html#content-previews
            htmlEmbed: {
                showPreviews: true
            },
            // https://ckeditor.com/docs/ckeditor5/latest/features/link.html#custom-link-attributes-decorators
            link: {
                decorators: {
                    addTargetToExternalLinks: true,
                    defaultProtocol: 'https://',
                    toggleDownloadable: {
                        mode: 'manual',
                        label: 'Downloadable',
                        attributes: {
                            download: 'file'
                        }
                    }
                }
            },
            // https://ckeditor.com/docs/ckeditor5/latest/features/mentions.html#configuration
            mention: {
                feeds: [
                    {
                        marker: '@',
                        feed: [
                            '@apple', '@bears', '@brownie', '@cake', '@cake', '@candy', '@canes', '@chocolate', '@cookie', '@cotton', '@cream',
                            '@cupcake', '@danish', '@donut', '@dragÃ©e', '@fruitcake', '@gingerbread', '@gummi', '@ice', '@jelly-o',
                            '@liquorice', '@macaroon', '@marzipan', '@oat', '@pie', '@plum', '@pudding', '@sesame', '@snaps', '@soufflÃ©',
                            '@sugar', '@sweet', '@topping', '@wafer'
                        ],
                        minimumCharacters: 1
                    }
                ]
            },
            // The "super-build" contains more premium features that require additional configuration, disable them below.
            // Do not turn them on unless you read the documentation and know how to configure them and setup the editor.
            removePlugins: [
                // These two are commercial, but you can try them out without registering to a trial.
                // 'ExportPdf',
                // 'ExportWord',
                'CKBox',
                'CKFinder',
                'EasyImage',
                // This sample uses the Base64UploadAdapter to handle image uploads as it requires no configuration.
                // https://ckeditor.com/docs/ckeditor5/latest/features/images/image-upload/base64-upload-adapter.html
                // Storing images as Base64 is usually a very bad idea.
                // Replace it on production website with other solutions:
                // https://ckeditor.com/docs/ckeditor5/latest/features/images/image-upload/image-upload.html
                // 'Base64UploadAdapter',
                'RealTimeCollaborativeComments',
                'RealTimeCollaborativeTrackChanges',
                'RealTimeCollaborativeRevisionHistory',
                'PresenceList',
                'Comments',
                'TrackChanges',
                'TrackChangesData',
                'RevisionHistory',
                'Pagination',
                'WProofreader',
                // Careful, with the Mathtype plugin CKEditor will not load when loading this sample
                // from a local file system (file://) - load this site via HTTP server if you enable MathType
                'MathType'
            ]
        }).then( editor => {
          console.log( 'Editor was initialized', editor );
          myEditor = editor;
      } )
      .catch( err => {
          console.error( err.stack );
      } );

      $('#getdata').on('click',function(){
        console.log(myEditor.getData());
      });

     // $('textarea#editor').ckeditor().myEditor.insertHtml('<a href="#">text</a>');

        $('#getdata').on('click',function(){
          console.log(myEditor.getData());
        });

       // $('textarea#editor').ckeditor().myEditor.insertHtml('<a href="#">text</a>');

      
        $("#dataelement").click(function () {
          insertAtCaret('ananr');
            });
      
      function insertAtCaret(myValue) {
        var hvla = ` <div class="ratio ratio-16x9">
        <iframe src="https://www.youtube.com/embed/zpOULjyy-n8?rel=0" title="YouTube video" allowfullscreen></iframe>
      </div>`;
        //for raw html
        //myEditor.execute( 'htmlEmbed', hvla );

        const content = '<p>A paragraph with <a href="https://ckeditor.com">some link</a>.';
        const viewFragment = myEditor.data.processor.toView( content );
        const modelFragment = myEditor.data.toModel( viewFragment );
        
        myEditor.model.insertContent( modelFragment );

    };
    

  

});



   