from django.contrib import admin

from reviews.models import Comment, Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'author', 'title',
        'text', 'score', 'pub_date',
    )
    search_fields = ('author', 'title', 'text',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'review', 'text', 'pub_date',)
    search_fields = ('author', 'text', 'pub_date',)
    list_filter = ('author',)


admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
