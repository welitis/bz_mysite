import datetime
from read_statistics.models import ReadNum, ReadDetail
from blog.models import Blog
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum




def read_statistics_once_read(request, blog_pk):
    ct = ContentType.objects.get_for_model(Blog)
    key = "%s_%s_read" % (ct.model, blog_pk)
    if not request.COOKIES.get(key, None):
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=blog_pk)
        readnum.read_num += 1
        readnum.save()
        # 判断阅读详情模型中是否有当天该篇文章的阅读数对象
        readnum, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=blog_pk, date=timezone.now())
        readnum.read_num += 1
        readnum.save()
        return key
    return None


def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(10, 3, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m-%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return read_nums, dates


def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')[:5]
    return read_details


def get_yesterday_hot_data(content_type):
    yesterday = timezone.now().date() - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')[:5]
    return read_details


def get_7_days_hot_data(content_type):
    today = timezone.now().date()
    passtime = timezone.now().date() - datetime.timedelta(days=7)
    read_details = ReadDetail.objects.filter(content_type=content_type, date__lt=today, date__gte=passtime)\
                       .values('content_type', 'object_id').annotate(read_num_sum=Sum('read_num'))\
                       .order_by('-read_num')[:5]
    return read_details
