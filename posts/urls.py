# Django
from django.urls import path, include

# local
from .views import PostListView, PostDetailView, PostAddReplyView, PostAddToFavoriteView, PostListApiView

favorite_url = [
    path('', PostListView.as_view(), name='post-list'),
    path('favorite/', PostListView.as_view(), name='favorite-post')
]

api_url = [
    path('', PostListApiView.as_view(), name='post-list-api'),
    path('favorite/', PostListApiView.as_view(), name='favorite-post-api'),
]

urlpatterns = [
    path('', include((favorite_url, 'posts'), namespace='home')),
    path('category/<slug:category_slug>/', include((favorite_url, 'posts'), namespace='category_filter'),
         name='category_filter'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('reply/<slug:slug>/<int:comment_id>/', PostAddReplyView.as_view(), name='add_reply'),
    path('add-favorite/<slug:post_slug>/', PostAddToFavoriteView.as_view(), name='add_favorite'),
    path('api/posts/', include((api_url, 'posts'), namespace='post_api'), ),
    path('api/category/<slug:category_slug>/', include((api_url, 'posts'), namespace='category_api'), ),

]
