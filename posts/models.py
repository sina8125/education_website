# Django
from django.urls import reverse
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _

# local
from accounts.models import User
from utils.models import AbstractCreatedUpdatedTime

# python
from os.path import join, splitext

# third party
import jdatetime
from ckeditor_uploader.fields import RichTextUploadingField
from mptt.models import TreeForeignKey, MPTTModel


class Category(MPTTModel):
    name = models.CharField(
        verbose_name=_('نام فارسی'),
        max_length=200
    )
    name_en = models.CharField(
        verbose_name=_('نام انگلیسی'),
        max_length=200
    )
    slug = models.SlugField(
        verbose_name=_('نشانی'),
        max_length=200,
        unique=True
    )
    parent = TreeForeignKey(
        'self',
        verbose_name=_('دسته بندی والد'),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('دسته بندی')
        verbose_name_plural = _('دسته بندی ها')

    def __str__(self):
        if self.parent:
            return f'{self.parent}_{self.name}'
        return self.name

    def get_absolute_url(self):
        return reverse('post:category_filter:post-list', args=[self.slug, ])


class Post(AbstractCreatedUpdatedTime):

    def set_thumbnail_path(self, filename):
        return join('posts', 'thumbnails', f'thumbnails_{filename}')

    title = models.CharField(
        verbose_name=_('عنوان فارسی'),
        max_length=200
    )
    title_en = models.CharField(
        verbose_name=_('عنوان انگلیسی'),
        max_length=200
    )
    slug = models.SlugField(
        verbose_name=_('نشانی'),
        max_length=200,
        unique=True
    )
    thumbnail = models.ImageField(
        verbose_name=_('تصویر اصلی'),
        upload_to=set_thumbnail_path
    )
    created_user = models.ForeignKey(
        User,
        verbose_name=_('نویسنده'),
        on_delete=models.CASCADE,
        related_name='posts'
    )
    available = models.BooleanField(
        verbose_name=_('وضعیت دسترسی'),
        default=True
    )
    is_premium = models.BooleanField(
        verbose_name=_('پست اشتراکی'),
        default=False
    )
    description = RichTextUploadingField(
        verbose_name=_('توضیحات فارسی'),
        blank=True,
        config_name='default'
    )
    description_en = RichTextUploadingField(
        verbose_name=_('توضیحات انگلیسی'),
        blank=True,
        config_name='default'
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_('دسته بندی'),
        related_name='posts',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = _('پست')
        verbose_name_plural = _('پست ها')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[self.slug, ])


class Comment(AbstractCreatedUpdatedTime):
    post = models.ForeignKey(
        Post,
        verbose_name=_('پست'),
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        verbose_name=_('نویسنده'),
        on_delete=models.CASCADE,
        related_name='comments'
    )
    reply_to = models.ForeignKey(
        'self',
        verbose_name=_('پاسخ به'),
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    is_reply = models.BooleanField(
        verbose_name=_('نوع کامنت'),
        default=False
    )
    available = models.BooleanField(
        verbose_name=_('وضعیت دسترسی'),
        default=True
    )
    body = models.TextField(
        verbose_name=_('متن'),
        max_length=500
    )

    class Meta:
        verbose_name = _('کامنت')
        verbose_name_plural = _('کامنت ها')

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

    @property
    def show_date(self):
        return self.created_time.strftime('%d %B %Y')


class Favorite(AbstractCreatedUpdatedTime):
    post = models.ForeignKey(
        Post,
        verbose_name=_('پست'),
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    user = models.ForeignKey(
        User,
        verbose_name=_('کاربر'),
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    class Meta:
        verbose_name = _('علاقه مندی')
        verbose_name_plural = _('علاقه مندی ها')
        unique_together = (('user', 'post'),)
