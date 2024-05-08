from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name = 'post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostNewView.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('drafts/', views.PostDraftList.as_view(), name='post_draft_list'),
    path('post/<pk>/publish/', views.PostPublishView.as_view(), name='post_publish'),
    path('post/<pk>/remove/', views.PostRemoveView.as_view(),name='post_remove'),
    path('post/<int:pk>/comment/', views.AddCommentToPostView.as_view(), name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', views.CommentApproveView.as_view(), name='comment_approve'),
    path('comment/<int:pk>/remove/', views.CommentRemoveView.as_view(), name='comment_remove'),
    path('accounts/logout/', views.custom_logout_view, name='logout'),
]