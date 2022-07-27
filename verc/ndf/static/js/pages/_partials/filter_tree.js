$(document).ready(function(){

    function processFilters(){
        let url_str = '';
        // collect resources
        
        let resourceType_list = $("input[name='resourceType']:checked").map(function() {return this.value;}).get().join(',');
        
        if($.trim(resourceType_list.length) > 0) { 
            $("input[name='resources']").val(resourceType_list);
            url_str = "resources="+resourceType_list;
        };
        
        // collect subjects
        
        let subjects_list = $("input[name='domain']:checked").map(function() {return this.value;}).get().join(',');
        if($.trim(subjects_list.length) > 0) { 
            $("input[name='subjects']").val(subjects_list);
            if($.trim(url_str.length)> 0)
            {
                url_str = url_str + "&";
            }
            url_str = url_str + "subjects="+subjects_list;
        };

        //collect topics

        let topics_list = $("input[name='subdomain']:checked").map(function() {
            let pcontainer = $(this).parents();
            console.log(pcontainer);
            if(!pcontainer.closest('.has').find(" input[type='checkbox']").prop("checked")){
                return this.value;
            } 
            
        }).get().join(',');

        if($.trim(topics_list.length) > 0) { 
            $("input[name='subdomains']").val(topics_list);
            if($.trim(url_str.length)> 0)
            {
                url_str = url_str + "&";
            }
            url_str = url_str + "topics="+topics_list;
        };

        // collect grades
        
        let grades_list = $("input[name='grade']:checked").map(function() {return this.value;}).get().join(',');
        if($.trim(grades_list.length) > 0) { 
            $("input[name='grades']").val(grades_list);
            if($.trim(url_str.length)> 0)
            {
                url_str = url_str + "&";
            }
            url_str = url_str + "grades="+grades_list;
        };

        //project
        let projects_list = $("input[name='project']:checked").map(function() {return this.value;}).get().join(',');
        if($.trim(projects_list.length) > 0) { 
            $("input[name='projects']").val(projects_list);
            if($.trim(url_str.length)> 0)
            {
                url_str = url_str + "&";
            }
            url_str = url_str + "projects="+projects_list;
        };
        //projects

        //primary user
        let primaryUsers_list = $("input[name='primaryUser']:checked").map(function() {return this.value;}).get().join(',');
        if($.trim(primaryUsers_list.length) > 0) { 
            $("input[name='languages']").val(primaryUsers_list);
            if($.trim(url_str.length)> 0)
            {
                url_str = url_str + "&";
            }
            url_str = url_str + "primaryusers="+primaryUsers_list;
        };
        
        //language
        let languages_list = $("input[name='language']:checked").map(function() {return this.value;}).get().join(',');
        if($.trim(languages_list.length) > 0) { 
            $("input[name='languages']").val(languages_list);
            if($.trim(url_str.length)> 0)
            {
                url_str = url_str + "&";
            }
            url_str = url_str + "languages="+languages_list;
        };

        //languages
        

        //primary users
        
        // collect locale
        
        // let localeSelected = $("#locale").val();
        // if($.trim(localeSelected.length) > 0) { 
        //     $("input[name='locales']").val(localeSelected);
        //     if($.trim(url_str.length)> 0)
        //     {
        //         url_str = url_str + "&";
        //     }
        //     url_str = url_str + "locale="+localeSelected;
        // };

        let searchString = $("#searchby_input").val();
        if($.trim(searchString.length) > 0) { 
            $("input[name='searchBy']").val(searchString);
            if($.trim(url_str.length)> 0)
            {
                url_str = url_str + "&";
            }
            url_str = url_str + "searchby="+searchString;
        };

        // sort view
        let sortStatus = $("input[name='sortby']").val();
        
        if($.trim(sortStatus.length) > 0) { 
            
            if($.trim(url_str.length) > 0)
            {
                url_str = url_str + "&";
            }
            url_str = url_str + "sortby=" + sortStatus;
        };

        // verify view
        let viewStatus = $("input[name='view']").val();
        
        if($.trim(viewStatus.length) > 0) { 
            
            if($.trim(url_str.length) > 0)
            {
                url_str = url_str + "&";
            }
            url_str = url_str + "view=" + viewStatus;
        };
        
        //-------------
          
        let url = (window.location.origin + window.location.pathname).split(/[?#]/)[0];
           
        let append_url_str = '';
        if($.trim(url_str.length)>0) { 

            append_url_str = "?"+url_str;


        }

         // Current URL: https://my-website.com/page_a
         const nextURL = url+append_url_str;
         const nextTitle = document.getElementsByTagName("title")[0].innerHTML;
         const nextState = {};

         // This will create a new entry in the browser's history, without reloading
         window.history.pushState(nextState, nextTitle, nextURL);
         // This will replace the current entry in the browser's history, without reloading
        //window.history.replaceState(nextState, nextTitle, nextURL);
        
//once you get all values you can perform ajax- we have added 1 form with few hidded values, incase if requried, it can be used.
        

       // $('#form_filter')[0].submit();
    }

    $("#filterSubmit_btn").on('click',function(e){
        processFilters();
    });
    $("#sortby_select").on('change',function(e){
        $("input[name='sortby']").val($(this).val());
        processFilters();
    });
    $(".list-view-button").on('click',function(e){
        $("input[name='view']").val('list');
        processFilters();
    });
    $(".grid-view-button").on('click',function(e){
        $("input[name='view']").val('');
        processFilters();
    });


    

    $(document).on('click', '.tree label', function(e) {
     
      if($($(this).next('ul')).css('display') !== 'block'){
        $(this).addClass('show');
      }else{
        $(this).removeClass('show');
      }
        $(this).next('ul').fadeToggle("slow", function(){
          
      });
        e.stopPropagation();
      });

      // $(document).on('change', '#locale', function(e) {
      //   processFilters();
      // });

   
        $(document).on('keypress', '#searchby_input', function(e) {
        if (e.keyCode == 13) {
            processFilters();
        }
        });

        function debounce(cb, interval, immediate) {
            var timeout;
          
            return function() {
              var context = this, args = arguments;
              var later = function() {
                timeout = null;
                if (!immediate) cb.apply(context, args);
              };          
          
              var callNow = immediate && !timeout;
          
              clearTimeout(timeout);
              timeout = setTimeout(later, interval);
          
              if (callNow) cb.apply(context, args);
            };
          };
          
          function keyPressCallback() {
            var targetse = document.getElementsByName('searchBy');
            var inputse = document.getElementById('searchby_input');
            
            if($.trim(inputse.value.length)>=3){
                targetse.value = inputse.value;
                processFilters();
            }

           
            
          }
          
          document.getElementById('searchby_input').onkeypress = debounce(keyPressCallback, 400);

      
      
      
      $(document).on('change', '.tree input[type=checkbox]', function(e) {
        //$(this).siblings('ul').find("input[type='checkbox']").prop('checked', this.checked);
        //$(this).parentsUntil('.tree').children("input[type='checkbox']").prop('checked', this.checked);
        var checked = $(this).prop("checked"),
      container = $(this).parent(),
      siblings = container.siblings();

  container.find('input[type="checkbox"]').prop({
    indeterminate: false,
    checked: checked
  });

  function checkSiblings(el) {

    var parent = el.parent().parent(),
        all = true;

    el.siblings().each(function() {
      let returnValue = all = ($(this).children('input[type="checkbox"]').prop("checked") === checked);
      return returnValue;
    });
    
    if (all && checked) {

      parent.children('input[type="checkbox"]').prop({
        indeterminate: false,
        checked: checked
      });

      checkSiblings(parent);

    } else if (all && !checked) {

      parent.children('input[type="checkbox"]').prop("checked", checked);
      parent.children('input[type="checkbox"]').prop("indeterminate", (parent.find('input[type="checkbox"]:checked').length > 0));
      checkSiblings(parent);

    } else {

      el.parents("li").children('input[type="checkbox"]').prop({
        indeterminate: true,
        checked: false
      });

    }

  }

  checkSiblings(container);
  //
        e.stopPropagation();
        processFilters();
      });
      
      $(document).on('click', '.controls button', function(e) {
        switch ($(this).text()) {
          case 'Collepsed':
            $('.tree ul').fadeOut();
            break;
          case 'Expanded':
            $('.tree ul').fadeIn();
            break;
          case 'Checked All':
            $(".tree input[type='checkbox']").prop('checked', true);
            break;
          case 'Clear All':
                $(".tree input[type='checkbox']").prop('checked', false);
                $("#searchby_input").val('');
                $("#locale").val('');
                processFilters();
            break;
          default:
        }
      });

    //end
});