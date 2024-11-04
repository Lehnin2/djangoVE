from django.urls import path
from .views import *
urlpatterns = [
    path('register/',usercreateview.as_view(),name="register"),
    path('login/',logincustomview.as_view(),name="login"),
    path('logout/',logoutcustomview.as_view(),name="logout")

]
