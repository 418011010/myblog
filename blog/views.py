from django.db.models import F
from django.shortcuts import render
from django.http import HttpResponse ,JsonResponse
from .models import Article
from .models import Category, Banner, Article, Tag, Link, Cihai, Words, Niceday
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
import requests
import re
# Create your views here.


def global_variable(request):
    allcategory = Category.objects.all()
    remen = Article.objects.filter(tui__id=2)[:6]
    tags = Tag.objects.all()
    return locals()


def getprovince(ipaddr):
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"}
    url = 'http://ip.ws.126.net/ipquery?ip={}'.format(ipaddr)

    r = requests.get(url,headers = headers)
    #out = re.findall('localAddress={city:"荆门市", province:"湖北省"}',r.text)
    out = re.findall('province:"(.*?)"', r.text)
    # print(out)

    pr = {}
    pr.update(province=out[0])

    #return JsonResponse(pr,safe=False)
    return pr


def get_ip(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    return JsonResponse(getprovince(ip),safe=False)



def testdb(request):
    #ll = Niceday.objects.all().using('db2').filter(key3__contains='ang')[0:10]
    ll = Niceday.objects.all().using('db2').order_by('?').first()
    return HttpResponse(ll.sentence)


def wxpost(request):
    if request.POST.get('language') == 'Chinese':
        mapping = {'s': 'key1', 'd': 'key2', 't': 'key3', 'q': 'key4'}
        json_data = {}
        data_list = []
        key = mapping[request.POST.get('mult')]
        kw = request.POST.get('keyword')
        #print(kw)
        # items = Cihai.objects.all().using('db2').raw(
        #     "SELECT * from Cihai WHERE key1=(SELECT key1  from Cihai where binary words='一心一意')")
        items = Cihai.objects.all().using('db2').raw("SELECT * from Cihai WHERE {}=(SELECT {}  from Cihai where words='{}') and CHAR_LENGTH(words)={}".format(key, key, kw, len(kw)))
        #Cihai.objects.using('db2').update_or_create(words=kw, times=F('times') + 1, defaults={'words': kw},)
        #print(len(items))
        if len(items):
            Cihai.objects.using('db2').filter(words=kw).update(times=F('times') + 1)
            #print(len(items))
            #print(type(items))
            items = random.sample(list(items), 100 if len(items) > 100 else len(items))
            #print(len(items))
            for item in items:
                #print(type(item))
                data = {}
                data["words"] = item.words
                data["content"] = item.content
                data["yin"] = item.yin
                data["key"] = getattr(item, key)
                #data["key"] = item.key1
                data_list.append(data)
            json_data['data'] = data_list[:100]

            return JsonResponse(json_data)

            #return HttpResponse(a.raw_query)
        else:
            kw = re.sub("[A-Za-z0-9\!\%\[\]\,\。\ ]", "", kw)
            Cihai.objects.using('db2').update_or_create(words=kw[0:4], times=1, content='暂未收录', yin='zan wei shou lu', key1='u', key2='ou,u', key3='ei,ou,u', key4='an,ei,ou,u')
            json_data['data'] = [
                {
                    "words": kw,
                    "content": "暂未收录",
                    "yin": "zan wei shou lu",
                    "key": "an,ei,ou,u"
                },
            ]
            return JsonResponse(json_data)

    elif request.POST.get('language') == 'English':
        mapping = {'s': 'key1', 'd': 'key2', 't': 'key3', 'q': 'key4'}
        json_data = {}
        data_list = []
        key = mapping[request.POST.get('mult')]
        kw = request.POST.get('keyword')
        #print(kw)
        # items = Cihai.objects.all().using('db2').raw(
        #     "SELECT * from Cihai WHERE key1=(SELECT key1  from Cihai where binary words='一心一意')")
        items = Words.objects.all().using('db2').raw(
            "SELECT * from Words WHERE {}=(SELECT {}  from Words where binary word='{}') ".format(key, key, kw))
        # print(len(items))
        # print(type(items))
        if len(items):
            Words.objects.using('db2').filter(word=kw).update(times=F('times') + 1)
            items = random.sample(list(items), 100 if len(items) > 100 else len(items))
            #print(len(items))
            for item in items:
                # print(type(item))
                data = {}
                data["words"] = item.word
                data["content"] = item.ch
                data["yin"] = item.pron
                data["key"] = getattr(item, key)
                # data["key"] = item.key1
                data_list.append(data)
            json_data['data'] = data_list[:100]

            return JsonResponse(json_data)
            #return HttpResponse(ll.values())
        else:
            return JsonResponse({'data': [{
                "words": kw,
                "content": "暂未收录",
                "yin": "",
                "key": ""
                }]}, safe=False)
    else:
        return HttpResponse("出错了哦~")


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
    allarticle = Article.objects.all().order_by('-id')[0:10]#通过Category表查出所有分类
    #把查询出来的分类封装到上下文里
    banner = Banner.objects.filter(is_active=True)[0:4]  # 查询所有幻灯图数据，并进行切片
    tui = Article.objects.filter(tui__id=1)[:3]
    #hot = Article.objects.all().order_by('?')[:10]#随机推荐
    #hot = Article.objects.filter(tui__id=3)[:10]   #通过推荐进行查询，以推荐ID是3为例
    hot = Article.objects.all().order_by('views')[:10]#通过浏览数进行排序
    link = Link.objects.all()


    return render(request, 'index.html', locals())#把上下文传到index.html页面

#列表页
def listx(request,lid):
    list = Article.objects.filter(category_id=lid).order_by('-id')#获取通过URL传进来的lid，然后筛选出对应文章
    cname = Category.objects.get(id=lid)#获取当前文章的栏目名


    page = request.GET.get('page')  # 在URL中获取当前页面数
    paginator = Paginator(list, 5)  # 对查询到的数据对象list进行分页，设置超过5条数据就分页
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'list.html', locals())

#内容页
def show(request,sid):
    show = Article.objects.get(id=sid)#查询指定ID的文章

    hot = Article.objects.all().order_by('?')[:10]#内容下面的您可能感兴趣的文章，随机推荐
    previous_blog = Article.objects.filter(created_time__gt=show.created_time,category=show.category.id).first()
    netx_blog = Article.objects.filter(created_time__lt=show.created_time,category=show.category.id).last()
    show.views = show.views + 1
    show.save()
    return render(request, 'show.html', locals())

#标签页
def tag(request, tag):
    list = Article.objects.filter(tags__name=tag).order_by('-id')

    tname = Tag.objects.get(name=tag)#获取当前搜索的标签名
    page = request.GET.get('page')

    paginator = Paginator(list, 5)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'tags.html', locals())


# 搜索页
def search(request):
    ss=request.GET.get('search')#获取搜索的关键词
    list = Article.objects.filter(title__icontains=ss)#获取到搜索关键词通过标题进行匹配

    page = request.GET.get('page')

    paginator = Paginator(list, 10)
    try:
        list = paginator.page(page) # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1) # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages) # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'search.html', locals())


# 关于我们
def about(request):

    return render(request, 'page.html',locals())

