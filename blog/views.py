from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Post
from .forms import PostModelForm, PostForm

# Create your views here.
# Post 목록
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})
    # name = 'django'
    # return HttpResponse('''<h2>Post List</h2>
    #                     <p>웰컴 {name}!</p><p>{content}</p>'''.format(name=name, content=request.user))

# Post 상세조회
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# Post 등록
def post_new(request): # 주석은 modelform으로 한 경우 (주석아닌건 PostForms로)
    if request.method == 'POST':
        # form에 data를 입력한 후 save btn을 클릭했을때(등록 요청 시)
        form = PostForm(request.POST) # title, text field값이 저장된다.
        if form.is_valid(): # form data가 clean한 상태(유효할때)
            print(form.cleaned_data) #### 검증이 통과된 데이터
            post = Post.objects.create(author=User.objects.get(username=request.user.username),
                                       published_date=timezone.now(),
                                       title=form.cleaned_data['title'],
                                       text=form.cleaned_data['text'])
            # title, text 필드값이 저장된다.
            # post = form.save(commit=False) # form data는 저장하되, db에 저장은 안된 상태
            # post.author = User.objects.get(username=request.user.username) # admin login이 안되어있으면 에러발생
            # post.published_date = timezone.now()
            # post.save() # DB에 등록
            return redirect('post_detail', pk=post.pk) # 방금 작성한 post를 웹페이지로 보여준다.
    else: # 등록 form을 보여준다.
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form}) # else면 그 form에 계속 머물러있는다.

# Post 수정
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk) # DB에서 pk에 매칭되는 Post 객체를 가져온다.
    if request.method == 'POST':
        # 글 수정하는 부분
        form = PostModelForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        # 수정하기 전 데이터를 읽어온다.
        form = PostModelForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# Post 삭제
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')