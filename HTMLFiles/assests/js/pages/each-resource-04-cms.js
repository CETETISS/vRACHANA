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

    $("#res4_title").on('keyup',function(event) {
      var stt = $(this).val();
      $("#res4_meta_title").val(stt);
    });
   
  
    //Add Content Available Langauge
    $(document)
  .on("click", ".res4_lang_container .add_lgn_btn", function (e) {
    e.preventDefault();
    // alert('hi');
      var re4langinput_value = $(".res4_lang_container .input_value");
      var is_re4langinput_value_empty = false;
      for (var i = 0; i < re4langinput_value.length; i++) {
        if($(re4langinput_value[i]).val() === ""){
          is_re4langinput_value_empty = true;
        }
       
      }
      if(is_re4langinput_value_empty === false){
    var blang_container_html =
      `  <div class="row langbx">
                           
      <div class="col-sm-10">
         <div class="mb-3">
             <label for="eventlanguage2" class="form-label">Article Language<span class="text-danger">*</span> </label>
             <select class="form-select form-control input_value" aria-label="Default select example" id="eventlanguage2">
               <option value="">Open this select menu</option>
               <option value="1">English</option>
               <option value="3">Hindi</option>
               <option value="2">Urdu</option>
               <option value="3">Marthi</option>
             </select>
             </div>
             <div class="mb-3">
                 <label for="event_url2" class="form-label">URL</label> <span class="text-danger">*</span>
                 <input type="text" class="form-control input_value" id="event_url2" placeholder="URL">
               </div>
         </div>
     
     <div class="col-sm-2">
         <button class="btn btn-danger member-del">
           <i class="fa-solid fa-minus"></i>
         </button>
         </div>
     </div>`;
      $(".res4_lang_url_container").prepend(blang_container_html);
        
      }
      else{
        $(myToastEl).find(".toast-body").html('Please select a Language');
        myToast.show();
      }
      
      
  });
  $(document)
  .on("click", ".res4_lang_url_container .add_lgn_btn", function (e) {
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
  .on("click", ".res4_gallery_container  .member-add", function (e) {
    e.preventDefault();
      var res4galleryinput_value = $(".res4_gallery_container .input_value");
      var is_res4galleryinput_value_empty = false;
      for (var i = 0; i < res4galleryinput_value.length; i++) {
        if($(res4galleryinput_value[i]).val() === ""){
          is_res4galleryinput_value_empty = true;
        }
       
      }
      if(is_res4galleryinput_value_empty === false){
    var res4galleryinput_html =
    `<div class="row each-form-set mb-3">
  
    <div class="col-sm-10 mb-3">
      
      <label for="gallery_select" class="col-sm-12 col-form-label mb-3">Type</label>
      <select class="form-select" aria-label="Type" name="typeg1" id="gallery_select">
        <option value="1">Image</option>
        <option value="2">Video</option>
        <option value="3">URL</option>
        <option value="3">File/Document</option>
      </select>
  
      
      <label for="galleryimage" class="col-sm-12 col-form-label mb-3">Upload Thumb</label>
      <input class="form-control input_value file_uploader" type="file" id="galleryimage" name="gallery_files[]">
    
      
        <label for="gallery_url" class="col-form-label mb-3">URL</label> <span class="text-secondary fst-italic txt-sm-85">(* If content is of type url or youtube video link is provided)</span>
          <input type="text" aria-label="Sponsor title" name="inputg3[]" id="gallery_url" class="form-control input_value col-sm-12" placeholder="Desc or URL link">
  
          <label for="galleryuploadtitle" class="col-sm-12 col-form-label mb-3">Title</label>
          <input type="text" aria-label="title" name="inputg2[]" class="form-control input_value" placeholder="Title" id="galleryuploadtitle">
  
         
      </div>
      <div class="col-sm-2 mb-3">
      <button class="btn btn-danger member-del">
      <i class="fa-solid fa-minus"></i>
    </button>
      </div>
      <hr>
      </div>`;
      $(".res4_each_gallery_container").prepend(res4galleryinput_html);
        
      }
      else{
        $(myToastEl).find(".toast-body").html('Please upload a image & title');
        myToast.show();
      }
      
      
  });
  $(document)
  .on("click", ".res4_gallery_container .member-add", function (e) {
    e.preventDefault();
  
    
  })
  .on("click", "res4_gallery_container .each-form-set .member-del", function (e) {
    e.preventDefault();
    $(this).closest(".each-form-set").remove();
    return false;
  });
  //add sponsor members end
    //gallery ends
  
    //end ready function
  
   
  
//check_type
$(document)
.on("change", ".res4_help_container .check_type", function (e) {
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
//Help Container Start
$(document)
.on("click", ".res4_help_container .member-add", function (e) {
  e.preventDefault();
  // alert('hi');
    var re4_helpinput_value = $(".res4_help_container .input_value");
    var is_re4_helpinput_value_empty = false;
    for (var i = 0; i < re4_helpinput_value.length; i++) {
      if($(re4_helpinput_value[i]).val() === ""){
        is_re4_helpinput_value_empty = true;
      }
     
    }
    if(is_re4_helpinput_value_empty === false){
  var re4help_container_html =
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
    $(".res4_each_help_container").prepend(re4help_container_html);
      
    }
    else{
      $(myToastEl).find(".toast-body").html('Please upload a image & title');
      myToast.show();
    }
    
    
});
$(document)
.on("click", ".res4_each_help_container .member-add", function (e) {
  e.preventDefault();

  
})
.on("click", ".res4_each_help_container .each-form-set .member-del", function (e) {
  e.preventDefault();
  $(this).closest(".each-form-set").remove();
  return false;
});

//Help Container End

 //Form Validation Start
    function checkvalidation() {
      //alert('hello');
      var isperfect = true;
      var info = "";
      var objdata = { isperfect: "", info: "" };
  
      //check field validations here
      //Basic Details
      var res4_title = $("#res4_title").val();
      if (res4_title === "") {
        info += "Please enter title<br>";
        isperfect = false;
      }
      var res_url = $("#res4_slug").val();
      if (res_url === "") {
        info += "Please enter URL Slug<br>";
        isperfect = false;
      }
      var res4_excerpt = $("#res4_excerpt").val();
      if (res4_excerpt === "") {
        info += "Please fill the Excerpt with max 360 words<br>";
        isperfect = false;
      }

      var resImage = $("#res4_thumbimg").val();
      // Allowing file type
      var allowedExtensions =
        /(\.png|\jpe?g|\.odt|\.pdf|\.tex|\.txt|\.rtf|\.wps|\.docx|\.doc)$/i;
      if (resImage === "") {
        info += "Please upload a the image<br>";
        isperfect = false;
      } else if (!allowedExtensions.exec(resImage)) {
        info += "Please upload a valid file<br>";
        isperfect = false;
      }

      var select_lang = document.getElementById("languagesecc");
      if (select_lang.selectedIndex <=0) {
        info += "Please Select Language <br>";
        isperfect = false;
      } 
      
    //Meta1 Details
      var res4_meta_title = $("#res4_meta_title").val();
      if (res4_meta_title === "") {
        info += "Please enter the Meta title<br>";
        isperfect = false;
      }
      var res4_meta_excerpt = $("#res4_meta_excerpt").val();
      if (res4_meta_excerpt === "") {
        info += "Please enter the Meta description<br>";
        isperfect = false;
      }
      var fileInput = $("#res4_meta_image").val();
      // Allowing file type
      var allowedExtensions12 =
        /(\.png|\jpe?g|\.odt|\.pdf|\.tex|\.txt|\.rtf|\.wps|\.docx|\.doc)$/i;
      if (fileInput === "") {
        info += "Please upload Meta Image<br>";
        isperfect = false;
      } else if (!allowedExtensions12.exec(fileInput)) {
        info += "Please upload a valid field for Meta Image<br>";
        isperfect = false;
      }

      var res4_hardcopy = $("#res4_hardcopy").val();
      if (res4_hardcopy === "") {
        info += "Please enter Author<br>";
        isperfect = false;
      }

      var res4_zip = $("#res4_zip").val();
      // Allowing file type
      var allowedExtensions3 = /(\.zip)$/i;
      if (res4_zip === "") {
      info += "Please upload a file for download<br>";
      isperfect = false;
      } else if (!allowedExtensions3.exec(res4_zip)) {
      info += "Please upload zip file for download<br>";
      isperfect = false;
      }
     
      //Content Avaliable
      var rev_lang_input_value = $(".res4_lang_container .input_value");
      var is_rev_lang_input_value_empty = false;
      for (var i = 0; i < rev_lang_input_value.length; i++) {
        if($(rev_lang_input_value[i]).val() === ""){
          is_rev_lang_input_value_empty = true;
  
          info += "Please add URL for Article Language Option<br>";
          isperfect = false;
        }
       
      }
      

   //Help Material
    var helpinput_value = $(".res4_help_container .input_value");
    var is_helpinput_value_empty = false;
    for (var i = 0; i < helpinput_value.length; i++) {
      if($(helpinput_value[i]).val() === ""){
        is_helpinput_value_empty = true;

        info += "Please upload Help Section Details<br>";
        isperfect = false;
      }
     
    }

    var res4help_file_uploader = $(".res4_help_container .input_value.file_uploader");
    var is_res4help_file_uploader_empty = false;
    let allowedExtensions4 =
        /(\.png|\jpe?g|\.odt|\.pdf|\.tex|\.txt|\.rtf|\.wps|\.docx|\.doc)$/i;
        
    for (var i = 0; i < res4help_file_uploader.length; i++) {
      let each_res4help_file_uploader = $(res4help_file_uploader[i]).val();
      //alert(each_res4help_file_uploader);
      if(each_res4help_file_uploader === ""){
        is_res4help_file_uploader_empty = true;

        info += "Please upload a file in Help Section<br>";
        isperfect = false;
      }else if (!allowedExtensions4.exec(each_res4help_file_uploader)) {
        info += "Please upload a valid file Extension in Help Section<br>";
        isperfect = false;

      }
    }

    //Gallery Add
    var galleryinput_value = $(".res4_gallery_container .input_value");
    var is_galleryinput_value_empty = false;
    for (var i = 0; i < galleryinput_value.length; i++) {
      if($(galleryinput_value[i]).val() === ""){
        is_galleryinput_value_empty = true;

        info += "Please upload Gallery Details<br>";
        isperfect = false;
      }
     
    }

    var galleryinput_file_uploader = $(".res4_gallery_container .input_value.file_uploader");
    var is_galleryinput_file_uploader_empty = false;
    let allowedExtensions5 =
        /(\.png|\jpe?g|\.odt|\.pdf|\.tex|\.txt|\.rtf|\.wps|\.docx|\.doc)$/i;
        
    for (var i = 0; i < galleryinput_file_uploader.length; i++) {
      let each_res4_file_uploader = $(galleryinput_file_uploader[i]).val();
      //alert(each_res4help_file_uploader);
      if(each_res4_file_uploader === ""){
        is_galleryinput_file_uploader_empty = true;

        info += "Please upload a file in Gallery<br>";
        isperfect = false;
      }else if (!allowedExtensions5.exec(each_res4_file_uploader)) {
        info += "Please upload a valid file Extension in Help Section<br>";
        isperfect = false;

      }
    }
   
    //Right Sidebar//
    var res4subject = document.getElementById("res4subject");
      if (res4subject.selectedIndex <=0) {
        info += "Please Select Subject <br>";
        isperfect = false;
      } 
    
      var res4language = document.getElementById("res4language");
      if (res4language.selectedIndex <=0) {
        info += "Please Select Language <br>";
        isperfect = false;
      } 

      var res4topics = document.getElementById("res4topics");
      if (res4topics.selectedIndex <=0) {
        info += "Please Select Topics <br>";
        isperfect = false;
      } 

      var res4projects = document.getElementById("res4projects");
      if (res4projects.selectedIndex <=0) {
        info += "Please Select Topics <br>";
        isperfect = false;
      } 

      var created_by = $("#created_by").val();
      if (created_by === "") {
        info += "Please enter name of Created by<br>";
        isperfect = false;
      }
      
      var authour = $("#authour").val();
      if (authour === "") {
        info += "Please enter Author<br>";
        isperfect = false;
      }

      var published_by = $("#published").val();
      if (published_by === "") {
        info += "Please enter Published by<br>";
        isperfect = false;
      }
      
      var year_published = document.getElementById("selectYear");
      if (year_published.selectedIndex <=0) {
        info += "Please Select Year of Publication<br>";
        isperfect = false;
      }

      var res4_selecthour = document.getElementById("res4_selecthour");
      if (res4_selecthour.selectedIndex <=0) {
        info += "Please Select Estimates Hour<br>";
        isperfect = false;
      }
      
      var res4_selectmins = document.getElementById("res4_selectmins");
      if (res4_selectmins.selectedIndex <=0) {
        info += "Please Select Estimates Mins<br>";
        isperfect = false;
      }

    

      //check field validation ends
  
      objdata.isperfect = isperfect;
      objdata.info = info;
      //checkvalidation function ends
  
      return objdata;
    }
    $("#res4cms_form").submit(function (e) {
      e.preventDefault();
      $("#res4cms_form .form-control").removeClass("is-invalid");
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
        var form_validate = $("#res4cms_form .form-control");
       
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
  
  
  