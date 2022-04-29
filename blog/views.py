from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import CommentForm
from .models import Post, Category, Tag


# Create your views here.
# def index(request):
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(request,
#                   'blog/post_list.html',
#                   {
#                       'posts': posts,
#
#                   })


# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#     return render(request,
#                   'blog/post_detail.html',
#                   {
#                       'post': post,
#                   }
#                   )
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = [ 'title', 'content', 'hook_msg', 'head_image', 'attached_file', 'category']
    template_name = "blog/post_form_update.html"

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated and current_user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else :
            raise PermissionDenied

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = [ 'title', 'content', 'hook_msg', 'head_image', 'attached_file', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user

        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author =current_user
            return super(PostCreate, self).form_valid(form)
        else :
            return redirect('/blog')
class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['count_posts_without_category'] = Post.objects.filter(category=None).count()

        return context

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['count_posts_without_category'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm

        return context


def show_category_posts(request, slug):
    if slug == 'no-category':   # 미분류 글 요청
        category = '미분류'
        post_list = Post.objects.filter(category=None)

    else:
        category = Category.objects.get(slug = slug)
        post_list = Post.objects.filter(category=category)

    context = {
        'categories' : Category.objects.all(),
        'count_posts_without_category' : Post.objects.filter(category=None).count(),
        'category' : category,
        'post_list': post_list
    }

    return render(request, 'blog/post_list.html', context)


def show_tag_posts(request, slug):

    tag = Tag.objects.get(slug = slug)
    post_list = tag.post_set.all()

    context = {
        'categories' : Category.objects.all(),
        'count_posts_without_category' : Post.objects.filter(category=None).count(),
        'tag' : tag,
        'post_list': post_list
    }

    return render(request, 'blog/post_list.html', context)


def addComment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(comment.get_absolute_url())

        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied
