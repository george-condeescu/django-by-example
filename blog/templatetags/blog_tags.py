from django import template
from django.utils import timezone
from django.db.models import Count
from django.utils.safestring import mark_safe
from markdown import markdown

register=template.Library()

from ..models import Post

@register.simple_tag
def total_posts():
    return Post.published.count()

@register.simple_tag
def current_time(format_string):
    return timezone.datetime.now().strftime(format_string)

@register.inclusion_tag('latest_posts.html')
def show_latest_posts(count=5):
    latest_posts=Post.published.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}

@register.simple_tag
def get_most_commented_posts():
    return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:3]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown(text))

