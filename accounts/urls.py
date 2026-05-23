from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.myAccount),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('custDashboard/', views.custDashboard, name='custDashboard'),
    path('restDashboard/', views.restDashboard, name='restDashboard'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('vendor/',include('vendor.urls'))
]