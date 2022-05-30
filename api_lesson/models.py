from django.db import models
from django.contrib.auth.models import User


class Lesson(models.Model):
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    level = models.IntegerField()

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def contents(self):
        return self.lessoncontent_set.all()


class LessonContent(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    content = models.TextField(null=True, blank=True)
    order_num = models.IntegerField()

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.content

