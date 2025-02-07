import uuid

from django.conf import settings
from django.db import models
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from taggit.managers import TaggableManager
from django.shortcuts import reverse
from embed_video.fields import EmbedVideoField



class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    tags = TaggableManager()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Video(models.Model):
    caption=models.CharField(max_length=100)
    description = models.TextField()
    video=models.FileField(upload_to='video/')
    preview=models.ImageField(upload_to='media/')
    tags=models.TextField()
    def __str__(self):
        return self.caption

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('oursite:product_list_by_category',
                       args=[self.slug])

class Course(models.Model):
    owner = models.ForeignKey(User, related_name='courses_created',on_delete=models.CASCADE)
    category = models.ForeignKey(Subject, related_name='courses',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    work = models.FileField(upload_to='work/')


    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('oursite:product_detail',
                       args=[self.id, self.slug])

    def url_to_course(self):
        return reverse('oursite:show',
                       args=[self.slug])


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video = models.FileField(upload_to='video/')
    slug = models.SlugField(max_length=200, default=uuid.uuid1())
    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)
    def __str__(self):
        return self.title


class UrlCheck(models.Model):
    title = url = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    def __str__(self):
        return self.title

class Homework(models.Model):
    course = models.ForeignKey(Course, related_name='homework', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    homework_file = models.FileField(upload_to='homework/')
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

class Constructor(models.Model):
    owner = models.ForeignKey(User, related_name='constructor_created',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, default=uuid.uuid1())

class VideoForConstructor(models.Model):
    constructor = models.ForeignKey(Constructor, related_name='constr', on_delete=models.CASCADE)
    video = models.CharField(max_length=200)

class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, limit_choices_to={'model__in': ('text',
                                                                                  'video',
                                                                                  'image',
                                                                                  'file')},on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')


class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name='%(class)s_related',on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


