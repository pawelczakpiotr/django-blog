from django.shortcuts import render, get_object_or_404
from blog.models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from blog.forms import EmailPostForm, CommentForm
from django.core.mail import send_mail

# Create your views here.


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month, publish__day=day)

    comments = post.comments.filter(active=True)
    added = False

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            added = True
    else:
        comment_form = CommentForm()

    values_dict = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'added': added,
    }

    return render(request, 'blog/post/detail.html', values_dict)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} ({cd['email']}) zacheca do przeczytania \"{post.title}\" "
            message = f'Przeczytaj post "{post.title}" na stronie {post_url}\n\nKomentarz dodany przez {cd["name"]}: {cd["comments"]}'
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})