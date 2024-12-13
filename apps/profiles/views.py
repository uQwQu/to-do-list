from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.profiles.models import Profile
from apps.profiles.serializers import AvatarUploadSerializer, ProfileSerializer

from .tasks import upload_avatar_to_cloudinary

User = get_user_model()


class ProfileDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self) -> Profile:
        return get_object_or_404(Profile, user=self.request.user)


@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def avatar_upload_api_view(request):
    profile = request.user.profile
    serializer = AvatarUploadSerializer(profile, data=request.data)

    if serializer.is_valid():
        image = serializer.validated_data["avatar"]

        image_content = image.read()

        upload_avatar_to_cloudinary.delay(str(profile.id), image_content)

        return Response(
            {"message": "Avatar upload started."}, status=status.HTTP_202_ACCEPTED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
