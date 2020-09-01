from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('home',views.home,name="home"),
    path('register',views.register,name="register"),
    path('logout',views.logout,name="logout"),
    path('adminpanel',views.adminpanel,name="adminpanel"),
    path('product',views.product,name="product"),
    path('add',views.add,name="add"),
    path("update/<int:id>/",views.update,name='update'),
    path("delete/<int:id>/",views.delete,name="delete" ),
    path('logoutuser',views.logoutuser,name='logoutuser'),
    path('admin/',views.adminlog),
    
]