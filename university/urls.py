from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

	url(r'^$', views.home, name='home'),	
	url( r'^login/$',auth_views.LoginView.as_view(template_name="login.html"), name="login"),
	#url(r'^logout/$', auth_views.LogoutView.as_view({'next_page': 'login'}),name='logout'),	
	url(r'^logout/$', auth_views.LogoutView.as_view(template_name="home.html"),name='logout'),
	url(r'^signup/$', views.signup, name='signup'),		
	url(r'^load_branch/$',views.load_branch,name="load_branch"),
]