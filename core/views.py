from django.db.models import Count,Q
from django.shortcuts import render,get_object_or_404,reverse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Post,Comments,Author
from .forms import CommentForm,PostForm
import datetime

def get_author(user):
    qs=Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


def get_category_count():
    query_set=Post.objects.values('category').annotate(Count('category'))
    return query_set


def search(request):
    queryset=Post.objects.all()
    query=request.GET.get("q")
    if query:
        queryset=queryset.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()
    context={
        'queryset':queryset,
    }
    return render(request,"search.html",context)



def Home(request):
    category_count=get_category_count()
    feature=Post.objects.filter(featured=True)
    timestamp=Post.objects.order_by('-timestamp')[0:3]
    timestamp2=Post.objects.order_by('timestamp')[0:3]
    slider=Post.objects.filter(slider=True)
    popular=Post.objects.order_by('-read')[:5]
    week_ago=datetime.date.today()-datetime.timedelta(days=7)
    trends=Post.objects.filter(timestamp__gte=week_ago).order_by('-read')
    paginator=Paginator(feature,3)
    page_request_var='page'
    page=request.GET.get(page_request_var)
    try:
        paginator_queryset=paginator.page(page)
    except PageNotAnInteger:
        paginator_queryset=paginator.page(1)
    except EmptyPage:
        paginator_queryset=paginator.page(paginator.num_pages)
    context={
        'trends':trends[:3],
        'popular':popular,
        'search_section':True,
        'post_section1':False,
        'page_request_var':page_request_var,
        'queryset':paginator_queryset,
        'latest':timestamp,
        'older':timestamp2,
        'slider':slider,
        'category_count':category_count,
    }
    return render(request,"home.html",context)


def blog(request,id):
    category_count=get_category_count()
    timestamp=Post.objects.order_by('-timestamp')[0:3]
    timestamp2=Post.objects.order_by('timestamp')[0:3]
    post=get_object_or_404(Post,id=id)
    popular=Post.objects.order_by('-read')[:5]
    week_ago=datetime.date.today()-datetime.timedelta(days=7)
    trends=Post.objects.filter(timestamp__gte=week_ago).order_by('-read')
    # if request.user.is_authenticated:
    #     PostView.objects.get_or_create(user=request.user,post=post)
    form=CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user=request.user
            form.instance.post=post
            form.save()
            return redirect(reverse("page",kwargs={
                'id':post.id
            }))

    context={
        'trends':trends[:3],
        'popular':popular,
        'category_count':category_count,
        'form': form,
        'post_section1':True,
        'latest':timestamp,
        'older':timestamp2,
        'post':post,
    }
    return render(request,"post-page.html",context)


def Post_list(request):
    category_count=get_category_count()
    timestamp=Post.objects.order_by('-timestamp')[0:3]
    timestamp2=Post.objects.order_by('timestamp')[0:3]
    popular=Post.objects.order_by('-read')[:5]
    post=Post.objects.all().order_by('-timestamp')
    week_ago=datetime.date.today()-datetime.timedelta(days=7)
    trends=Post.objects.filter(timestamp__gte=week_ago).order_by('-read')[0:3]
    paginator=Paginator(post,8)
    page_request_var='page'
    page=request.GET.get(page_request_var)
    try:
        post=paginator.page(page)
    except PageNotAnInteger:
        post=paginator.page(1)
    except EmptyPage:
        post=paginator.page(paginator.num_pages)
    context={
        'trends':trends,
        'popular':popular,
        'category_count':category_count,
        'post_section1':False,
        'page_request_var':page_request_var,
        'post':post,
        'latest':timestamp,
        'older':timestamp2,
    }
    return render(request,"post_list.html",context)


def post_update(request,id):
    title='Update'
    post=get_object_or_404(Post,id=id)
    form=PostForm(request.POST or None ,request.FILES or None,instance=post)
    author=get_author(request.user)
    if request.method=="POST":
        if form.is_valid():
            form.instance.author=author
            form.save()
            return redirect("/")
    context={
        'form':form,
        'title':title,
    }
    return render(request,"post_create.html",context)


def post_delete(request,id):
    pass