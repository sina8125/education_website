from os.path import join, splitext

import jdatetime
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils import timezone
from mptt.models import TreeForeignKey, MPTTModel

from accounts.models import User


class Category(MPTTModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        if self.parent:
            return f'{self.parent}_{self.name}'
        return self.name

    def get_absolute_url(self):
        return reverse('post:category_filter:post-list', args=[self.slug, ])


class Post(models.Model):

    def set_thumbnail_path(self, filename):
        return join('posts', 'thumbnails', f'thumbnails_{filename}')

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    thumbnail = models.ImageField(upload_to=set_thumbnail_path)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    available = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    description = RichTextUploadingField(blank=True, config_name='default')
    category = models.ForeignKey(Category, related_name='posts', blank=True, null=True, on_delete=models.SET_NULL)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[self.slug, ])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    is_reply = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    body = models.TextField(max_length=500)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.body[:10] + '...' if len(self.body) > 10 else self.body

    @property
    def solar_date(self):
        return jdatetime.datetime.fromgregorian(
            datetime=self.created_time.astimezone(tz=timezone.get_current_timezone()), tzinfo=timezone.tzinfo,
            locale=jdatetime.FA_LOCALE)

    @property
    def solar_show_date(self):
        return self.solar_date.strftime('%d %B %Y')


class Favorite(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'favorite'
        verbose_name_plural = 'favorites'
        unique_together = (('user', 'post'),)
