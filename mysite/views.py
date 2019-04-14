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


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums, dates = get_seven_days_read_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    sevenday_hot_data = cache.get('sevenday_hot_data')
    if sevenday_hot_data is None:
        sevenday_hot_data = get_7_days_hot_blogs()
        cache.set('sevenday_hot_data', sevenday_hot_data, 3600)

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['sevenday_hot_data'] = sevenday_hot_data
    return render(request, 'home.html', context)


