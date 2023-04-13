from django.contrib import admin

from api.models import User, Title


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


admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
