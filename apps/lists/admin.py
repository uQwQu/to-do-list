from django.contrib import admin

from apps.lists.models import List


class ListAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author"]
    list_filter = ["author"]
    readonly_fields = ("slug",)


admin.site.register(List, ListAdmin)
