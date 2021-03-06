from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), # index is the name of a method in views.py
    url(r'^success$', views.success),
    url(r'^login$', views.login),
    url(r'^new$', views.reg),
    url(r'^logout$', views.logout),
    url(r'^wishes/new$', views.new_wish),
    url(r'^wishes/add_wish$', views.add_wish),
    url(r'^wishes/(?P<wish_id>\d+)/edit$', views.edit),
    url(r'^wishes/(?P<wish_id>\d+)/destroy$', views.destroy),
    url(r'^wishes/(?P<wish_id>\d+)/update$', views.update),
    url(r'^wishes/(?P<wish_id>\d+)/grant$', views.grant),
    url(r'^wishes/(?P<wish_id>\d+)/like$', views.toggle_like),
]