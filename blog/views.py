# from django.shortcuts import render, get_object_or_404
# from .models import Post, Comment
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.views.generic import ListView
# from .forms import EmailPostForm, CommentForm
# from django.core.mail import send_mail

# # Create your views here.
# class PostListView(ListView): 
# 	queryset = Post.published.all()
# 	context_object_name = 'posts'
# 	paginate_by = 2
# 	template_name = 'blog/post/list.html'

# # def post_list(request):
# # 	object_list = Post.published.all()
# # 	paginator = Paginator(object_list, 2) # По 2 статьи на каждой странице
# # 	page = request.GET.get('page')

# # 	try:
# # 		posts = paginator.page(page)
# # 	except PageNotAnInteger:
# # 		# Если страница не является целым числом, возвращаем первую страницу.
# # 		posts = paginator.page(1)
# # 	except EmptyPage:
# # 		# Если номер страницы больше, чемобщее количество страниц, возвращаем последнюю
# # 		posts = paginator.page(paginator.num_pages)
# # 	# posts = Post.published.all()
# # 	return render(request, 'blog/post/list.html', {'posts': posts})

# def post_detail(request, year, month, day, post):
# 	post = get_object_or_404(Post, slug=post, status='published', publish__year = year,
# 			publish__month=month, publish__day=day
# 		)
# 	#Список активных комментариев для этой статьи
# 	#Добавили обработчик QuerySet для получения всех активных комментариев
# 	comments = post.comments.filter(active=True)
# 	new_comment = None
# 	if request.method == 'POST':
# 		#Пользователь отправил комментарий
# 		comment_form = CommentForm(data = request.POST)

# 		if comment_form.is_valid():
# 			#Создаем комментарий но пока не сохраняем в базе данных
# 			new_comment = comment_form.save(commit = False)
# 			#Привязываем комментарий к текущей статье
# 			new_comment.post = post
# 			#Сохраняем комментарий в базе данных
# 			new_comment.save()
# 		else:
# 			comment_form = CommentForm()

# 	return render(request, 'blog/post/detail.html', 
# 			{   
# 				'post': post,
# 				'comments': comments,
# 				'new_comment': new_comment,
# 				'comment_form': comment_form,

# 			}
# 		)


# def post_share(request, post_id):
#     # Retrieve post by id
#     post = get_object_or_404(Post, id=post_id, status='published')
#     sent = False 
 
#     if request.method == 'POST':
#         # Form was submitted
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             # Form fields passed validation
#             cd = form.cleaned_data
#             post_url = request.build_absolute_uri(
#                                           post.get_absolute_url())
#             subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
#             message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
#             send_mail(subject, message, 'admin@myblog.com',
#  [cd['to']])
#             sent = True
#     else:
#         form = EmailPostForm()
#     return render(request, 'blog/post/share.html', {'post': post,
#                                                     'form': form,
#                                                     'sent': sent})

from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чемобщее количество страниц, возвращаем последнюю
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    
    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    # List of similar posts
    # post_tags_ids = post.tags.values_list('id', flat=True)
    # similar_posts = Post.published.filter(tags__in=post_tags_ids)\
    #                               .exclude(id=post.id)
    # similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                # .order_by('-same_tags','-publish')[:4]

    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form,
                   # 'similar_posts': similar_posts,
                   }
                   )

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False 
 
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                                          post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com',
 [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
