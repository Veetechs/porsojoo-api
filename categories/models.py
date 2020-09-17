import os
import uuid

from django.conf import settings
from django.db import models


# Create your models here.


def post_image_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/post/images/', filename)


class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='adder'
    )
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Image(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploader'
    )
    image = models.ImageField(blank=False, null=False, upload_to=post_image_file_path, default='default.jpg')
    uploaded_date = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='questioner'
    )
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    answers = models.ManyToManyField('Answer', related_name="questionAnswers", null=True, blank=True)
    images = models.ManyToManyField('Image', blank=True)


class Answer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="inserter",
    )
    body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dis_likes = models.IntegerField(default=0)
