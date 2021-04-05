from django.urls import path
from blog import views

app_name = 'app'

urlpatterns = [
    path('post/create/', views.PostCreateView.as_view(), name='create_post'),
    path('post/published/', views.PostListView.as_view(), name='list_post'),
    path('post/drafts/', views.PostDraftListView.as_view(), name='drafts_list'),
    path('post/detail/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/update/<int:pk>', views.PostUpdateView.as_view(), name='post_update'),
    path('post/delete/<int:pk>', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/publish/<int:pk>', views.post_publish, name='publish'),
    path('post/comments/<int:pk>', views.add_comment, name='comments'),
]
