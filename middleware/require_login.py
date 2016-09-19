from django.shortcuts import reverse
from django.http import HttpResponseRedirect
import re


class RequireLoginMiddleware(object):
    """
    Limits the pages a not logged in user can visit
    """
    
    def __init__(self, get_response):
        """
        Creates the middleware response handler, with the urls allowed to visit before login in
        """
        self.get_response = get_response
        self.allowed_urls = ["^/login(/error)?$", "^/auth$"]

    def __call__(self, request):
        """
        Redirects the user to the login page if it is not logged in or trying to access an allowed page
        """
        if not request.user.is_authenticated and not self.url_match(request.path):
            return HttpResponseRedirect(reverse("band_booking:login"))
        return self.get_response(request)

    def url_match(self, target_url):
        """
        Uses regex to check if the target_url matches any of the allowed_urls.
        """
        for url in self.allowed_urls:
            if re.match(url, target_url):
                return True
        return False
