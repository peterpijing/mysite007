#coding=utf-8
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render,render_to_response
from models import Post

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.template import RequestContext
# def post_list(request):
#     # """所有已发布文章"""
#     # # postsAll = Post.objects.annotate(num_comment=Count('comment')).filter(
#     # #     published_date__isnull=False).prefetch_related(
#     # #     'category').prefetch_related('tags').order_by('-published_date')
#     # postsAll = Post.objects.all()
#     # # for p in postsAll:
#     # #     p.click = cache_manager.get_click(p)
#     # paginator = Paginator(postsAll, 3)  # Show 10 contacts per page
#     # page = request.GET.get('page')
#     # try:
#     #     posts = paginator.page(page)
#     # except PageNotAnInteger:
#     #     # If page is not an integer, deliver first page.
#     #     posts = paginator.page(1)
#     # except EmptyPage:
#     #     # If page is out of range (e.g. 9999), deliver last page of results.
#     #     posts = paginator.page(paginator.num_pages)
#
#     posts = Post.objects.all()
#     # return render(request, 'blog/post_list.html', {'posts': posts})
#
#     return render_to_response('blog/post_list.html', {'posts': posts})

from django.contrib.auth.decorators import login_required


def post_list(request):
    posts = Post.objects.filter(published_date__isnull= False).order_by('-published_date')
    # posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

from django.shortcuts import get_object_or_404
def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


from forms import PostForm
# def post_new(request):
#     form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog:post_detail', pk=pk)

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:post_index')


#搜索定义
from haystack.forms import SearchForm
def full_search(request):
    """全局搜索"""
    keywords = request.GET['q']
    sform = SearchForm(request.GET)
    posts = sform.search()
    return render(request, 'blog/post_search_list.html',
                  {'posts': posts, 'list_header': '关键字 \'{}\' 搜索结果'.format(keywords)})
