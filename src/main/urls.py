from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name="main"),
    path('home/', views.home_view, name='home'),
    path('list/', views.list_view, name='list'),
    path('listing/<str:id>', views.listing_view, name='listing_view'),
    path('listing/<str:id>/edit', views.edit_view, name='edit_view'),
    path('listing/<str:id>/like/', views.like_listing_view, name='like_listing'),
    path('send-mail/', views.send_mail, name='send_mail'),
    path('listing/<str:id>/inquire/',
         views.inquire_listing_using_email, name='inquire_listing'),
    path('delete_listing/<str:id>', views.delete_listing_view, name='delete_listing'),
    path('delete_listing_confirmation/<str:id>', views.delete_listing_confirmation_view, name='delete_listing_confirmation'),
    #path('listing/<str:id>/delete/', views.listing_delete_view, name='delete_listing'),
]