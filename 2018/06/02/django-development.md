---
title: "Django development实践笔记"
date: 2018-06-02
tags:
  - Python
  - Django
description: "买到一本有趣的关于Django开发和接口测试的书，写的很棒，这里随手记录以下Django开发的要点。 项目的启动 推荐用Python 3.x，pip install django==1.10.3. 安装成功后，如果django-admin程序在PATH目录的话，运行django-admin可以看到命令列表。 执行django-admin guest来创建一个叫guest的项目。 进入guest目录"
---

# Django development实践笔记

<div class="article-meta">
  <span class="date">📅 发布于：2018年06月02日</span>
  <span class="tags">🏷️ 标签：<span class="tag">Python</span> <span class="tag">Django</span></span>
</div>

买到一本有趣的关于Django开发和接口测试的书，写的很棒，这里随手记录以下Django开发的要点。

## 项目的启动

- 推荐用Python 3.x，`pip install django==1.10.3`.
- 安装成功后，如果django-admin程序在PATH目录的话，运行`django-admin`可以看到命令列表。
- 执行`django-admin guest`来创建一个叫guest的项目。
- 进入guest目录，执行`python3 manage.py`来查看manage所提供的命令列表。
- 执行`python3 manage.py startapp appname`，创建一个app，名为`appname`。

## Django中的app

Django框架下的Web开发有很多有意思的概念，比如这个app概念，我理解就是完成一个比较独立的功能的模块。

创建了名为`appname`的app后，会有appname目录生成，其中会有以下文件或者目录：

- migrations/  用来记录modles中的数据变更
- admin.py     映射modles中的数据到Django自带的admin后台
- apps.py      用于app的配置
- modles.py    Django模型文件，创建app的数据表模型，对应数据库的相关操作
- tests.py     创建测试用例
- views.py     Django的视图文件，控制向前段页面显示的内容
- templates/   用来放HTML模版文件

app创建之后，还需要去项目目录下的`settings.py`，把app名字添加到`INSTALLED_APPS`中。

## 一次具体的网站页面访问到底是怎样一个过程呢？

假设有一个登陆后可以看到图片列表的网站，现在开始打开浏览器，输入`http://localhost/login/`敲回车开始访问，这里我尝试用在Django框架里发生的一系列事件来解释下这个过程。

- Django框架下的服务器程序会接受到一个针对`/login/`的HTTP GET request。
- Django会依据项目目录下的`urls.py`中的`urlpatterns`(如下)来查找/login/所绑定的视图函数。

```python
urlpatterns = [
  url(r'^admin/', admin.site.urls),
  url(r'^$', views.login),
  url(r'^login/$', views.login),
  url(r'^login_action/$', views.login_action),
  url(r'^image_list/$', views.image_list),
]
```

查找后发现/login/绑定的是函数`views.login(request)`(存在于`/appname/views.py`)，然后会把这个http request对象作为参数传给`views.login(request)`。
函数`views.login(request)`的内容如下，它会返回index.html文件，这是事先写好放在`/appname/templates`目录里的。没有学习Web开发之前，可能会认为URL名字总是有相应的HTML文件，实际在Django Web开发中却不是这样的。


```python
deflogin(request):
  return render(request,"index.html")
```

`index.html`中的内容会呈现在浏览器中，此刻浏览器的地址栏还是`http://localhost/login/`。这里需要说下`index.html`，源文件中多半有下面这样的代码.


```html
<form class="center" action="/login_action/" method="POST">
<input type="text" name="username" placeholder="username">
<br>
<input type="password" name="password" placeholder="password">
<br> {{ error_message }}
<br>
<button id="btn" type="submit">登录</button>
</form>
```


填写用户名和密码，并提交的页面元素是一个`form`，填好后点击按钮，form里定义的`action="/login_action/" method="POST"`，决定了填好的这些username和password信息，是向`http://localhost/login_action/`提交(POST方法)。这里的`error_message`和`csrf_token`，一个是预备载入错误信息的地方，一个是django中的防止跨站请求伪造的token，先不展开了。

然后就重复之前的步骤，服务器会从`urls.py`中查找路径/login_action/所绑定的视图函数，这里是`views.login_action`，然后把http request对象传过去作为参数。来看下`login_action()`函数的细节


```python
def login_action(request):
  ifrequest.method =='POST':
  username = request.POST.get('username','')
  password = request.POST.get('password','')
  user = auth.authenticate(username=username, password=password)

  if userisnotNone:
    auth.login(request, user)
    request.session['user'] = username
    response = HttpResponseRedirect('/image_list/')
    return response
  else:
    return render(request,'index.html', {'error_message':'username or password is not correct!'})
```


如果`login_action()`函数收到的http request是一个POST，就会从rquest中解析出username/password信息，然后用Django提供的通用认证方法进行检查，如果一切ok，user变量就不为空，然后把request session中的user置为username的值(刚刚由request中解析出来)，再把request重定向到`/image_list/`。

- 再一次重复上面的步骤，服务器会从`urls.py`中查找路径`/image_list/`所绑定的视图函数，此处是`views.image_list`，然后把http request对象传过去作为参数。
- 看一下`views.image_list(request)`函数：

```python
@login_required
def image_list(request):
  username = request.session.get('user','')
  image_list = Image.objects.all()
  return render(request,"image_list.html", {"user": username,"images": image_list})
```

`views.image_list`收到http request后，先从session中获得user变量的值，也即最开始用户登陆的时候输入的用户名，再从系统中的Image modle(定义在项目根目录的models.py里)获取到所有的Image对象列表(这里有很多Django的辅助实施)，然后把user变量的值，和Image对象列表组成一个字典(或可称为json串?)传给`/appname/templates`里image_list.html，Django会使用字典作为参数对html文件进行加工，比如把user变量的值放在网页右上角显示为`欢迎 User`,然后依据Image对象列表找到所有Image的地址，生成一些列li标签，每个li带一个image，最后看起来像一个相册。

最后浏览器的地址栏会停留在`http://localhost/image_list/`，浏览器的主页面会显示经过Django处理过的，以image_list.html为模板的网页。

最后一点题外话，发现hexo似乎有个bug，blog的md文本中里不能出现用`%{`包围的csrf_token，否则会`hexo s`失败，报错`Template render error: unknown block tag: csrf_token`，所以文中引用的第一段HTML代码中button tag下原本是有csrf_token的。