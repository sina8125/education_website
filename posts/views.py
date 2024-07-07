# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import gettext_lazy as _

# local
from .forms import CommentCreateForm, CommentReplyForm
from .models import Post, Comment, Favorite, Category
from .serializers import CommentSerializer
from subscriptions.models import Subscription
from accounts.authentication import CookieJWTAuthentication
from .serializers import PostListSerializer

# python
import math
from datetime import timedelta

# third party
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class PostListView(View):
    def get(self, request, category_slug=None):
        posts = Post.objects.filter(available=True)
        if category_slug:
            categories = get_object_or_404(Category, slug=category_slug).get_descendants(include_self=True)
            posts = posts.filter(category__in=categories)

        if 'favorite/' in request.path and request.user.is_authenticated:
            posts = posts.filter(available=True, favorites__user=request.user)
        if 'page' in request.GET.keys():
            page = int(request.GET.get('page'))
        else:
            page = 1
        number_of_page = math.ceil(len(posts) / 20)
        if not 0 < page <= number_of_page:
            page = 1

        posts = posts[20 * (page - 1): 20 * page]
        return render(request, 'posts/home.html',
                      context={'posts': posts, 'number_of_pages': number_of_page, 'page': page})


class PostDetailView(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug, available=True)
        comments = post.comments.filter(available=True, is_reply=False)
        comments = CommentSerializer(comments, many=True)
        comments = JSONRenderer().render(comments.data).decode('utf-8')
        similar_posts = Post.objects.filter(
            category=post.category,
            created_time__gte=timezone.now() - timedelta(days=30)).exclude(pk=post.pk).order_by('?')[:3]
        if post.is_premium:
            if not request.user.is_authenticated:
                messages.error(request, _('برای مشاهده این پست لطفا وارد شوید'), 'danger')
                return redirect(request.META['HTTP_REFERER'])
            user_sub = Subscription.objects.filter(user=request.user,
                                                   )
            if not user_sub.exists():
                messages.error(request, _('برای مشاهده این پست به اشتراک نیاز دارید'), 'danger')
                return redirect(request.META['HTTP_REFERER'])
        is_favorite = False
        if request.user.is_authenticated:
            is_favorite = Favorite.objects.filter(post=post, user=request.user).exists()
        return render(request,
                      'posts/detail.html',
                      context={'post': post, 'comments': comments,
                               'comment_form': CommentCreateForm,
                               'reply_form': CommentReplyForm,
                               'similar_posts': similar_posts,
                               'is_favorite': is_favorite
                               }
                      )

    @method_decorator(login_required)
    def post(self, request, slug):
        comment_form = CommentCreateForm(request.POST)
        post = get_object_or_404(Post, slug=slug, available=True)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            messages.success(request, _('نظر شما ثبت شد'), 'success')
            return redirect('post:post_detail', slug)


class PostAddReplyView(View):
    @method_decorator(login_required)
    def post(self, request, slug, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, available=True)
        post = get_object_or_404(Post, slug=slug, available=True)
        form = CommentReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.post = post
            reply.reply_to = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, _('پاسخ شما ثبت شد'), 'success')
            return redirect('post:post_detail', slug)


class PostAddToFavoriteView(View):
    @method_decorator(login_required)
    def get(self, request, post_slug):
        user = request.user
        post = get_object_or_404(Post, slug=post_slug)
        favorite, created = Favorite.objects.get_or_create(post=post, user=user)
        if created:
            messages.success(request, _('پست به علاقه مندی ها اضافه شد'), 'success')
        else:
            favorite.delete()
            messages.success(request, _('پست از علاقه مندی ها حذف شد'), 'success')
        return redirect('post:post_detail', post_slug)


# ---------------------------
# apis

class PostListApiView(APIView):
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request: Request, category_slug=None):
        posts = Post.objects.filter(available=True)
        if category_slug:
            categories = get_object_or_404(Category, slug=category_slug).get_descendants(include_self=True)
            posts = posts.filter(category__in=categories)
        if 'favorite/' in request.path and request.user.is_authenticated:
            posts = posts.filter(available=True, favorites__user=request.user)

        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)
