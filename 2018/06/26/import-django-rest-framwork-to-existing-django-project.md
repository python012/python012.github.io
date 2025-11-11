---
title: "为Django项目应用Django REST framework实现REST风格的Web API"
date: 2018-06-26
tags:
  - Python
  - Django
  - Django Rest Framework
description: "Django REST framework实现的REST风格的Web API，同时又可以用浏览器进行查看，一个快速的例子就是https://restframework.herokuapp.com/users/，Django官方提供的一个范例，简洁明了，Django REST framework这套框架可以帮助Django项目快速实现REST风格的API，十分Pythonic。 假如基于Django"
---

# 为Django项目应用Django REST framework实现REST风格的Web API

<div class="article-meta">
  <span class="date">📅 发布于：2018年06月26日</span>
  <span class="tags">🏷️ 标签：<span class="tag">Python</span> <span class="tag">Django</span> <span class="tag">Django Rest Framework</span></span>
</div>

Django REST framework实现的REST风格的Web API，同时又可以用浏览器进行查看，一个快速的例子就是[https://restframework.herokuapp.com/users/]，Django官方提供的一个范例，简洁明了，Django REST framework这套框架可以帮助Django项目快速实现REST风格的API，十分Pythonic。

假如基于Django已经实现了一个简单的Web项目（项目中实现了一个app，名为api，`./project_name/api/models.py`中已经定义了api中用到的model数据表`class Person(models.Model)`）。

STEP 1- 首先去`./project_name/project_name/settings.py`，在INSTALLED_APPS中添加rest_framework：

```properties
INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'api',
'bootstrap3',
'rest_framework',
]

```text

STEP 2- 创建`./project_name/api/serializers.py`，基本代码如下：

```yaml
fromdjango.contrib.auth.modelsimportUser, Group
fromrest_frameworkimportserializers
fromapi.modelsimportPerson

classUserSerializer(serializers.HyperlinkedModelSerializer):
classMeta:
model = User
fields = ('url','username','email','groups')

classGroupSerializer(serializers.HyperlinkedModelSerializer):
classMeta:
model = Group
fields = ('url','name')

classPersonSerializer(serializers.HyperlinkedModelSerializer):
classMeta:
model = Person
fields = ('name','address','status')

```text

STEP 3- 创建`./project_name/api/view_interface_rest.py`，基本代码如下：

```python
fromdjango.contrib.auth.modelsimportGroup, User
fromrest_frameworkimportviewsets

fromapi.modelsimportPerson
fromapi.serializersimportGroupSerializer, UserSerializer, PersonSerializer

classUserViewSet(viewsets.ModelViewSet):
"""
API endpoint that allows users to viewed or edited.
"""
queryset = User.objects.all().order_by('-date_joined')
serializer_class = UserSerializer

classGroupViewSet(viewsets.ModelViewSet):
"""
API endpoint that allows groups to viewed or edited.
"""
queryset = Group.objects.all()
serializer_class = GroupSerializer

classPersonViewSet(viewsets.ModelViewSet):
"""
API endpoint that allows events to viewed or edited.
"""
queryset = Person.objects.all()
serializer_class = PersonSerializer

```text

STEP 4- 打开`./project_name/perject_name/urls.py`，添加REST API的路由信息，代码如下：

```properties
fromdjango.conf.urlsimporturl, include
fromdjango.contribimportadmin
fromapiimportviews, views_interface_rest

fromrest_frameworkimportrouters

router = routers.DefaultRouter()
router.register(r'users', views_interface_rest.UserViewSet)
router.register(r'groups', views_interface_rest.GroupViewSet)
router.register(r'persons', views_interface_rest.EventViewSet)

urlpatterns = [
url(r'^admin/', admin.site.urls),
url(r'^$', views.index),
url(r'^index/$', views.index),
url(r'^login_action/$', views.login_action),
url(r'^accounts/login/$', views.index),
url(r'^logout/$', views.logout),

url(r'^rest/', include(router.urls)),
url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

```text

THE END- 此时代码工作应该是完成了，登陆访问`http://127.0.0.1:8000/rest/`就可以打开api root的页面，使用PostMan或者HTTPie等工具向`http://127.0.0.1:8000/rest/`发送GET请求，同时带上basic auth的用户名密码，就能拿到类似如下的response。

```text
rx:guest reed$ http -a admin:password http://127.0.0.1:8000/rest/
HTTP/1.1 200 OK
Allow: GET, HEAD, OPTIONS
Content-Length: 183
Content-Type: application/json
Date: Wed, 27 Jun 2018 01:17:15 GMT
Server: WSGIServer/0.2 CPython/3.6.5
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
"persons":"http://127.0.0.1:8000/rest/persons/",
"groups":"http://127.0.0.1:8000/rest/groups/",
"users":"http://127.0.0.1:8000/rest/users/",
}

```