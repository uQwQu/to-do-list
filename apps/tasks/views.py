import logging

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.lists.models import List
from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer
from apps.tasks.validators import check_task, is_owner

logger = logging.getLogger(__name__)


class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        list_slug = self.kwargs.get("list_slug")
        if is_owner(self, list_slug):
            return Task.objects.filter(list__slug=list_slug)

    def perform_create(self, serializer):
        list_slug = self.kwargs.get("list_slug")
        if is_owner(self, list_slug):
            serializer.save(
                author=self.request.user, list=get_object_or_404(List, slug=list_slug)
            )


class TaskUpdateDestroyAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> Task:
        return check_task(self)


class TaskStatusChangeAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["patch", "options"]

    def update(self, request, *args, **kwargs):
        instance = check_task(self)
        instance.done = not instance.done
        instance.save()
        return Response(
            {"message": f"Task status changed to {instance.done}!"},
            status=status.HTTP_200_OK,
        )


class TaskDoneListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        list_slug = self.kwargs.get("list_slug")
        if is_owner(self, list_slug):
            return Task.objects.filter(list__slug=list_slug, done=True)


class TaskUndoneListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        list_slug = self.kwargs.get("list_slug")
        if is_owner(self, list_slug):
            return Task.objects.filter(list__slug=list_slug, done=False)
