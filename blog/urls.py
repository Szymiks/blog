from django.urls import path

from blog import views
from blog.feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    # url dla wioków funkcyjnych
    path("tag/<slug:tag_slug>/", views.post_list, name='post_list_by_tag'),

    path("", views.post_list, name='post_list'),
    path('home', views.home, name='home'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('update/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.post_update, name='post_update'),
    path('delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('search/', views.post_search, name='post_search'),


    path('feed/', LatestPostsFeed(), name='post_feed')




]
