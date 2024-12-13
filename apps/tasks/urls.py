from django.urls import path

from apps.tasks.views import (
    TaskDoneListAPIView,
    TaskListCreateAPIView,
    TaskStatusChangeAPIView,
    TaskUndoneListAPIView,
    TaskUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "<slug:list_slug>/<slug:task_slug>/status/",
        TaskStatusChangeAPIView.as_view(),
        name="task-status-change",
    ),
    path(
        "<slug:list_slug>/done/", TaskDoneListAPIView.as_view(), name="task-done-list"
    ),
    path(
        "<slug:list_slug>/undone/",
        TaskUndoneListAPIView.as_view(),
        name="task-undone-list",
    ),
    path("<slug:list_slug>/", TaskListCreateAPIView.as_view(), name="task-list-create"),
    path(
        "<slug:list_slug>/<slug:task_slug>/",
        TaskUpdateDestroyAPIView.as_view(),
        name="task-update-destroy",
    ),
]
