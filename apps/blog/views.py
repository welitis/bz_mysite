from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from comment.models import Comment
from read_statistics.utils import read_statistics_once_read
from .models import *


# Create your views here.


def get_blog_list_common_data(request, blogs_all_list):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 每10篇进行分页
    page_of_blogs = paginator.get_page(page_num)  # get_page可以处理一些不合法的参数
    current_page_num = page_of_blogs.number
    page_range = list(range(max(current_page_num - 2, 1), min(current_page_num + 3, paginator.num_pages + 1)))
    # 加上省略页码标记
    # 加入第一页或尾页码
    if page_range[0] != 1:
        if page_range[0] == 2:
            page_range.insert(0, 1)
        else:
            page_range.insert(0, 1)
            page_range.insert(1, '...')
    if page_range[-1] != paginator.num_pages:
        if page_range[-1] == paginator.num_pages - 1:
            page_range.append(paginator.num_pages)
        else:
            page_range.extend(['...', paginator.num_pages])

    # 获取博客分类的对应博客数量

    # type_count = {}
    # blog_types = BlogType.objects.all()
    # for blog_type in blog_types:
    #     blog_type_count = Blog.objects.filter(blog_type=blog_type).count()
    #     type_count[blog_type] = blog_type_count

    # 获取时间归档中对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_dates_dict[blog_date] = Blog.objects.filter(created_time__year=blog_date.year,
                                                         created_time__month=blog_date.month).count()

    context = {}
    context['page_range'] = page_range
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    # 获取按月分类的datetime对象列表
    context['blog_date'] = blog_dates_dict
    return context


def blog_list(request):
    blogs = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs)
    return render(request, 'blog/blog_list.html', context)


def blog_type_list(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, id=blog_type_pk)
    blogs = Blog.objects.filter(blog_type=blog_type).all()
    context = get_blog_list_common_data(request, blogs)
    context['blog_type'] = blog_type
    return render(request, 'blog/blog_type_list.html', context)


def blog_date_list(request, year, month):
    blogs = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs)
    # 获取按月分类的datetime对象列表
    context['blog_cur_date'] = "%s年%s月" % (year, month)
    return render(request, 'blog/blog_date_list.html', context)


def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, id=blog_pk)
    context = {}
    context['blog'] = blog
    # 阅读计数
    read_cookie_key = read_statistics_once_read(request, blog_pk)
    context['previous_blog'] = Blog.objects.filter(created_time__gt=context['blog'].created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__lt=context['blog'].created_time).first()

    content_type = ContentType.objects.get(model='blog')
    comment_list = Comment.objects.filter(content_type=content_type, object_id=blog_pk).order_by('-comment_time')
    paginator = Paginator(comment_list, 5)
    page_of_comment = paginator.get_page(request.GET.get('page', 1))
    current_page_num = page_of_comment.number
    page_range = list(range(max(current_page_num - 2, 1), min(current_page_num + 3, paginator.num_pages + 1)))
    # 加上省略页码标记
    # 加入第一页或尾页码
    if page_range[0] != 1:
        if page_range[0] == 2:
            page_range.insert(0, 1)
        else:
            page_range.insert(0, 1)
            page_range.insert(1, '...')
    if page_range[-1] != paginator.num_pages:
        if page_range[-1] == paginator.num_pages - 1:
            page_range.append(paginator.num_pages)
        else:
            page_range.extend(['...', paginator.num_pages])

    context['page_of_comment'] = page_of_comment
    context['page_range'] = page_range
    response = render(request, 'blog/blog_detail.html', context)
    if read_cookie_key:
        response.set_cookie(read_cookie_key, 'true')
    return response
