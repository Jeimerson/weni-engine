from rest_framework import status, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import RecentActivitySerializer
from ..paginations import CustomCursorPagination
from connect.api.v1.internal.permissions import ModuleHasPermission
from connect.common.models import Project, RecentActivity

User = get_user_model()


class RecentActivityViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = RecentActivity.objects.all()
    serializer_class = RecentActivitySerializer
    permission_classes = [ModuleHasPermission]
    pagination_class = CustomCursorPagination

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request):
        project_uuid = request.query_params.get("project")
        try:
            project = Project.objects.get(uuid=project_uuid)
        except Project.DoesNotExist:
            return Response({"message": "Project does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if not project.project_authorizations.filter(user__email=request.user.email).exists():
            return Response({"message": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        recent_activities = RecentActivity.objects.filter(project__uuid=project_uuid).order_by("-created_on")
        data = [recent_activity.to_json for recent_activity in recent_activities]
        return Response(data, status=status.HTTP_200_OK)
