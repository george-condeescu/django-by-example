from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView, DetailView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.conf import settings
from taggit.models import Tag
from django.db.models import Count

# Create your views here.
def post_list(request, tag_slug=None):
    object_list=Post.objects.all()
    tag=None

    if tag_slug:
        tag=get_object_or_404(Tag, slug=tag_slug)
        object_list=object_list.filter(tags__in=[tag])

    paginator=Paginator(object_list,2)
    page=request.GET.get('page') # numarul paginii
    print(page)
    try:
        posts=paginator.page(page)
    except EmptyPage:
        # page is out of range deliver last page
        posts=paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # if page is not an integer deliver fist page
        posts=paginator.page(1)
    return render(request, 'list.html', {'page':page, 'posts':posts, 'tag':tag})

# o alternativa la post_list view este folosirea unei generic view
# class PostListView(ListView):
#     queryset=Post.objects.all()
#     paginate_by=2
#     context_object_name='posts'
#     template_name='list.html'


def post_detail(request, year, month, day, slug):
    post=get_object_or_404(Post,    slug=slug,  
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day
                            )
    # list of active comments for this post
    comments=post.comments.filter(active=True)

    if request.method=='POST':
        # a comment was posted
        comment_form=CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create Comment object but don't save to database yet
            new_comment=comment_form.save(commit=False)
            # assign the current post to the comment
            new_comment.post=post
            # save the comment to the database
            new_comment.save()

    else:
        comment_form=CommentForm()
    # lista de similar posts
    post_tags_ids=post.tags.values_list('id', flat=True) # obtin id-urile tuturor tag-urilor
    similar_posts=Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts=similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'detail.html', {'post':post, 'comments':comments, 'comment_form':comment_form, 'similar_posts':similar_posts})

def post_share(request, post_id):
    post=get_object_or_404(Post, id=post_id, status='published')
    sent=False
    if request.method=='POST':
        # form was submitted
        form=EmailPostForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject='{} ({}) recommends yor reading "{}'.format(cd['name'], cd['email'], post.title)
            message='Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'george.condeescu@gmail.com', ['george_condeescu@yahoo.com'], fail_silently=False)
            sent=True
    else:
        # form was get
        form=EmailPostForm()
    return render(request, 'share.html', {'post':post, 'form':form, 'sent':sent})



