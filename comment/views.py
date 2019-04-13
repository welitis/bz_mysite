import datetime

from django.shortcuts import render, redirect, reverse
from .models import Comment
from .forms import CommentForm
from django.http import JsonResponse
# Create your views here.


def update_comment(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST, user=request.user)
        data = {}
        if comment_form.is_valid():
            comment = Comment()
            comment.comment_user = comment_form.cleaned_data['user']
            comment.content = comment_form.cleaned_data['text']
            comment.content_object = comment_form.cleaned_data['content_object']
            # 获取form表单根据id查询的父评论对象
            parent = comment_form.cleaned_data['parent']
            if not parent is None:  # 如果父评论对象不为None，说明这条评论不是根评论
                comment.root = parent if parent.root is None else parent.root
                # 如果父评论的root为None，说明父评论就是根评论，则当前评论对象的根评论就是父评论
                # 如果父评论的root不为None，说明父评论之上还有评论，则根评论为上一层的根评论，
                # 就这样逐层递归，最后确定根评论
                comment.parent = parent # 父评论=父评论
                comment.reply_to = parent.comment_user  # 回复用户为父评论用户
            comment.save()

            # 返回数据
            data['status'] = 'success'
            data['username'] = comment.comment_user.username
            data['comment_time'] = comment.comment_time.timestamp()
            data['text'] = comment.content
            if not parent is None:
                data['reply_to'] = comment.reply_to.username
                data['root_id'] = comment.root_id
            else:
                data['reply_to'] = ''
            data['pk'] = comment.pk

        else:
            data['status'] = 'error'
            data['data'] = comment_form.errors
        return JsonResponse(data)
    return JsonResponse({'status': 'error'})