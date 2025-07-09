from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from spodcat.contrib.admin.mixin import AdminMixin

from podd_backend.models import User


@admin.register(User)
class UserAdmin(AdminMixin, DjangoUserAdmin): # type: ignore
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "language")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    save_on_top = True

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            return ["is_superuser", "user_permissions", "groups", *fields]
        return fields

    def has_add_permission(self, request):
        return request.user.is_superuser
