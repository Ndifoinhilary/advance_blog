from django.contrib import admin
from blog import models
# Register your models here.


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title','slug','author','publish','status']
    list_firter = ['created','publish','status','author']
    search_fields = ['body','title','author']
    prepopulated_fields = {'slug':('title')}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status','publish']