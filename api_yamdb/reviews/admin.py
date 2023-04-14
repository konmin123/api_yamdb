from django.contrib import admin

from .models import User, Title, Comment, Review


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'role'
    )
    list_editable = ('role',)
    list_filter = ('role',)
    search_fields = ('username',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'year',
        'description',
        'category',
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    filter_horizontal = ('genre',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'title',
        'text',
        'score',
        'pub_date',
    )
    search_fields = ('author', 'title', 'text',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'review',
        'text',
        'pub_date',
    )
    search_fields = ('author', 'text', 'pub_date',)
    list_filter = ('author',)


admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
