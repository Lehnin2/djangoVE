from django.urls import path
from .views import *
urlpatterns = [
    path('list/',conferenceList,name="listconf"),
    path('listview/',conferenceListeview.as_view(),name="listviewconf"),
    path('details/<int:pk>/',detailsviewconference.as_view(),name="detailconf"),
    path('create/',Createviewconference.as_view(),name="conference_create"),
    path('update/<int:pk>/',UpdateViewconference.as_view(),name="conference_update"),
    path('delete/<int:pk>/',DeleteViewconference.as_view(),name="conference_delete")

]
