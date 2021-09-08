from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import ArticlesType, Post, Stories, Work, ArticleTypeHeader, Comment

admin.site.register(ArticlesType)
admin.site.register(Stories)


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


@admin.register(ArticleTypeHeader)
class ArticleTypeHeaderAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'id')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'comments_number')

    def comments_number(self, obj):
        a = (o for o in obj.comments.filter(read=True))
        return '{0} + {1}'.format(len(list(a)), len(list(o for o in obj.comments.filter(read=False))))
    inlines = [
        CommentInline,
    ]


@admin.register(Work)
class WorksAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag_list', 'link')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)