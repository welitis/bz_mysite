# 基于Django实现个人博客

基于`python3.6`和`django2.0`的博客

![](https://img.shields.io/badge/build-passing-green.svg) ![](<https://img.shields.io/badge/requirement-insecure-red.svg>)

### 主要功能：

- 文章、页面、分类目录、标签的添加、编辑和删除等。
- 采用`django-ckeditor`，文章和评论支持富文本编辑，内置编辑器插件，支持代码高亮。
- 完整的评论系统，包括发表回复评论，以及评论的邮件提醒功能。
- 首页通过`echarts`图表插件，可视化显示博客的访问量数据信息。
- 独立的点赞模块，能够给博客内容和评论信息进行点赞和取消点赞。
- 支持`redis`缓存，提高页面固定数据的加载速度，并定时自动刷新。
- 登录注册功能，具有登录、注册、找回密码等功能，并通过邮件完成注册验证。
- 博客后台异常邮件提醒，若服务器返回500错误将发送邮件通知管理员并附带错误信息。

### 如何使用

首先是创建虚拟环境，如果没有`virtualenv`，需要使用pip进行安装

```python3
pip install virtualenv
virtualenv mysite_env
```

启动虚拟环境，并查看是否与外界python环境隔离

```python
source mysite_env/bin/activate	# 激活虚拟环境
pip list	# 查看包是否纯净，若还有很多包表明环境未隔离
deactivate	# 退出虚拟环境
```

在虚拟环境中安装指定包，通过项目的需求包文件`requirements.txt`

```python
pip install -r requirements.txt	# 通过需求文件安装指定包
```

由于该项目使用mysql数据库和redis数据库，所以需要安装mysql和redis，若未安装，请参照网上教程进行安装，以下步骤默认是已安装好mysql、redis数据库的环境。

首先在mysql数据库中创建库，库名应与项目配置文件`settings.py`中设置一致，redis则需要将服务启动起来。

在`settings`文件夹中根据自己的设置修改以下内容，`development.py`是用于开发环境使用的配置文件，`production.py`这是生产环境使用的。

```python
# development.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mysitedb',	# 数据库名称
        'USER': 'zhangsan',	# 用户名称
        'PASSWORD': 'mima',	# 密码
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# 发送邮件设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'	# 发送邮件的服务器主机
EMAIL_PORT = 25
EMAIL_HOST_USER = '943446906@qq.com'	# 发送邮件的用户
EMAIL_HOST_PASSWORD = 'pujojuinumbdda'    #授权码
EMAIL_SUBJECT_PREFIX = '[王希知的博客]'
EMAIL_USE_TLS = True    # 与SMTP服务器通信时，是否启动TLS链接（安全链接）
SERVER_EMAIL = '943446906@qq.com'	# 用于服务器错误日志通知的发送方邮箱
ADMINS = (
    ('admin', 'welisit@qq.com'),	# 错误日志的接收方邮箱
)
```

配置完成后，就可以开始数据库迁移操作了，以下命令在虚拟环境下运行

```python
# 项目目录文件夹下
python manage.py makemigrations
python manage.py migrate
```

由于mysql数据库没有时区表信息，所以在进行时间分类时会无法查询到结果，这个问题需要手动插入时区表信息，具体可查看[官网](<https://docs.djangoproject.com/en/2.2/ref/databases/#time-zone-definitions>)。

然后就可以启动本地服务啦！

```python
python manage.py runserver
```

### 问题相关

有任何问题欢迎提Issue，或者将问题描述发送至我的邮箱`welisit#qq.com`.我会尽快解答，推荐提交Issue方式。

---

### 致大家:raising_hand_man::raising_hand_woman:

本项目参考自[HaddyYang](<https://github.com/HaddyYang/django2.0-course>)的博客项目教程，通过这个教程学到了很多东西，自己也在这基础上扩展了一些内容，比如redis数据库作为缓存等，后续还会不断更新和完善，由于目前技术能力有限，不足之处大家一起交流讨论哦 ！:bow::bow: ​





