from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.utils import translation
from django.utils.cache import patch_vary_headers

from podd_backend.models import User


class LocaleMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)

        if request.resolver_match and request.resolver_match.app_name == "admin":
            language = translation.get_language()
            patch_vary_headers(response, ("Accept-Language",))
            response.headers.setdefault("Content-Language", language)

        return response

    # pylint: disable=unused-argument
    def process_view(self, request: HttpRequest, *args, **kwargs):
        if request.resolver_match and request.resolver_match.app_name == "admin":
            if isinstance(request.user, User) and request.user.language:
                language = request.user.language
            else:
                language = translation.get_language_from_request(request, check_path=False)

            translation.activate(language)
