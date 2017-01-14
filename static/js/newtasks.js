
$(document).ready(function() {
      autoHideBox = $(document).find(".quickaddbox");
		if (autoHideBox.is(":visible")) {
        autoHideBox.hide();
		}
$('body').tooltip({
    selector: '[data-toggle="tooltip"]'
});
$(function() {
    $(".datepicker").datepicker({ dateFormat: 'yy-mm-dd' });
});
$(document).on('click', '.date', function() {
    $(".datepicker").datepicker({ dateFormat: 'yy-mm-dd' });
    previouspicker = $(this).prev('.datepicker');
    previouspicker.datepicker("show");
    // console.log($(this).prev('.datepicker'))
    // $(this).closest('.datepicker').datepicker("show");
});

var getDaysLeft = function(duedate) {
	var current = new Date();
	current = new Date(current.getFullYear(), current.getMonth(), current.getDate(), 0, 0, 0, 0);
	daysLeft = Math.ceil((duedate - current) / (1000 * 60 * 60 * 24));
	if (daysLeft < 0) {
        daysLeft = '(past due date)&nbsp;';
    } else if (daysLeft == 0) {
        daysLeft = '(in < 1 day)&nbsp;';
    } else if (daysLeft == 1) {
        daysLeft = '(in 1 day)&nbsp;';
    } else {
        daysLeft = '(in ' + String(daysLeft) + ' days)&nbsp;';
    }
    return daysLeft;
};

$(document).on('change', '.datepicker', function() {
  console.log( $(this).next('.date'));
  postdateman  =  $(this).val();
  postdatemanDate = new Date(postdateman);
  postdatemanDateSpliced = postdatemanDate.toUTCString().split(' ');
  $(this).next('.date').html(postdatemanDateSpliced[2]+". "+postdatemanDateSpliced[1]+", "+postdatemanDateSpliced[3]+'&nbsp;'+getDaysLeft(postdatemanDate));
  $(this).next('.date').removeClass('lighttext');
  posterid = $(this).closest("li").data('id');
  
  posturl = '/updateDate/';
  groupId = -1;
  if (window.location.pathname.includes('group')) {
  	posturl = '/updateGroupTaskDate/';
  	split = window.location.pathname.split('group/');
  	groupId = split[1];
  	groupId = groupId.replace('/', '');
  }
  $.ajax({
    type: "POST",
    dataType: "json",
    url: posturl,
    data: {
      posterid: posterid,
      datezp: postdateman,
      groupId: groupId,

    },
    cache: false,
  });
    // $('h4').html($('#datepicker').val());
});
            // using jQuery
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            var csrftoken = getCookie('csrftoken');
            function csrfSafeMethod(method) {
                // these HTTP methods do not require CSRF protection
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
    
    function updatePBars() {
          progressBarz = $("#nestable3").find(".progress-bar") ;

          progressBarEls = progressBarz.closest("li");
          console.log(progressBarEls);
          $.each(progressBarEls, function( index, value) {
            uncheckedVal = $(this).find("input[type='checkbox']").length;
            console.log(uncheckedVal);
            checkedVal = $(this).find("input:checked").length;
            percentageVal = checkedVal/uncheckedVal*100;

            if(percentageVal > 0 && percentageVal < 30) {
              $(progressBarz[index]).css({'width': percentageVal+"%",'background-color':'#d9534f'});

            } else if (percentageVal > 30 && percentageVal < 60) {
              $(progressBarz[index]).css({'width': percentageVal+"%",'background-color':'#f0ad4e'});
            } else {
              $(progressBarz[index]).css({'width': percentageVal+"%", 'background-color':'#5cb85c'});

            }

            $(progressBarz[index]).find(".percval").remove();
            $(progressBarz[index]).append('<span class="percval">'+Math.round(percentageVal)+'%</span>');
          });
    }
    
            
    updatePBars();
    
    $(document).on('click', '.editable', function() {
        var that = $(this);
        if (that.find('input').length > 0) {
            return;
        }
        var currentText = that.text();
        
        
        var $input = $('<input title="Click outside the textbox to save your changes.">').tooltip();

        that.text('');
  
        $(this).append($input);
        $input.focus();
        $input.val(currentText);  
        $(document).click(function(event) {
            if(!$(event.target).closest('.editable').length) {
                if ($input.val()) {
                    that.text($input.val());
                    idchange = that.closest("li").data('id');
                    namechange = $input.val();
                    $.ajax({
                        type: "POST",
                        dataType: "json",
                        url: '/updateName/',
                        data: {
                          idtchange: idchange,
                          nametchange: encodeURIComponent(namechange),
              
                        },
                        cache: false,
                      });
                    
                    
                    
                    
                    
                } else {
                  that.text(currentText);
                }
                that.find('input').remove();
            }
        });
    });


        
    $(document).on('click', 'input[type="checkbox"]', function() {


      if (this.checked) {
        //change all the children too
        closest = $(this).closest("li");
        closest.find(".dd3-content").css({'opacity':'0.5', 'text-decoration':'line-through'});
        childCheckboxes = closest.find('input[type="checkbox"]').prop('checked', true);
        $.each(childCheckboxes, function( index, value) {

          $.ajax({
            type: "PUT",
            dataType: "json",
            url: '.',
            data: {
              completed: 1,
              completed_id: this.name,
  
            },
            cache: false,
          });
          
        });


      }
      else {
        closest = $(this).closest("li");
        closest.find(".dd3-content").css({'opacity':'1', 'text-decoration':'none'});
        childCheckboxesFalse = closest.find("input").prop('checked', false);

        $.each(childCheckboxesFalse, function(index, value ){
              $.ajax({
                type: "PUT",
                dataType: "json",
                url: '.',
                data: {
                  completed: 0,
                  completed_id: this.name,
      
                },
                cache: false,
              });

        });





      }
      
    updatePBars();
      
      // if(this.checked) {
      // $.ajax({
      //             type: "PUT",
      //             dataType: "json",
      //             url: '.',
      //             data: {
      //               completed: 1,
      //               completed_id: this.name,
      //             },
      //             cache: false,
      //       });
      // }

    });

    $('#nestable3').nestable({
      group: 1,
      maxDepth: 5

    }).on('dragEnd', function(event, item, source, destination, position) {
      // Make an ajax request to persist move on database
      // here you can pass item-id, source-id, destination-id and position index to the server
      // ....
      var parent_id = $(item).parent().parent().data('id');
      var actual_id = $(item).data('id');
      var prev_id = $(item).prev("li").data('id');
      var next_id = $(item).next("li").data('id');
      console.log("id " + actual_id + "\nParent: " + parent_id + "\nPosition:" + position + "\nPrev : " + prev_id + "\nNext : " + next_id);
      if (!parent_id) {
        parent_id = -1;
      }
      if (!prev_id) {
        prev_id = -1;
      }
      if (!next_id) {
        next_id = -1;
      }
      $.ajax({
        type: "POST",
        dataType: "json",
        url: '.',
        data: {
          id: actual_id,
          parent_id: parent_id,
          position: position,
          prev_id: prev_id,
          next_id: next_id,

        },
        cache: false,
      });
    updatePBars();

    });
    updatePBars();
 
 
 	
 	
 	$(".details-btn").click(function() {
		details = $($(this).parent().parent().find("div.details").get(0));
		if (details.is(":visible")) {
			$(this).title = "Hide details";
			details.hide();
		} else {
			$(this).title = "Show details";
			details.show();
		}
	});
	
	
	 $(".quickadd").click(function() {
		quickadd = $(document).find(".quickaddbox");
		if (quickadd.is(":visible")) {
        	quickadd.hide();
		} else {
		    quickadd.show();
		}
	});
	
	
	
	$('.quickaddbox').bind("enterKey",function(e){
	  if($('.quickaddbox').val()=='') {
	    return;
	  }
	  if ($('.quickaddbox').val().length > 30) {
	  	alert('Maximum character length is 30');
	  	return;
	  }
	  entered_name = $(".quickaddbox").val().replace(/<(?:.|\n)*?>/gm, '');
	  posturl = '/add_todo/';
	  groupId = -1;
	  if (window.location.pathname.includes('group')) {
	  	posturl = '/addGroupTask/';
	  	split = window.location.pathname.split('group/');
	  	groupId = split[1];
	  	groupId = groupId.replace('/', '');
	  }
	   $.ajax({
        type: "POST",
        url: posturl,
        data: {
          namej: entered_name,
          groupId: groupId,
          
        },
        cache: false,
        success : function(json) {
            taskpk = json.savepk;
            console.log(taskpk); // log the returned json to the console
        	$("#notasks").hide();
                $("#nestable3 > ol > ol").append("\
          		  <li class='dd-item dd3-item' data-id='" + taskpk + "'>\
          		  <div class='dd-handle dd3-handle'>&nbsp;</div>\
          		  <div class='dd3-content'>\
          	     <div class='pull-left'>\
          	     <div class='checkbox no-margin'>\
          	     <label>\
          			  <input class='checkbox style-0' name='" + taskpk + "' type='checkbox'><span class='font-xs'>    	</span>\
          			 </label>\
          	     </div>\
          	     <span class='importantT glyphicon glyphicon-fire' data-toggle='tooltip' data-placement='top' setting='Not Urgent' title='Toggle Urgency' style='color:#ccc;'></span> \
          	     <span class='urgentT glyphicon glyphicon-star' data-toggle='tooltip' data-placement='top' setting='Not Important' title='Toggle Importance' style='color:#ccc;'></span>  \
          	     <span class='publicT glyphicon glyphicon glyphicon-eye-close' data-toggle='tooltip' data-placement='top' setting='Private' title='Toggle Privacy' style='color:#ccc;'></span> \
          		   		      <span class='removeT glyphicon glyphicon-remove'  data-toggle='tooltip' data-placement='top' title='Delete' style='color:#ff4848'></span> \
          		  </div>\
          	          <span class='editable'>" + entered_name + "</span>\
          	     <span class='pull-right'>\
          	             <input type='text' class='datepicker' style='visibility:hidden'>\
	                      	       <span class='date lighttext' data-toggle='tooltip' data-placement='top' title='Click to Change'>No Due Date&nbsp;</span>\
          	     <span class='pull-right details-btn details-icon glyphicon glyphicon-info-sign' title='Show details'></span>\
          			</span>\
          	   <div class='details'></div>\
          	   </div></li>");
          	   if (window.location.pathname.includes('group')) {
          	   		$('.publicT').hide();
          	   }
          	   $('.quickaddbox').val('');
        },

      });
   });
   
   
   
    $('.quickaddbox').keyup(function(e){
        if(e.keyCode == 13)
        {
              $(this).trigger("enterKey");

        }
    });

    //progress bar sanity
    listp2 = $('#nestable3').data('nestable');
    closest2 = $(".progress").closest("li");


    $(closest2).each(function() {

      console.log(this);
      itemz = $(this);
      lenOfChilds = $(this).find("li").length;
      if(lenOfChilds<1) {
        listp2.unsetParent(itemz);
      }
    
    //   lengthOfParentChilds = closestOfParent.find("li").length     
  	 // if(lengthOfParentChilds<=1) {
    //       listp2.unsetParent(closestOfParent);
    //   }
    });
    
    
    
    toggleTaskFlag = function (htmlTag, fieldName) {
    	taskId = -1;
		taskId = $(htmlTag).parent().parent().parent().data('id');
    	posturl = '/toggleTaskFlag/';
		groupId = -1;
		if (window.location.pathname.includes('group')) {
			posturl = '/toggleGroupTaskFlag/';
			split = window.location.pathname.split('group/');
			groupId = split[1];
			groupId = groupId.replace('/', '');
		}
    	$.ajax({
        type: "POST",
        url: posturl,
        data: {
        	taskId: taskId,
        	field: fieldName,
          	groupId: groupId,
        },
        cache: false,
        success: function() {
        	console.log($(htmlTag).attr('title'));
        	if ($(htmlTag).hasClass('glyphicon-eye-close')) {
        		$(htmlTag).removeClass('glyphicon-eye-close').addClass('glyphicon-eye-open');
        		$(htmlTag).attr('setting', 'Public');
        		$(htmlTag).css('color', '#12C3E6');
        	} else if ($(htmlTag).hasClass('glyphicon-eye-open')) {
        		$(htmlTag).removeClass('glyphicon-eye-open').addClass('glyphicon-eye-close');
        		$(htmlTag).attr('setting', 'Private');
        		$(htmlTag).css('color', '#ccc');
        	} else if ($(htmlTag).attr('setting') == 'Urgent') {
    			$(htmlTag).attr('setting', 'Not Urgent');
    			$(htmlTag).css('color', '#ccc');
        	} else if ($(htmlTag).attr('setting') == 'Not Urgent') {
    			$(htmlTag).attr('setting', 'Urgent');
    			$(htmlTag).css('color', '#ff4741');
        	} else if ($(htmlTag).attr('setting') == 'Important') {
    			$(htmlTag).attr('setting', 'Not Important');
    			$(htmlTag).css('color', '#ccc');
        	} else if ($(htmlTag).attr('setting') == 'Not Important') {
    			$(htmlTag).attr('setting', 'Important');
    			$(htmlTag).css('color', '#FBAC37');
        	}
        }
      });
    };
    $(document).on('click', '.importantT', function () {
    	toggleTaskFlag(this, 'urgent');
    });
    $(document).on('click', '.urgentT', function () {
    	toggleTaskFlag(this, 'important');
    });
   $(document).on('click', '.publicT', function () {
    	closest = $(this).closest("li");
    	currentSetting = $(this).attr('setting');
    	if(currentSetting=='Public') {
    	  pubChildTasks = closest.find("span[setting='Public']")
        $.each(pubChildTasks, function(index, value ){
          toggleTaskFlag(this, 'public');
        });
    	} else {
    	  privateChildTasks = closest.find("span[setting='Private']")
        $.each(privateChildTasks, function(index, value ){
          toggleTaskFlag(this, 'public');
        });
    	}
    	
      closestParent = closest.parent().parent("li");
      closestParentPubSpan = closestParent.find(".publicT")
      closestParentSetting = $(closestParentPubSpan[0]).attr('setting');
      if(closestParentSetting=='Private') {
         toggleTaskFlag(closestParentPubSpan, 'public');
      }



    });
});
