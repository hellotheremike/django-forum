from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from PIL import Image


#A base class that contains fields that the other tabels also will contain.
class Base(models.Model):
	content = models.CharField(max_length=500)
	created = models.DateTimeField(auto_now=True)
	lastChanged = models.DateTimeField(auto_now=True)
	displays = models.IntegerField()
	author = models.ForeignKey(User, blank=True, null=True)
	
	#orders the posts the variable created that is a Date column, so the latest entry will be the first in the list.
	class Meta():
		ordering = ['-created']

#The class that holds all the forum		
class Forum(Base):
	title = models.CharField(max_length=50)
	
	#When calledupon this class will return the title of the Forum.
	def __unicode__(self):
		return self.title
	#Fetches all the thread-objects that is related to a specific forum-entry.
	#This is used to count the number of threads in a forum.
	def threadsInForum(self):
		return self.thread_set.all()
	#Returns the Post-object of the latest activity in a specific forum
	#I use it to print the username & thread.
	def lastPostInForum(self):
		return Post.objects.filter(key_forum=self)[:1]

#The class that holds the threads
class Thread(Base):
	title = models.CharField(max_length=50)
	#Creating a relation between Forum and Thread so that the right thread will apperar in the right forum.
	key_forum = models.ForeignKey(Forum)
	
	#When calledupon this class will return the title of the Thread.
	def __unicode__(self):
		return self.title
	#Fetches all the Post-objects that is related to a specific Thread-entry.
	#This is used to count the number of posts(comments) in a forum.
	def commentsInThread(self):
		return self.post_set.all()
	#Returns the Post-object of the latest activity in a specific Thread.
	#I use it to print the username.
	def commentsInPost(self):
		return Post.objects.filter(key_thread=self)[:1]

#The class that holds the Posts/Comments
class Post(Base):
	#Creating a relation between Forum and Post so i can access post data from the forum view.
	key_forum = models.ForeignKey(Forum)
	#Creating a relation between Post and Thread so that the right post will apperar in the right thread.
	key_thread = models.ForeignKey(Thread)
	
	#Retuns the comment entry data.
	def __unicode__(self):
		return self.content

def content_file_name(instance, filename):
    return '/'.join(['avatars', instance.user.username, filename])

#Userprofile that holds userdata and a image.
class UserProfile(models.Model):
	#user = models.ForeignKey(User, blank=True, null=True, related_name='profile')
	user = models.ForeignKey(User, blank=True, null=True, related_name='profile')
	firstname = models.CharField(max_length=50)
	lastname = models.CharField(max_length=50)
	image = models.FileField(upload_to=content_file_name)
	
	#When calledupon this class will return the firstname of the user.
	def __unicode__(self):
		return self.user.username
	
	#Resize images when uploaded to save server data-storage.
	def save(self, size=(200, 200)): 
		super(UserProfile, self).save() 
		if self.image: 
			filename = self.image.path 
			image = Image.open(filename) 
			image.thumbnail(size, Image.ANTIALIAS) 
			image.save(filename) 
	
#A simple admin-registration because the system is not meant to be used from the django-admin view.
admin.site.register(Forum)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(UserProfile)
