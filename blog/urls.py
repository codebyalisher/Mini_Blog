from  django.urls import  path
from blog import views

urlpatterns=[
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('userlogin/',views.user_login,name='userlogin'),
    path('userlogout/',views.user_logout,name='userlogout'),
    path('signup/',views.signup,name='signup'),
    path('addpost/',views.add_post,name='addpost'),
    path('updatepost/<int:pk>/',views.update_post,name='updatepost'),
    path('deletepost/<int:id>/',views.del_post,name='delete'),
    ]