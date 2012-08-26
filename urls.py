from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

#The view file that handels the GET operations
urlpatterns = patterns('forum.views',
	url(r'^$', 'viewForum', name="View Forum"),
	url(r'^(?P<forumID>\d+)/$', 'viewThreads', name="View Threads"),
	url(r'^(?P<forumID>\d+)/(?P<threadID>\d+)/$', 'viewPosts', name="View Posts"),
	
	url(r'^login/$', 'login', name="Login Protocoll"),
	url(r'^logout/$', 'logout', name="Logout Protocoll"),
)


#The add file that writes/cahange data in the database
urlpatterns += patterns('forum.add',
	url(r'^AddThread/$', 'addThread', name="add new thread"),
	url(r'^AddForum/$', 'addForum', name="Add new forum"),
    url(r'^AddPost/$', 'addPost', name="Add new post"),
	url(r'^checkUser/$', 'checkUser', name="Add new User"),

	url(r'^sign-up/$', 'signUp', name="sigUp"),
	
	url(r'^deleteItem/(?P<author>\w+)/(?P<type>\w+)/(?P<itemID>\d+)/$', 'deleteItems', name="Delete items"),
	url(r'^changePost/$', 'changePost', name="Edit Post"),
	
	#url(r'^saveImage/$', 'upload_file', name="add new User"),
)

#Admin view
urlpatterns += patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

#Allows you to fetch staticdata from a local serverfolder if DEBUG is set to true in the settingsfile
if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
	)
