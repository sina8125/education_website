from django.urls import path, include

from .views import PostListView, PostDetailView, PostAddReplyView, PostAddToFavoriteView

favorite_url = [
    path('', PostListView.as_view(), name='post-list'),
    path('favorite/', PostListView.as_view(), name='favorite-post')
]

urlpatterns = [
    path('', include((favorite_url, 'posts'), namespace='home')),
    path('category/<slug:category_slug>/', include((favorite_url, 'posts'), namespace='category_filter'),
         name='category_filter'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('reply/<slug:slug>/<int:comment_id>/', PostAddReplyView.as_view(), name='add_reply'),
    path('add-favorite/<slug:post_slug>/', PostAddToFavoriteView.as_view(), name='add_favorite')

]
