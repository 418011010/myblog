from django.shortcuts import render
from django.http import HttpResponse
from .models import Article
from .models import Category, Banner, Article, Tag, Link

# Create your views here.


def showlist(request):
    #添加两个变量，并给它们赋值
    sitename = 'Django中文网'
    url = 'www.django.cn'
    #把两个变量封装到上下文里

    list = [
        '开发前的准备',
        '项目需求分析',
        '数据库设计分析',
        '创建项目',
        '基础配置',
        '欢迎页面',
        '创建数据库模型',
    ]


    mydict={
        'name': '吴秀峰',
        'qq': '445813',
        'wx': 'vipdjango',
        'email': '445813@qq.com',
        'Q群': '10218442',
    }

    context = {
        'sitename': sitename,
        'url': url,
        'list': list,
        'mydict': mydict,
    }
    #把上下文传递到模板里
    return render(request, 'showlist.html', context)


def bkindex(request):
    #对Article进行声明并实例化，然后生成对象allarticle
    allarticle = Article.objects.all()
    #把查询到的对象，封装到上下文
    context = {
        'allarticle': allarticle,
    }
    #把上传文传到模板页面index.html里
    return render(request, 'bkindex.html', context)

def index(request):
    allcategory = Category.objects.all()#通过Category表查出所有分类
    #把查询出来的分类封装到上下文里
    banner = Banner.objects.filter(is_active=True)[0:4]  # 查询所有幻灯图数据，并进行切片
    tui = Article.objects.filter(tui__id=1)[:3]
    #hot = Article.objects.all().order_by('?')[:10]#随机推荐
    #hot = Article.objects.filter(tui__id=3)[:10]   #通过推荐进行查询，以推荐ID是3为例
    hot = Article.objects.all().order_by('views')[:10]#通过浏览数进行排序
    remen = Article.objects.filter(tui__id=2)[:6]
    tags = Tag.objects.all()
    link = Link.objects.all()

    context = {
            'allcategory': allcategory,
            'banner': banner,  # 把查询到的幻灯图数据封装到上下文
            'tui':tui,
            'hot': hot,
            'remen': remen,
            'tags': tags,
            'link': link,
        }
    return render(request, 'index.html', context)#把上下文传到index.html页面

#列表页
def list(request,lid):
    pass

#内容页
def show(request,sid):
    pass

#标签页
def tag(request, tag):
    pass

# 搜索页
def search(request):
    pass
# 关于我们
def about(request):
    pass

