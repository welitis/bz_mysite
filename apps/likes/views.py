from .models import LikeCount, LikeRecord
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def error_response(code, message):
    data = {}
    data['status'] = 'error'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def success_response(like_num):
    data = {}
    data['status'] = 'success'
    data['liked_num'] = like_num
    return JsonResponse(data)


def like_change(request):
    if request.method != "GET":
        return error_response(404, 'request method error')
    user = request.user
    if not user.is_authenticated:   # 判断用户是否登录
        return error_response(400, 'you were not login')
    content_type_model = request.GET.get('content_type')
    object_id = request.GET.get('object_id')
    try:
        content_type = ContentType.objects.get(model=content_type_model)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return error_response(401, 'object not exists')

    # 处理数据
    if request.GET.get('is_like') == 'true':   # 不能因为前端返回True就立即创建对象，而是先判断数据库中是否存在，不存在则创建
        # 要点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 未点赞过，进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num += 1
            like_count.save()
            return success_response(like_count.liked_num)
        else:
            # 已点赞过，不能重复点赞
            return error_response(402, 'you were liked')
    else:
        # 取消点赞
        like_record_list = LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user)
        if like_record_list.exists():
            # 数据存在，有点赞过，则这次是取消点赞
            like_record = like_record_list.first()
            like_record.delete()    # 删除点赞详情
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created: # 数据正常，点赞数已存在
                like_count.liked_num -= 1     # 点赞总数-1
                like_count.save()
                return success_response(like_count.liked_num)
            else:   # 数据异常
                return error_response(404, 'data error')
        else:
            # 数据不存在,取消点赞，但对象从未创建过，异常
            return error_response(403, 'you were not liked')

