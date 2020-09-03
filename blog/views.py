from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Book
from itertools import chain
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from comment.forms import CommentForm
from django.contrib import messages
from comment.models import Comment


class SearchView(ListView):
    template_name = 'blog/search.html'
    paginate_by = 30
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            blog_results = Book.objects.search(query)

            # combine querysets
            queryset_chain = chain(
                blog_results,
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs)  # since qs is actually a list
            return qs
        return Book.objects.none()  # just an empty queryset as default


def book_search(request):
    books_list = Book.objects.none()
    query = request.GET.get('q')
    if query:
        books_list = Book.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()
    paginator = Paginator(books_list, 10)  # 6 posts per page
    page = request.GET.get('page')

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
        'books': books
    }
    return render(request, "blog/search_copy.html", context)


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def post_detail(request, pk):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, pk=pk)

    comments = post.comment_set.all()

    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        comment_form.instance.post = post
        reply_id = request.POST.get('comment_id')
        if reply_id:
            comment_qs = Comment.objects.get(id=reply_id)
            comment_form.instance.reply = comment_qs
        comment_form.instance.author = request.user
        if comment_form.is_valid():
            comment_form.save()
            messages.success(request, f'评论已提交。')
            return redirect(f'/post/{pk}')

    else:
        comment_form = CommentForm()

    return render(request, template_name, {'object': post,
                                           'comments': comments,
                                           'comment_form': comment_form})

def book_detail(request, pk):
    template_name = 'blog/book_detail.html'
    book = get_object_or_404(Book, pk=pk)
    return render(request, template_name, {'object': book,})