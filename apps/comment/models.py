# Create your models here.
import threading

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string


class SendMail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.email = email
        self.text = text
        self.fail_silently = fail_silently
        super().__init__()

    def run(self):
        send_mail(self.subject,
                  self.text,
                  settings.EMAIL_HOST_USER,
                  self.email,
                  self.fail_silently,
                  html_message=self.text)


class Comment(models.Model):
    # 评论对象
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # 评论内容
    content = models.TextField()
    # 评论时间
    comment_time = models.DateTimeField(auto_now_add=True)
    # 评论者
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

    root = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name="root_comment")  # 根评论
    parent = models.ForeignKey("self", null=True, on_delete=models.CASCADE, related_name="parent_comment")  # 父评论
    reply_to = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="replys")  # 回复哪个评论

    def __str__(self):
        return str(self.content)

    class Meta:
        db_table = 'comment'
        ordering = ['comment_time']
        verbose_name = verbose_name_plural = '评论'

    def send_mail(self):
        # 发送邮件通知
        if self.parent is None:
            # 评论我的博客
            subject = '有人评论你的博客'
            email = self.content_object.get_email()
        else:
            # 回复评论
            subject = '有人回复你的评论'
            email = self.reply_to.email
        if email != '':
            context = {}
            context['comment_text'] = "{}回复了你，并说：{}".format(self.comment_user, self.content)
            context['url'] = self.content_object.get_url()
            text = render_to_string('comment/send_mail_temp.html', context)
            thread = SendMail(subject, text, [email], fail_silently=False)
            thread.start()
