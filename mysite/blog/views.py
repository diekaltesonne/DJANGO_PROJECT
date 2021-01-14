from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm
from .models import Post, Comment
from taggit.models import Tag

def post_list(request, tag_slug = None):
    object_list = Post.published.all()
    tag = None 

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    
    paginator = Paginator(object_list, 3) # По 3 статьи на каждой странице.
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        posts = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        posts = paginator.page(paginator.num_pages)
    return render(request,'blog/post/list.html', {'page': page, 'posts': posts,'tag': tag})
    
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',publish__year=year,
                            publish__month = month,publish__day=day)
    # Список вктивных комментарие для этой статьи
    comments = post.comments.filter(active = True)
    new_comment = None
    if request.method == 'POST':
        # Пользователь отправил комментарий
        comment_form = CommentForm(data = request.POST)
        if comment_form.is_valid():
            # Создаем комментарий, но пока не сохраняем в базе данных.
            new_comment = comment_form.save(commit = False)
            # Привязываем комментарий к текущей статье.
            new_comment.post = post
            # Сохраняем комментарий в базе данных 
            new_comment.save()
        else:
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    return render(request,'blog/post/detail.html',{'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})


def post_share(request, post_id):
    # Получение статьи по идентификатору
    post = get_object_or_404(Post, id = post_id, status = 'published')
    sent = False
    if request.method == 'POST':
        # Форма была отправлена на соранение.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Все поля формы прошли валидацию.
            cd = form.cleaned_data
            # Отправка электронной почты
            post_url = request.build_absolute_url(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject,message,'admin@myblog.com',[cd['to']])
            sent = True
        else:
            form  = EmailPostForm()
            return render(request,'blog/post/share.html',{'post': post, 'form': form, 'sent': sent})