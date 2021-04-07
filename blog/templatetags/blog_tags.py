from django import template
from blog.models import Post
from django.db.models import Count
import markdown
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    posts = Post.published.all()
    posts = posts.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return posts


@register.filter
def markdown_format(text):
    return mark_safe(markdown.markdown(text))