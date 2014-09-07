from django.conf.urls import patterns, include, url
from django.contrib import admin
from ontosApp import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ontosProject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r"^$", views.main, name="evernote_index"),
    url(r"^login/$", views.login, name="evernote_auth"),
    url(r"^dashboard/$", views.dashboard, name="evernote_callback"),
	url(r"^register/$", "register", name="register"),

    url(r'^admin/', include(admin.site.urls)),

)
