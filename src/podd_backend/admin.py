from collections.abc import Iterable

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.db.models import Q, QuerySet
from django.utils.translation import gettext_lazy as _
from spodcat.contrib.admin.mixin import AdminMixin, StaticRSSMixin
from spodcat.models import Podcast

from podd_backend.models import User


@admin.register(User)
class UserAdmin(AdminMixin, StaticRSSMixin[User], DjangoUserAdmin):  # type: ignore
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

    def get_podcast_slugs_from_instance(self, obj: User) -> Iterable[str]:
        return set(Podcast.objects.filter(Q(owner=obj) | Q(authors=obj)).values_list("slug", flat=True))

    def get_podcast_slugs_from_queryset(self, queryset: QuerySet[User]) -> Iterable[str]:
        return {slug for slugs in queryset.values_list("podcasts__slug", "owned_podcasts__slug") for slug in slugs}

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if not request.user.is_superuser:
            return ["is_superuser", "user_permissions", "groups", *fields]
        return fields

    def has_add_permission(self, request):
        return request.user.is_superuser
