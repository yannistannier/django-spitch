from django.contrib import admin
from .models import Ask, Tag, Asktag


@admin.register(Ask)
class AskAdmin(admin.ModelAdmin):
    list_display = ("text", "is_private", "active")

 
@admin.register(Asktag)
class AsktagAdmin(admin.ModelAdmin):
    list_display = ("tag", "ask")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
