from django.conf.urls import url
from django.contrib import admin
from Main import views

urlpatterns = [
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$',views.user_logout, name='logout'),
	url(r'^$',views.Question_list, name='home'),
	url(r'^views$',views.Question_list_views, name='home_views'),
	url(r'^create/$', views.Question_create,name='create'),
	url(r'^question/(?P<id>\d+)/$', views.Question_detail,name='detail'),
	url(r'^update/(?P<id>\d+)/$', views.Question_update,name='update'),
	url(r'^delete/(?P<id>\d+)/$', views.Question_delete,name='delete'),
	url(r'^ansupdate/(?P<id>\d+)/$', views.Answer_update,name='ans_update'),
	url(r'^ansdelete/(?P<id>\d+)/$', views.Answer_delete,name='ans_delete'),
	url(r'^ansaccept/(?P<id>\d+)/$', views.Answer_accept,name='accept'),
	url(r'^ansunaccept/(?P<id>\d+)/$', views.Answer_unaccept,name='unaccept'),
	url(r'^upvote/(?P<id>\d+)/$', views.vote_up,name='up'),
	url(r'^downvote/(?P<id>\d+)/$', views.vote_down,name='down'),
	url(r'^profile/(?P<id>\d+)/$', views.profile,name='profile'),
	url(r'^profileupdate/(?P<id>\d+)/$', views.Update_pro,name='profile_update'),
	url(r'^users$',views.User_list, name='user'),
	]
