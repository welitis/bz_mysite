from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class OAuthRelationship(models.Model):
    OAUTH_TYPE = (
        (1, 'QQ'),
        (2, 'WeChat'),
        (3, 'WeiBo'),
        (4, 'Github'),
        (5, 'Twitter')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    openid = models.CharField(max_length=128)
    oauth_type = models.IntegerField(choices=OAUTH_TYPE)

    def __str__(self):
        return "<OAuthRelationship %s>" % self.user.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户名")
    nickname = models.CharField('昵称', max_length=50)

    def __str__(self):
        return self.user.username


def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''


def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username


User.get_nickname = get_nickname
User.get_nickname_or_username = get_nickname_or_username