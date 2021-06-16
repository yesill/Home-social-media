from django.db import models


# Create your models here.
class Post(models.Model):
    content = models.CharField(max_length=999, verbose_name="content")
    author = models.ForeignKey("auth.user", on_delete=models.CASCADE, verbose_name="author")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="created_date")
    likers = models.JSONField(verbose_name="likers", default=list)
    #images = models.FileField(blank=True, null=True, verbose_name="add image")
