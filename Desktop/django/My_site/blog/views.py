from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.postgres.search import (SearchVector, SearchQuery, SearchRank) 
from django.db.models import Count
from taggit.models import Tag
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from .models import FavouritePost, Post
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.views.decorators.http import require_POST




def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)

            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),
                search=search_vector,
                rank=SearchRank(search_vector, search_query)

            ).filter(similarity__gt=0.3).order_by('-similarity')
            
    return render(
        request, 
        'blog/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        }
    )



@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    # A comment was posted.
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database.
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        comment.save()
    return render (
        request,
        'blog/post/comment.html',
        {
            'post':post,
            'form': form,
            'comment': comment
        },
    )


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} ({cd['email']}) recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']} comments: {cd['comments']}"
            
            send_mail(subject, message, None, [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 3)  # 3 posts per page
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        #  If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)  
    except EmptyPage:
            # IF page_number is out of range get last page of results.
            posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {
            "posts": posts,
            "tag":tag
         }
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment 
    form = CommentForm()

    # List of similar Posts.

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags').order_by)('-same_tags', '-publish')[:4]
    # Slice the result to retrieve the first 4 posts.

    return render(
        request,
        'blog/post/detail.html',
        {
            'comments': comments,
            'post': post,
            'form': form,
            'similar_posts':similar_posts
        }
    )


@login_required
def add_favourite(request, id):
    """Add a post to favourites. Redirect to post detail."""
    post = get_object_or_404(Post, id=id)
    FavouritePost.objects.get_or_create(
        user=request.user, post=post
    )
    return HttpResponseRedirect(post.get_absolute_url())


@login_required
def favourites(request):
    """List all favourite posts."""
    favourite_posts = Post.objects.filter(
        id__in=FavouritePost.objects.filter(
            user=request.user
        ).values_list('post_id', flat=True)
    )
    return render(
        request,
        'blog/post/favourites.html',
        {'favourite_posts': favourite_posts}
    )
class PostListView(ListView):
     """ Alternative post list view"""
     queryset = Post.published.all()
     context_object_name = 'posts'
     paginate_by = 3
     template_name = 'blog/post/list.html'