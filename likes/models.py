from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
# Create your models here.


class LikeCount(models.Model):
    # 点赞对象
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # 点赞数量
    liked_num = models.IntegerField('点赞数', default=0)

    def __str__(self):
        return str(self.content_type)

    class Meta:
        verbose_name = verbose_name_plural = '点赞数'


class LikeRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content_type)

    class Meta:
        db_table = 'like_record'
        verbose_name = verbose_name_plural = '点赞详情'