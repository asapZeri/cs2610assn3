from django.shortcuts import redirect
from .models import Session

class SessionMiddleware:
    EXEMPT_URIS = ['/', '/users/new/', '/sessions/new/' , '/createaccount/']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_token = request.COOKIES.get('session_token')
        if session_token:
            try:
                session = Session.objects.get(token=session_token)
                request.user = session.user
            except Session.DoesNotExist:
                request.user = None
        else:
            request.user = None
        if not request.user and request.path not in self.EXEMPT_URIS:
            return redirect('/sessions/new/') 
        response = self.get_response(request)
        return response

