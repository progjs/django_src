from django.contrib import admin
from .models import Post, Comment

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    # admin page에서 Post 객체들의 title뿐 아니라 다른것들도 보여지게 한다.
    list_display = ['id', 'title', 'count_text']
    list_display_links = ['title']

    def count_text(self, obj):
        return '{}글자'.format(len(obj.text))

    count_text.short_description = '내용 글자수'


# 관리자 페이지에서 만든 모델을 보기위해 Post model을 등록
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
