from django.shortcuts import render, redirect, reverse
from .models import Comment
from django.contrib.contenttypes.models import ContentType
# Create your views here.


def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    # 数据检查
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'message': '用户未登录', 'redirect_to': referer})

    content = request.POST.get('content', '').strip()
    if not content:
        return render(request, 'error.html', {'message': '评论内容为空', 'redirect_to': referer})

    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'error.html', {'message': '评论对象不存在', 'redirect_to': referer})
    # 检查通过，保存信息
    comment = Comment()
    comment.comment_user = request.user
    comment.content = content

    comment.content_object = model_obj
    comment.save()
    return redirect(referer)