from rest_framework import serializers

from apps.tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source="author.username")
    list = serializers.ReadOnlyField(source="list.title")
    priority = serializers.CharField()
    title = serializers.CharField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "priority",
            "list",
            "title",
            "slug",
            "body",
            "done",
            "author_username",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "slug", "done"]

    def get_created_at(self, obj):
        now = obj.created_at
        formatted_date = now.strftime("%m.%d.%Y, %H:%M:%S")
        return formatted_date
