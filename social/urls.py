from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic.base import RedirectView
from social import views
from social.views import MyPostListView, MyPostCreateView, MyPostDetailView, MyProfileListView, MyProfileUpdateView, MyProfileDetailView

#from social.views import NoticeListView
urlpatterns = [
    path('',RedirectView.as_view(url="home/")),
    path('home/', views.HomeView.as_view()),
    path('about/', views.AboutView.as_view()),
    path('contact/', views.ContactView.as_view()),
    path('login/', views.loginPage, name="login"), 
    path('profile/edit/<int:pk>', views.MyProfileUpdateView.as_view(success_url="/social/home")),
    
    
    
    path('mypost/create/', views.MyPostCreateView.as_view(success_url="/social/mypost")),
    path('mypost/delete/<int:pk>', views.MyPostDeleteView.as_view(success_url="/social/mypost")),
    path('mypost/', views.MyPostListView.as_view()),
    path('mypost/<int:pk>', views.MyPostDetailView.as_view()),


    path('mypost/like/<int:pk>', views.like),
    path('mypost/unlike/<int:pk>', views.unlike),

    path('myprofile/', views.MyProfileListView.as_view()), 
    path('myprofile/<int:pk>', views.MyProfileDetailView.as_view()),
    path('myprofile/follow/<int:pk>', views.follow),
    path('myprofile/unfollow/<int:pk>', views.unfollow),




    #path('register/', views.RegisterView.as_view()),
    #path('',RedirectView.as_view(url='home/')),
    path('register/', views.registerPage, name="register"),

    path('logout/', views.logoutUser, name="logout"),
    #path('', views.home1, name="home1"),
   
]
