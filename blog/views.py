from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, FormView, CreateView, TemplateView, UpdateView, DeleteView
from taggit.models import Tag

from blog.models import Post

### Widoki funkcyjne
from blog.forms import EmailPostForm, CommentForm, PostUpdateForm


@login_required()
def home(request):
    return render(request, "blog/home.html", {})


@login_required()
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'page': page, 'tag': tag})


@login_required()
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    comments = post.comments.filter(active=True)
    new_comment = ""
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'comment_form': comment_form,
                                                     'new_comment': new_comment,
                                                     'similar_posts': similar_posts})


@login_required()
def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) zachęca do przeczytania "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Przeczytaj post "{}" na stronie {}\n\n Komentarz dodany przez {}:' \
                      '{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def post_update(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    form = PostUpdateForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog:post_list')
    return render(request, 'blog/post/update_post.html', {"form": form})


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if "POST" in request.method:
        post.delete()
        return redirect("blog:post_list")
    return render(request, "blog/confirmation_to_delete.html", {'object': post})


















### Widoki oparte na klasach bazowych Django


@method_decorator(login_required, name="dispatch")
class HomepageView(TemplateView):
    template_name = "blog/home.html"


@method_decorator(login_required, name="dispatch")
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


@method_decorator(login_required, name="dispatch")
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post/detail.html'


@method_decorator(login_required, name="dispatch")
class PostShareView(FormView):
    form_class = EmailPostForm
    template_name = "blog/post/share.html"
    extra_context = {'sent': False}

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            cd = form.cleaned_data
            post = get_object_or_404(Post, pk=self.kwargs['post_id'], status='published')

            post_url = self.request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) zachęca do przeczytania "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Przeczytaj post "{}" na stronie {}\n\n Komentarza dodany przez {}:' \
                      '{}'.format(post.title, post_url, cd['name'], cd['comments'])

            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            self.extra_context['sent'] = True
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['post_id'], status='published')
        return context

    def get_success_url(self):
        return reverse("blog:post_share", kwargs={'post_id': self.kwargs['post_id']})


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse("blog:post_list")


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'body']
    template_name = "blog/post/update_post.html"


class DeletePostView(DeleteView):
    model = Post
    template_name = "blog/confirmation_to_delete.html"
    success_url = reverse_lazy('blog:post_list')
