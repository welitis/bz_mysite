from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import Comment


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput(attrs={}))
    object_id = forms.IntegerField(widget=forms.HiddenInput(attrs={}))
    text = forms.CharField(label='', error_messages={'required': '评论内容不能为空'},
                           widget=CKEditorWidget(config_name='comment_ckeditor', attrs={
        'class': 'form-control',
        'rows': 5,
    }))
    reply_comment_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'id': 'reply_comment_id'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if hasattr(self, 'user'):
            if self.user.is_authenticated:
                self.cleaned_data['user'] = self.user
            else:
                raise forms.ValidationError('用户尚未登录')

        # 评论对象验证，content_type, object
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            model_class = ContentType.objects.get(model=content_type).model_class()
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')

        return self.cleaned_data

    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data.get('reply_comment_id')
        if reply_comment_id < 0:    # reply的id不能小于0
            raise forms.ValidationError('回复出错')
        elif reply_comment_id == 0: # 代表的是根评论，即不回复任何人，所以没有父母
            self.cleaned_data['parent'] = None
        elif Comment.objects.filter(pk=reply_comment_id).exists():  # 判断是否存在
            self.cleaned_data['parent'] = Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError("回复出错")
        return reply_comment_id
