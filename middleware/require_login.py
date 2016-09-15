from django.shortcuts import reverse
from django.http import HttpResponseRedirect


class RequireLoginMiddleware(object):
    """
    Limits the pages a not logged in user can visit
    """
    
    def __init__(self, get_response):
        """
        Creates the middleware response handler, with the urls allowed to visit before login in
        """
        self.get_response = get_response
        self.allowed_urls = ["/login", "/auth"]

    def __call__(self, request):
        """
        Redirects the user to the login page if it is not logged in or trying to access an allowed page
        """
        if not request.user.is_authenticated and not request.path in self.allowed_urls:
            return HttpResponseRedirect(reverse("band_booking:login"))
        return self.get_response(request)

