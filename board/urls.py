from django.urls import path

from .views import PostsList, PostDetail, PostCreate, PostEdit, PostDelete, CommentList, CommentCreate, \
    CommentDelete, CommentDetail, approve


urlpatterns = [
    path('', PostsList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/comment/', CommentCreate.as_view(), name='comment_create'),
    path('responses/', CommentList.as_view(), name='comment_list'),
    path('responses/<int:pk>/approve/', approve, name='approve'),
    # path('responses/<int:pk>', CommentDetail.as_view(), name='comment_detail'),
    path('responses/<int:pk>/delete/', CommentDelete.as_view(), name='comment_delete'),
]
