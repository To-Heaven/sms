from django.conf import settings
from django.shortcuts import redirect


class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class LoginMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        userInfo =  request.session.get(settings.LOGINAUTH)
        if request.path_info == '/login/':
            return None
        if not userInfo:
            return redirect('/login/')

