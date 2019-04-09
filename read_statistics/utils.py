from read_statistics.models import ReadNum, ReadDetail
from blog.models import Blog
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


def read_statistics_once_read(request, blog_pk):
    ct = ContentType.objects.get_for_model(Blog)
    key = "%s_%s_read" % (ct.model, blog_pk)
    if not request.COOKIES.get('blog_%s_readed' % blog_pk, None):
        if ReadNum.objects.filter(content_type=ct, object_id=blog_pk).count():
            # 存在记录
            readnum = ReadNum.objects.get(content_type=ct, object_id=blog_pk)
        else:
            readnum = ReadNum(content_type=ct, object_id=blog_pk)
        readnum.read_num += 1
        readnum.save()
        # 判断阅读详情模型中是否有当天该篇文章的阅读数对象
        if ReadDetail.objects.filter(content_type=ct, object_id=blog_pk, date=timezone.now()).count():
            # 存在记录，则获取对象
            readnum = ReadDetail.objects.get(content_type=ct, object_id=blog_pk, date=timezone.now())
        else:
            readnum = ReadDetail(content_type=ct, object_id=blog_pk)
        readnum.read_num += 1
        readnum.save()
        return key
    return None