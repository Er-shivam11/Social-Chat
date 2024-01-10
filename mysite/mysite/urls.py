"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path,include
from chat import views
from accounts import views as accounts


urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat", include("chat.urls")),
    path('', views.home, name='home'),
    path('messages', views.messages, name='messages'),
    path('createpost', views.create_post, name='createpost'),
    path('edit_post/<int:post_id>/', views.edit_post, name='editpost'),
    path('addcomment/<int:post_id>/', views.add_comment, name='addcomment'),
    path('toggle_like/<int:post_id>/', views.toggle_like, name='toggle_like'),





    path('login/', accounts.loginuser, name='login'),
     path('signup/', accounts.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('createuser/', accounts.createuser, name='createuser'),
    path('user_profile/', accounts.userprofile, name='userprofile'),
    path('user_list/', accounts.userlist, name='userlist'),
    path('basicuserprofile/', accounts.basicuserprofile, name='basicuserprofile'),
    path('userhome/', accounts.userhome, name='userhome'),



    

    path('checksuperusre/', accounts.checksuperusre, name='checksuperusre'),
    


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)