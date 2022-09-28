$(document).ready(function () {
    $("#fd-excerpt").textcounter({
      max: 15,
      stopInputAtMaximum: false,
      countDownText: "%d characters remaining",
    });
    //tags - multiselct
    $(".tagsInput, .multipleSelect").fastselect();
  
    //date picker demo
    //$('#datepicker').datepicker('setDate', 'now');
    //var date = new Date();
    //   var today = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    //   var end = new Date(date.getFullYear(), date.getMonth(), date.getDate());
    $(".datepicker").datepicker({
      format: "dd/mm/yyyy",
      todayHighlight: true,
    });
    $(".datepicker").datepicker("setDate", "now");
  
     //replicate content to other text-field 

     $("#age_bstitle").on('keyup',function(event) {
      var stt = $(this).val();
      $("#age_meta_title").val(stt);
    });
   
  
    //Add Content Available Langauge
    $(document)
  .on("click", ".age_lang_container .add_lgn_btn", function (e) {
    e.preventDefault();
    // alert('hi');
      var blanginput_value = $(".age_lang_container .input_value");
      var is_blanginput_value_empty = false;
      for (var i = 0; i < blanginput_value.length; i++) {
        if($(blanginput_value[i]).val() === ""){
          is_blanginput_value_empty = true;
        }
       
      }
      if(is_blanginput_value_empty === false){
    var age_lang_container_html =
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
                 <label for="blog_langurl" class="form-label">URL</label> <span class="text-danger">*</span>
                 <input type="text" class="form-control input_value" id="blog_langurl" placeholder="URL">
               </div>
         </div>
     
     <div class="col-sm-2">
         <button class="btn btn-danger member-del">
           <i class="fa-solid fa-minus"></i>
         </button>
         </div>
     </div>`;
      $(".age_lang_url_container").prepend(age_lang_container_html);
        
      }
      else{
        $(myToastEl).find(".toast-body").html('Please select a Language');
        myToast.show();
      }
      
      
  });
  $(document)
  .on("click", ".age_lang_container .add_lgn_btn", function (e) {
    e.preventDefault();
  
    
  })
  .on("click", ".langbx .member-del", function (e) {
    e.preventDefault();
    $(this).closest(".langbx").remove();
    return false;
  });
  //Add Content Available Langauge
   
    
  
  
  
    //add gallery
    $(document)
  .on("click", ".age_gallery_container  .member-add", function (e) {
    e.preventDefault();
      var agegalleryinput_value = $(".age_gallery_container .input_value");
      var is_agegalleryinput_value_empty = false;
      for (var i = 0; i < agegalleryinput_value.length; i++) {
        if($(agegalleryinput_value[i]).val() === ""){
          is_agegalleryinput_value_empty = true;
        }
       
      }
      if(is_agegalleryinput_value_empty === false){
      var agegallery_container_html =
    `<div class="row each-form-set mb-3">
  
    <div class="col-sm-10 mb-3">
      
      <label for="uploadThumb_file" class="col-sm-12 col-form-label mb-3">Type</label>
      <select class="form-select" aria-label="Type" name="typeg1">
        <option value="1">Image</option>
        
      </select>
  
      
      <label for="gallery_files" class="col-sm-12 col-form-label mb-3">Upload Thumb</label>
      <input class="form-control input_value file_uploader" type="file" id="gallery_files" name="gallery_files">
    
      
      
  
          <label for="blog_uploadtitle" class="col-sm-12 col-form-label mb-3">Title</label>
          <input type="text" aria-label="title" name="inputg2[]" class="form-control input_value" placeholder="Title" id="blog_uploadtitle">
  
         
      </div>
      <div class="col-sm-2 mb-3">
      <button class="btn btn-danger member-del">
      <i class="fa-solid fa-minus"></i>
    </button>
      </div>
      <hr>
      </div>`;
      $(".age_gallerys_container").prepend(agegallery_container_html);
        
      }
      else{
        $(myToastEl).find(".toast-body").html('Please upload a image & title');
        myToast.show();
      }
      
      
  });
  $(document)
  .on("click", ".age_gallery_container .member-add", function (e) {
    e.preventDefault();
  
    
  })
  .on("click", ".age_gallery_container .member-del", function (e) {
    e.preventDefault();
    $(this).closest(".each-form-set").remove();
    return false;
  });
  
    //gallery ends
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
  
    //end ready function
  
    //Form Validation Start
  
    function checkvalidation() {
      //alert('hello');
      var isperfect = true;
      var info = "";
      var objdata = { isperfect: "", info: "" };
  
      //check field validations here
      //Basic Details
      var age_bstitle = $("#age_bstitle").val();
      if (age_bstitle === "") {
        info += "Please enter Title <br>";
        isperfect = false;
      }
      var age_url = $("#age_url").val();
      if (age_url === "") {
        info += "Please enter the URL Slug<br>";
        isperfect = false;
      }
      var age_excerpt = $("#age_excerpt").val();
      if (age_excerpt === "") {
        info += "Please fill the Excerpt with max 360 words<br>";
        isperfect = false;
      }

      var ageImage = $("#age_thumbimg").val();
      // Allowing file type
      var allowedExtensions =
        /(\.png|\jpe?g|\.odt|\.pdf|\.tex|\.txt|\.rtf|\.wps|\.docx|\.doc)$/i;
      if (ageImage === "") {
        info += "Please upload Thumb image<br>";
        isperfect = false;
      } else if (!allowedExtensions.exec(ageImage)) {
        info += "Please upload a valid thumb file<br>";
        isperfect = false;
      }
      
      var select_lang2 = document.getElementById("languagesecc");
      if (select_lang2.selectedIndex <=0) {
            info += "Please Select Language <br>";
            isperfect = false;
      }  
     
      var age_meta_title = $("#age_meta_title").val();
      if (age_meta_title === "") {
        info += "Please enter Meta Title<br>";
        isperfect = false;
      }

      var age_meta_title = $("#age_meta_excerpt").val();
      if (age_meta_title === "") {
        info += "Please enter Meta description Maximum 360 words<br>";
        isperfect = false;
      }
      

      var agemetaImage = $("#age_meta_img").val();
      // Allowing file type
      var allowedExtensions2 =
        /(\.png|\jpe?g|\.odt|\.pdf|\.tex|\.txt|\.rtf|\.wps|\.docx|\.doc)$/i;
      if (agemetaImage === "") {
        info += "Please upload Meta Thumb image<br>";
        isperfect = false;
      } else if (!allowedExtensions2.exec(agemetaImage)) {
        info += "Please upload a valid Meta thumb file<br>";
        isperfect = false;
      }

      var age_mainexplore_link = $("#age_mainexplore_link").val();
      if (age_mainexplore_link === "") {
        info += "Please enter Explore Link<br>";
        isperfect = false;
      }

        var fileInput = $("#age_zipfile").val();
        // Allowing file type
        var allowedExtensions3 = /(\.zip)$/i;
        if (fileInput === "") {
        info += "Please upload a file for download<br>";
        isperfect = false;
        } else if (!allowedExtensions3.exec(fileInput)) {
        info += "Please upload zip file for download<br>";
        isperfect = false;
        }

      //Add Button fileds Validation start
      var agalleryinput_value = $(".age_lang_container .input_value");
      var is_agalleryinput_value_empty = false;
      for (var i = 0; i < agalleryinput_value.length; i++) {
        if($(agalleryinput_value[i]).val() === ""){
          is_agalleryinput_value_empty = true;
  
          info += "Please fill the added fileds for Content Section<br>";
          isperfect = false;
        }
      }

      var a_galleryinput_value = $(".age_gallery_container .input_value");
      var is_a_galleryinput_value_empty = false;
      for (var i = 0; i < a_galleryinput_value.length; i++) {
        if($(a_galleryinput_value[i]).val() === ""){
          is_a_galleryinput_value_empty = true;
  
          info += "Please fill the added fileds for Gallery Section<br>";
          isperfect = false;
        }
      }

      var role_input_value = $(".team_container .input_value");
      var is_role_input_value_empty = false;
      for (var i = 0; i < role_input_value.length; i++) {
        if($(role_input_value[i]).val() === ""){
          is_role_input_value_empty = true;
  
          info += "Add Team Members<br>";
          isperfect = false;
        }
      }

      var sp_input_value = $(".sponsor_container .input_value");
      var is_sp_input_value_empty = false;
      for (var i = 0; i < sp_input_value.length; i++) {
        if($(sp_input_value[i]).val() === ""){
          is_sp_input_value_empty = true;
  
          info += "Add Sponsor Image & Title<br>";
          isperfect = false;
        }
      }

    var age_gallery_file_uploader = $(".age_gallery_container .input_value.file_uploader");
    var is_age_gallery_file_uploader_empty = false;
    let allowedExtensions4 =
        /(\.png|\jpe?g|\.odt|\.pdf|\.tex|\.txt|\.rtf|\.wps|\.docx|\.doc)$/i;
        
    for (var i = 0; i < age_gallery_file_uploader.length; i++) {
      let each_age_gallery_file_uploader = $(age_gallery_file_uploader[i]).val();
      //alert(each_bgallery_file_uploader);
      if(each_age_gallery_file_uploader === ""){
        is_age_gallery_file_uploader_empty = true;

        info += "Please upload a file in Image Gallery<br>";
        isperfect = false;
      }else if (!allowedExtensions4.exec(each_age_gallery_file_uploader)) {
        info += "Please upload a valid file Extension in image Gallery<br>";
        isperfect = false;

      }
    }

    var sp_file_uploader = $(".sponsor_container .input_value.file_uploader");
    var is_sp_file_uploader_empty = false;
    let allowedExtensions5 =
        /(\.png|\jpe?g|\.odt|\.pdf|\.tex|\.txt|\.rtf|\.wps|\.docx|\.doc)$/i;
        
    for (var i = 0; i < sp_file_uploader.length; i++) {
      let spo_file_uploader = $(sp_file_uploader[i]).val();
      //alert(each_bgallery_file_uploader);
      if(spo_file_uploader === ""){
        is_sp_file_uploader_empty = true;

        info += "Please upload a file for Sponsors<br>";
        isperfect = false;
      }else if (!allowedExtensions5.exec(spo_file_uploader)) {
        info += "Please upload a valid file Extension for Sponsors<br>";
        isperfect = false;

      }
     
    }

        //Add Button fileds Validation end

     var age_subject = document.getElementById("age_subject");
      if (age_subject.selectedIndex <=0) {
            info += "Please Select Subject <br>";
            isperfect = false;
      }

      var age_topics = document.getElementById("age_topics");
      if (age_topics.selectedIndex <=0) {
            info += "Please Select Topics <br>";
            isperfect = false;
      }

      var age_projects = document.getElementById("age_projects");
      if (age_projects.selectedIndex <=0) {
            info += "Please Select Topics <br>";
            isperfect = false;
      }


    var age_hour = document.getElementById("age_hours");
    if (age_hour.selectedIndex <=0) {
          info += "Please Select Hour<br>";
          isperfect = false;
    }
    var age_mins = document.getElementById("age_mins");
    if (age_mins.selectedIndex <=0) {
          info += "Please Select Mins<br>";
          isperfect = false;
    }

     var created_by = $("#created_by").val();
      if (created_by === "") {
        info += "Please enter the Person Name Cretaed By<br>";
        isperfect = false;
      }

      var copyrightlicc = $("#copyrightlicc").val();
      if (copyrightlicc === "") {
        info += "Please enter Copyrights/Licence details<br>";
        isperfect = false;
      }


      //check field validation ends
  
      objdata.isperfect = isperfect;
      objdata.info = info;
      //checkvalidation function ends
  
      return objdata;
    }
    $("#guessmyage_cms_form").submit(function (e) {
      e.preventDefault();
      $("#guessmyage_cms_form .form-control").removeClass("is-invalid");
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
        var form_validate = $("#guessmyage_cms_form .form-control");
       
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
  
          alert('hi');
      };
      
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
  
        alert('hi');
    };
    
  
  });
  
  
  