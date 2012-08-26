from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from forum.models import Forum, Thread, Post, UserProfile

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django import forms
from django.core.files.base import ContentFile
from django.core.context_processors import csrf

# Decorator that only allows users that are logedon to run the function below.
@login_required
#Add new thread function.
def addThread(request):
	#Checks if user is authed. Function that i used before i discoverd the decorator.
	if request.user.is_authenticated():
		#Gets all the userinput data, And the dynamicly generated ID.
		id = request.GET['id']
		name = request.GET['threadName']
		description = request.GET['threadDescription']
		forum = Forum.objects.get(id=id)
		#Creates a instance of a user so the Thred is bound to a creator.
		user = User.objects.get(username__exact=request.user.username)
		
		#A cleaner that scans trough the thread description the users typed in and replaces the \n line breakers with html linebreakers (<br>)
		cleanDescription = ""
		for a in description:
			if a in '\n':
				a += r'<br>'
			cleanDescription += a
		#creates a new insance of Thread, inserts the values and finaly saves them.
		newTread = Thread(key_forum=forum, title=name, content=cleanDescription, displays=0, author= user )
		newTread.save()
		bool = True
		#Sends the user back to the viewThreads function and dispalys the forum the user added the newthread in.
		return HttpResponseRedirect(reverse('forum.views.viewThreads', args=(id,)))
	else:
		#If faulthy access user gets sentback to startpage
		bool = False
		return HttpResponseRedirect(reverse('forum.views.viewForum'))	

#Add new forum function.		
@login_required
def addForum(request):
	if request.user.is_authenticated():
		#Gets all the userinput data. 
		name = request.GET['forumName']
		description = request.GET['forumDescription']
		#Creates a instance of a user so the Thred is bound to a creator.
		user = User.objects.get(username__exact=request.user.username)
		
		#A cleaner that scans trough the thread description the users typed in and replaces the \n line breakers with html linebreakers (<br>)
		cleanPost = ""
		for a in description:
			if a in '\n':
				a += r'<br>'
			cleanPost += a
		#creates a new insance of Forum, inserts the values and finaly saves them.
		newForum = Forum(title=name, content=cleanPost, displays=0, author= user )
		newForum.save()
		bool = True
		#Sends the user back to the viewForum function and dispalys the forum the user added the new forum in.
		return HttpResponseRedirect(reverse('forum.views.viewForum'))
	else:
		#If faulthy access user gets sentback to startpage
		bool = False
		return HttpResponseRedirect(reverse('forum.views.viewForum'))

#Add new post function.		
@login_required
def addPost(request):
	if request.user.is_authenticated():
		#Gets all the userinput data. And the hidden input fields that contains the ID's of the forum and thread the user is located in.
		postContent = request.GET['postContent']
		forum_key = request.GET['forum_key']
		thread_key = request.GET['thread_key']
		
		#A cleaner that scans trough the thread description the users typed in and replaces the \n line breakers with html linebreakers (<br>)
		cleanPost = ""
		for a in postContent:
			if a in '\n':
				a += r'<br>'
			cleanPost += a
		#Creates a instance of a user so the Thred is bound to a creator.
		user = User.objects.get(username__exact=request.user.username)	
		key_forum = Forum.objects.get(id=forum_key)
		key_thread = Thread.objects.get(id=thread_key, key_forum=forum_key)
		
		#creates a new insance of Post, inserts the values and finaly saves them.
		newPost = Post(content=cleanPost, displays=0, author= user, key_forum=key_forum, key_thread=key_thread )
		newPost.save()
		bool = True
		return HttpResponseRedirect(reverse('forum.views.viewPosts', args=(forum_key,thread_key)))	
	else:
		bool = False
		return HttpResponseRedirect(reverse('forum.views.viewForum'))

#Changes data in existing post.
@login_required
def changePost(request):
	if request.user.is_authenticated():
		try:
			#Gets the userdata input, and the dynamicly generated ID that belongs to a specific post.
			newContent = request.GET['postContent']
			postID = request.GET['postID']
			
			#Stars the instance of the post the user wants to edit
			changedPost = Post.objects.get(id=postID)
			#select which column that will get a new value, and declares the new value.
			changedPost.content = newContent
			changedPost.save()
			bool = 1
			return HttpResponse(bool)
		except:
			bool = 0
			return HttpResponse(bool)
	else:
		bool = 0
		return HttpResponse(bool)

#Delete specific item.
@login_required
def deleteItems(request, author, type, itemID):
#Built to operate when javascript is deactivated, therby the parameters.
	#Everything wrapped in try/except if the process would go trough the user vill return a error message.
	try:
		if request.user.is_staff:
			#If the user returns a 0 it means that the process didnt validate the criterias for deleting and item
			mess= 0
			#Checks what kind of item is being requested to be deleted.
			if type == "forum":
				#starts ans instance of the object with the specific ID and deletes it.
				item = Forum.objects.get(id=itemID)
				item.delete()
			if type == "thread":
				item = Thread.objects.get(id=itemID)
				item.delete()
			if type == "post":
				item = Post.objects.get(id=itemID)
				item.delete()
			mess= 1
		else:
			mess= 0
			#Regular users can only delete their own posts. This validation step stopps users who may alter the delete-URL-pattern.
			#And want to delete a post that isnt crated by the user who is logedon.
			if author == request.user.username:
				if type == "post":
					item = Post.objects.get(id=itemID)
					item.delete()
				mess=1
			else:
				mess=0
	except:
		mess=2
	
	return HttpResponse(mess)

def checkUser(request):
	#Gets the userdata input.
	username = request.GET['username']
	
	try:
		bool = 1
		#Try to start an instance of a user with the data the user typed in the username field.
		#If the process validates the username is taken, and the bool variable is set to False, therby returnning a0 to the user,
		#alerting the user that this username is taken, pick a newone
		User.objects.get(username__exact=username)
	except:
		#if the matching process crashes the boolvariable will be set to True, the username is free and the If-statement will be runed.
		bool = 0

	return HttpResponse(bool)

#Add new user
def signUp(request):
	#sets a Staff variable is user is staff, this allows user to create and delete foums
	if request.user.is_staff:
		staff = True
	else:
		staff = False
	#Sets a authed variabels if, that validates if user is logedon.
	if request.user.is_authenticated():
		authed = True
	else:
		authed = False
	form = UploadFileForm(request.POST, request.FILES)
	if form.is_valid():
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		image = form.cleaned_data['file']
		
		newUser = user = User.objects.create_user(username, email, password)
		newUser.save()

		newProfile = UserProfile(user=user, firstname=firstname, lastname=lastname, image=image)
		newProfile.save()

		user = authenticate(username=username, password=password)
		auth_login(request, user)

		return HttpResponseRedirect('/')
	else:
		c = {'form': form, 'authed':authed, 'request':request}
		c.update(csrf(request))
		form = UploadFileForm()
		return render_to_response('signUp.html', c)

class UploadFileForm(forms.Form):
    file  = forms.FileField()