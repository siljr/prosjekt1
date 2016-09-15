from django.shortcuts import reverse
from django.http import HttpResponseRedirect


class RequireLoginMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_urls = ["/login", "/auth"]

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path in self.allowed_urls:
            return HttpResponseRedirect(reverse("band_booking:login"))
        return self.get_response(request)

