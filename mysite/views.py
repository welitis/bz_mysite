from django.core.cache import cache
from django.shortcuts import render
from read_statistics.utils import *


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date)\
        .values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num'))\
        .order_by('-read_num_sum')
    return blogs[:7]


# 缓存通用执行函数
def cache_handle(keyname, func, *args):
    value = cache.get(keyname)
    if value is None: # 缓存不存在则向数据库查找
        if args:
            value = func(*args)
        else:
            value = func()
        cache.set(keyname, value, 3600)
        return value
    return value


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    context = {}
    context['read_nums'] = cache_handle('read_nums', get_seven_days_read_data, blog_content_type)[0]
    context['dates'] = cache_handle('dates', get_seven_days_read_data, blog_content_type)[1]
    context['today_hot_data'] = cache_handle('today_hot_data', get_today_hot_data, blog_content_type)
    context['yesterday_hot_data'] = cache_handle('yesterday_hot_data', get_yesterday_hot_data, blog_content_type)
    context['sevenday_hot_data'] = cache_handle('sevenday_hot_data', get_7_days_hot_blogs)
    return render(request, 'home.html', context)


