from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    # url dla wioków funkcyjnych
    # path("", views.post_list, name='post_list'),
    # path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    # path('<int:post_id>/share/', views.post_share, name='post_share'),
    # url dla widoków opartych na klasach
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/share/', views.PostShareView.as_view(), name='post_share'),
]
