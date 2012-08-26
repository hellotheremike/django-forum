$(document).ready(function(){
	formActionButtons();
	forumPostButtonActions();
	generalActionButtons();
	userRelatedActionButtons();
	tooltip('.useravatar');

	$('input[type=file]').change(function(){
		$(this).siblings("span").html("").parent().addClass('granted');
	});

	$('#file').click(function(){
		$(this).siblings('input[type=file]').click();
	})

	function loginFormAnimation(direction){
			//$("#add-item").animate({bottom: "20px"},{duration: 500,easing:'easeInOutCubic'})
			if(direction == 'up')
				$("#login-form").animate({bottom: "20px"},{duration: 500,easing:'easeInOutCubic'})
			else
				$("#login-form").animate({bottom: "-230px"},{duration: 500,easing:'easeInOutCubic'})
		}
	function addFormAnimation(direction){
			//$("#login-form").animate({bottom: "20px"},{duration: 500,easing:'easeInOutCubic'})
			if(direction == 'up')
				$("#add-item").animate({bottom: "20px"},{duration: 500,easing:'easeInOutCubic'})
			else
				$("#add-item").animate({bottom: "-400px"},{duration: 500,easing:'easeInOutCubic'})
		}
	function formActionButtons(){
		$("#login-toggle").toggle(
			function(){
				loginFormAnimation('down');
				return false;
			},
			function(){
				loginFormAnimation('up');
				return false;
			}
		);
		$("#additem-toggle").toggle(
			function(){
				addFormAnimation('down');
				return false;
			},
			function(){
				addFormAnimation('up');
				return false;
			}
		);
		$(".remove .icon").click(function(){
			if($(this).hasClass('rotate')){
				$(this).removeClass('rotate');
				$(this).parent().animate(
					{width: '12px'},
					{duration: 300, easing:'easeInCubic'});
			}
			else{
				var width = '65px'
				if($(this).html() == 'S')
					width = '85px'

				$(this).addClass('rotate')
				$(this).parent().animate(
					{width: width},
					{duration: 300, easing:'easeInCubic'});
			}

		});
		$(".remove a").click(function(){
			$(this).siblings().removeClass('rotate')
			$(this).parent().animate(
				{width: '12px'},
				{duration: 300, easing:'easeInCubic'}
			);
		});
	}

	function forumPostButtonActions(){
		//Edit button that is generated if Post belongs to logedon user  
		$(".editPost").click(function(event){
			//Orienting to the Div that holds the comment data
			data=$(this).parent().parent().parent().children('.right').children('.contentData');
			console.log(data)
			data.addClass('editMode');
			//Alows me to edit the content in the Div.
			data.attr('contenteditable','true').focus();
			//Dispalys Save/Cancel buttons
			data.parent().children('.changeContent').css({'display':'block', 'opacity':'0'});
			data.parent().children('.changeContent').animate({opacity:1},{duration:500})
			return false;
		});
		//Saves changes to post.
		$(".save-changes").click(function(event){
			//In the HTML the value is the same as the HREF, this way i get the right adress to the save for the specific post
			postID = $(this).attr('data-value')
			//The content of the Div that contains the comment
			newContent = $(this).parent().parent().parent().children('.contentData');
			//The comment contentn from the last save.
			orginal = $(this).parent().parent().parent().children('.contentDataOrginal');
			//Save / Cancel Buttons
			links = $(this).parent().parent().parent().children('.changeContent');
			
			//If the orginal and new content is the same it wont save cause no changes has ben done sience last save in the newContent.
			if(newContent.html() != orginal.val()){
				$.get('/changePost', { postContent: newContent.html(), postID: postID },
				function(data){
					//If Django returns 1 the save was successfull
					if(data == 1){
						//Hides Save/Cancel links
						links.animate({opacity:0},{duration:500, complete: function(){$(this).hide();}});
						//Disabels that user can change content in comment Div
						newContent.attr('contenteditable','false').removeClass('editMode');
						//Sets newsaved value to hidden inputfield
						orginal.val(newContent.html());
					}else{
						alert("Error occured.")
					}
				});

				
			}
			//If No changes  has ben made in newContent user will be alerted to do so.
			else{
				$(this).parent().addClass('error')
			}
			return false;
		});
		//Cancels and close editmode
		$(".cancel-changes").click(function(event){
			//Disabels contenteditabel and resets all atributs to its original.
			$(this).parent().parent().parent().children('.changeContent').animate({opacity:0},{duration:500, complete: function(){$(this).hide();}})
			content = $(this).parent().parent().parent().children('.contentData')
			orginal = $(this).parent().parent().parent().children('.contentDataOrginal').val();
			content.attr('contenteditable','false').removeClass('editMode');
			//Fills the Div with its orginal data if it should have been changed.
			content.html(orginal)
			return false;
		});
		//Deletes specific post. Diffrent button due to diffrent HTML structure than Forum & Tread
		$('.deletePost').click(function(){
			//If Yes call AJAX deletes specific post, fetches the adress that handels the delete process.
			//that is set ho have the same value as the href-link. This becusee the site partly is prepared for browsers  with javascript disabeld
		 	url = $(this).attr("data-value");
			path = $(this).parent().parent().parent();
			$.get(url,
				function(data){
					//If django returns 0 the user didnt validate the permisson controll
					if(data == 0){
						alert("You dont have permissions to do this.");
					}
					//If django returns 1 the comment will be hiddden and the deleteprocess was succesfull
					if(data == 1){
						path.css({'minHeight':'0px', 'height':path.height()})
						path.animate({height: '0px', opacity: '0'},{duration: 900, complete: function(){
								path.remove();
						}})
					}
					//If django returns 2 the user is trying to delete a none existing item
					if(data == 2){
						alert("Item does not exist.");
					}
					
			});
			return false;
	    });	
	}

	function generalActionButtons(){
		//Deletes specific Forums & Threads
		$(".deleteForumThread").click(function(event){
			//If Yes call AJAX deletes specific Forums or threads, fetches  the adress that handels the delete process.
			//that is set ho have the same value as the href-link. This becusee the site partly is prepared for browsers  with javascript disabeld
			url = $(this).attr("data-value");
			path = $(this).parent().parent().parent();		
			$.get(url,
				function(data){
					//If django returns 0 the user didnt validate the permisson controll
					if(data == 0){
						alert("You dont have permissions to do this.");
					}
					//If django returns 1 the comment will be hiddden and the deleteprocess was succesfull
					if(data == 1){
						path.animate({height: '0px', opacity: '0'},{duration: 900, complete: function(){
							path.remove();
						}})
					}
					//If django returns 2 the user is trying to delete a none existing item
					if(data == 2){
						alert("Item does not exist.");
					}
			});
			return false;
		});
		//Add Forum animation
		$("#addForumBtn").click(function(event){	
			//If the Add-divbox height is 200px,  animate it to a height of 0px, and sett CSS atribute display to none
			if($('#addContainer').css('height')== "220px"){
				$('#addContainer').animate({
				height: 0
				}, 800, function() {
					$('#addContainer').css({'display':'none'});
					//Animation complete.
				});
			}
			//If the height isnt 220px, sett CSS atribute display to block and animate it to a height of 220px 
			else{
				$('#addContainer').css({'display':'block'});
				$('#addContainer').animate({
				height: 220
				}, 800, function() {
					// Animation complete.
				});
			}
		  });	 
		//Add Thread animation
		$("#addThreadBtn").click(function(event){	
			//If the Add-divbox height is 200px,  animate it to a height of 0px, and sett CSS atribute display to none
			if($('#addContainer').css('height')== "220px"){
				$('#addContainer').animate({
				height: 0
				}, 800, function() {
					$('#addContainer').css({'display':'none'});
					// Animation complete.
				});
			}
			//If the height isnt 220px, sett CSS atribute display to block and animate it to a height of 220px 
			else{
				$('#addContainer').css({'display':'block'});
				$('#addContainer').animate({
				height: 220
				}, 800, function() {
					// Animation complete.
				});
			}
		  });
		//thread post button
		$("#postButton").click(function(){
			var text = $("#postContent");
			if(text.val()){
				return true
			}
			else{
				text.parent().addClass('error')
				return false
			}
		});
	}

	function userRelatedActionButtons(){
		//Create user function
		$("#new-username").keyup(function(){
			if($(this).val()){
				$("#new-username").siblings('span').html("").parent().removeClass('error').addClass('granted');
				$.get('/checkUser',{username: $("#new-username").val()},function(data){
					if(data == 1){
						$("#new-username").siblings('span').html("Username is taken").parent().addClass('error').removeClass('granted');
					}
				});
			}
			else{
				$("#new-username").siblings('span').html("Chose your username").parent().addClass('error').removeClass('granted');
			}
		});
		$("#new-lastname").keyup(function(){
			if($("#new-lastname").val()){
				$("#new-lastname").siblings('span').html("").parent().removeClass('error').addClass('granted');
			}
			else{
				$("#new-lastname").siblings('span').html("Type your firstname").parent().removeClass('granted').addClass('error');
			}
		});
		$("#new-firstname").keyup(function(){
			if($("#new-firstname").val()){
				$("#new-firstname").siblings('span').html("").parent().removeClass('error').addClass('granted');
			}
			else{
				$("#new-firstname").siblings('span').html("Type your lastname").parent().removeClass('granted').addClass('error');
			}
		});
		$("#new-email").keyup(function(){
			if($("#new-email").val()){
				$("#new-email").siblings('span').html("").parent().removeClass('error').addClass('granted');
			}
			else{
				$("#new-email").siblings('span').html("Type your email").parent().removeClass('granted').addClass('error');
			}
		});
		$("#new-password").keyup(function(){
			if($("#new-password").val()){
				$("#new-password").siblings('span').html("").parent().removeClass('error').addClass('granted');
			}
			else{
				$("#new-password").siblings('span').html("Type your password").parent().removeClass('granted').addClass('error');
			}
		});
		$("#new-password-confirm").keyup(function(){
			if($("#new-password-confirm").val()){
				$("#new-password-confirm").siblings('span').html("").parent().removeClass('error').addClass('granted');
			}
			else{
				$("#new-password-confirm").siblings('span').html("repeat your password").parent().removeClass('granted').addClass('error');
			}
		});

		$("#create-user").click(function(){
			//Checks all Inputfields if they contain any data
			function validateEmail(email) { 
			    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
			    return re.test(email);
			} 
			var bool = false;
			if(!$("#new-username").val()){
				$("#new-username").siblings('span').html("Chose your username").parent().addClass('error');
			}
			if(!validateEmail($("#new-email").val())){
				$("#new-email").siblings('span').html("Type a valid email").parent().addClass('error').removeClass('granted');
			}
			if(!$("#new-email").val()){
				$("#new-email").siblings('span').html("Type your email").parent().addClass('error');
			}
			if($("#new-password-confirm").val() != $("#new-password").val()){
				$("#new-password-confirm").siblings('span').html("Passwords dont match").parent().addClass('error').removeClass('granted');
				$("#new-password").siblings('span').html("Passwords dont match").parent().addClass('error').removeClass('granted');
			}
			if(!$("#new-password-confirm").val() && !$("#new-password").val()){
				$("#new-password-confirm").siblings('span').html("Type a valid password").parent().addClass('error');
				$("#new-password").siblings('span').html("Type a valid password").parent().addClass('error');
			}
			if(!$("#new-lastname").val()){
				$("#new-lastname").siblings('span').html("Type your lastname").parent().addClass('error');
			}
			if(!$("#new-firstname").val()){
				$("#new-firstname").siblings('span').html("Type your firstname").parent().addClass('error');
			}
			if(!$("#id_file").val()){
				$("#file").siblings('span').html("Chose a profile picture").parent().addClass('error');
			}
			//final controll that all fields validate
			if($("#new-password-confirm").val() == $("#new-password").val() && $("#new-password-confirm").val() 
				&& $("#new-password").val() && $("#new-email").val() 
				&& $("#new-username").val() && validateEmail($("#new-email").val()) && $("#id_file").val()){
				bool = true;
			}
			return bool
		});
		//Runs the logoutfunction in a ajax call so the user remains at the same site when pressing the button.
		$("#logout").click(function(event){
			$.get('/logout',
				function(data){
					location.reload();
			});
			return false;
		});	
		//Runs the Loginfunction in a ajax call so the user remains at the same site when pressing the button.
		//This because  the user dont have to navigate to a thread AGAIN when logingon.
		$("#login").click(function(event){
			username = $('#login-form .holder p.input input[type=text]').val();
			password = $('#login-form .holder p.input input[type=password]').val();
			if(username && password){
				$('#login-form .holder p.input').removeClass('error')
				$.get('/login', { username: username, password: password },
				function(data){
					if(data == 0){
						loginFormAnimation('up');
						$("#login-form").animate(
							{bottom: "20px"},
							{duration: 500,easing:'easeInOutCubic', complete:function(){
								location.reload();
							}}
							);
					}
					else{
						$('#login-form .holder p.message').html("Wrong username or password, try again!");
					}
				});
			}
			else{
				$('#login-form .holder p.message').html("");
				$('#login-form .holder p.input').removeClass('error')
				if(!username){
					$('#login-form .holder p.input:eq(0)').addClass('error')
				}
				if(!password){
					$('#login-form .holder p.input:eq(1)').addClass('error')
				}
			}
			return false;
		});
	}	
	
	function tooltip(target_items){
		$(target_items).each(function(i){
			$("body").append("<div class='tip' id='tip"+i+"'><img src='"+$(this).attr("src")+"' alt='avatar'></div>");
			var my_tooltip = $("#tip"+i);
			$(this).removeAttr("title").mouseover(function(){
				my_tooltip.css({display:"none"}).fadeIn(300);
			}).mousemove(function(kmouse){
					my_tooltip.css({left:kmouse.pageX+15, top:kmouse.pageY-40});
			}).mouseout(function(){
					my_tooltip.fadeOut(300);
			});
		});
	}

});
