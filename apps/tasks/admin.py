from django.contrib import admin

from apps.tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "id", "done", "author", "list"]
    list_filter = ["author", "list"]
    readonly_fields = ("slug",)


admin.site.register(Task, TaskAdmin)
