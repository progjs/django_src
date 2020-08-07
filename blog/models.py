from django.db import models
from django.utils import timezone
from django import forms

# Create your models here.

# Validator 함수 정의
# title 입력필드의 길이 체크 < 3
def min_length_3_validator(value):
    if len(value) < 3:
        raise forms.ValidationError('제목을 3글자 이상 입력해주세요!')

'''
CASCADE : 참조 된 객체가 삭제되면 참조가있는 객체도 삭제하십시오 
            (예를 들어 블로그 게시물을 제거하면 주석도 삭제할 수 있습니다). 
'''
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, validators=[min_length_3_validator]) # 유효성검사 함수
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    # field 추가
    # test = models.TextField()

    # 게시일자에 현재 날짜/시간을 대입해주는 함수
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    # 객체주소 대신 글제목을 반환해주는 toString() 함수
    ## /admin/ 에서 보면 post목록 이름에 title이 명시되어있다.
    def __str__(self):
        return self.title

# Post에 달리는 댓글
class Comment(models.Model):
    # post 정보
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100) # 댓글작성자
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False) # 댓글 승인여부

    def approve(self): # 댓글 승인여부 설정
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text