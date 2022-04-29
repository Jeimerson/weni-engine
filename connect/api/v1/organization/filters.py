from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import ugettext_lazy as _
from django_filters import rest_framework as filters
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied
from connect.api.v1 import READ_METHODS

from connect.common.models import (
    OrganizationAuthorization,
    Organization,
    RequestPermissionOrganization,
)


class OrganizationAuthorizationFilter(filters.FilterSet):
    class Meta:
        model = OrganizationAuthorization
        fields = ["organization"]

    organization = filters.CharFilter(
        field_name="organization",
        method="filter_organization_uuid",
        help_text=_("Organization's UUID"),
        required=True,
    )

    def filter_organization_uuid(self, queryset, name, value):
        request = self.request
        try:
            organization = Organization.objects.get(uuid=value)
            authorization = organization.get_user_authorization(request.user)
            if request.method in READ_METHODS:
                if not authorization.can_contribute:
                    raise PermissionDenied()
            else:
                if not authorization.is_admin:
                    raise PermissionDenied()
            return queryset.filter(organization=organization)
        except Organization.DoesNotExist:
            raise NotFound(_("Organization {} does not exist").format(value))
        except DjangoValidationError:
            raise NotFound(_("Invalid Organization UUID"))


class RequestPermissionOrganizationFilter(filters.FilterSet):
    class Meta:
        model = RequestPermissionOrganization
        fields = ["organization"]

    organization = filters.CharFilter(
        field_name="organization",
        method="filter_organization_uuid",
        help_text=_("Organization's UUID"),
        required=True,
    )

    def filter_organization_uuid(self, queryset, name, value):
        request = self.request
        try:
            organization = Organization.objects.get(uuid=value)
            authorization = organization.get_user_authorization(request.user)

            if not authorization.is_admin:
                raise PermissionDenied()
            return queryset.filter(organization=organization)
        except Organization.DoesNotExist:
            raise NotFound(_("Organization {} does not exist").format(value))
        except DjangoValidationError:
            raise NotFound(_("Invalid Organization UUID"))
