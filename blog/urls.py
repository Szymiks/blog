from django.urls import path

from blog import views

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


    # url dla widoków opartych na klasach

    # path('', views.PostListView.as_view(), name='post_list'),
    # path('home', views.HomepageView.as_view(), name='home'),
    # path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    # path('<int:post_id>/share/', views.PostShareView.as_view(), name='post_share'),
    # path('update/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostUpdateView.as_view(), name='post_update'),
    # path('delete/<int:pk>/', views.DeletePostView.as_view(), name='post_delete'),
]
