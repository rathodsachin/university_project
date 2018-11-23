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
	url(r'^payfees/$', views.payfees, name='payfees'),

	#url('^', include('django.contrib.auth.urls')),

	url(r'^password/reset/$', 
        auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"), 
        name='password_reset'),
	
	url(r'^password/reset/done/$', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), 
        name='password_reset_done'),
	
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), 
        name='password_reset_confirm'),

	url(r'^reset/done/$', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), 
        name='password_reset_complete'),

    
]