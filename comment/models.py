from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
# Create your models here.


class Comment(models.Model):
    # 评论对象
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # 评论内容
    content = models.TextField()
    # 评论时间
    comment_time = models.DateTimeField(auto_now_add=True)
    # 评论者
    comment_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


    def __str__(self):
        return str(self.content_object)

    class Meta:
        db_table = 'comment'
        ordering = ['-comment_time']
        verbose_name = verbose_name_plural = '评论'