from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
import os


from forum.models import Forum, Thread, Post, UserProfile

#Function that generates the Forum-view
def viewForum(request):
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
	
	#Fetches all forum objects from DB, if an error occurrs forum  variable will be set no False
	try:
		forum = Forum.objects.all()		
	except:
		forum = False
	return render_to_response('forum.html', locals())

#Function that generates the Threads-view
def viewThreads(request, forumID):
	#sets a Staff variable is user is staff, this allows user to create and delete threas
	if request.user.is_staff:
		staff = True
	else:
		staff = False
	#Sets a authed variabels if, that validates if user is logedon. allows user to create thread
	if request.user.is_authenticated():
		authed = True
	else:
		authed = False
	#Fetches all Thread-objects from DB that has the specific relationship with Forum
	#If an error occurrs such as non-matching query the threads variable will be set no False
	try:
		forum = Forum.objects.get(id=forumID)
		threads = Thread.objects.all().filter(key_forum=forumID)
	except:
		threads = False
	return render_to_response('threads.html', locals())

#Function that generates the Threads-view
def viewPosts(request, forumID, threadID):
	#sets a Staff variable is user is staff, this allows user to create and delete posts
	if request.user.is_staff:
		staff = True
	else:
		staff = False
	#Sets a authed variabels if, that validates if user is logedon. allows user to create posts and etit them.
	if request.user.is_authenticated():
		authed = True
	else:
		authed = False
	#Fetches all Post-objects from DB that has the specific relationship with Threads. 
	#If an error occurrs such as non-matching query the threads variable will be set no False
	try:
		forum = Forum.objects.get(id=forumID)
		thread = Thread.objects.get(id=threadID)
		posts = Post.objects.all().filter(key_forum=forumID, key_thread=threadID).order_by('created')
	except:
		posts = False
	username = request.user.username
	return render_to_response('posts.html', locals())

#Function that generates the Profile-view	
#OBS! NOT FINISHED!
def viewProfile(request):
	#Sets a authed variabels if, that validates if user is logedon. allows user to create posts and etit them.
	if request.user.is_authenticated():
		authed = True
	else:
		authed = False
	#Fetches the username from the metadata and crosscheks it with the profile that has a Foregienkey realtion with the User object.
	try:	
		user = User.objects.get(username__exact=request.user.username)
		profile = UserProfile.objects.get(username=user)
	except:
		pass

#Login Function
def login(request):
	#Grabs the username & password the user typed into the input fields.
	username = request.GET['username']
	password = request.GET['password']
	#Try to authenticate the user with the data the user enterd.
	user = authenticate(username=username, password=password)
	#If the user returns username the user will be logedin.
	#A session is created that ceeps the user logedon.
	if user is not None:
		if user.is_active:
			auth_login(request, user)
			bool = 0
		else:
			bool = 1
	#Returning a 1 menans that the user enterd wrong data or that the user has be deactivated.
	else:
		bool = 1
	return HttpResponse(bool)
#Logout Function	
def logout(request):
	#A builtin django function that probertly flushes the user session.
	auth_logout(request)
	return HttpResponse("logout")

