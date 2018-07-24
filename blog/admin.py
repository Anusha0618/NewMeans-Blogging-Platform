from django.contrib import admin

# Register your models here.
from blog.models import *
class BlogModelAdmin(admin.ModelAdmin):
     list_display = ["title","updated","timestamp"]
     list_display_links = ["updated"]
     list_editable = ["title"]
     list_filter = ["updated","timestamp"]
     search_fields = ["title","content"]
     class Meta:
        model = Blog
admin.site.register(Blog,BlogModelAdmin)
admin.site.register(Comment)
