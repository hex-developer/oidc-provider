from oidc_provider.models import Client
from oidc_provider.lib.errors import ClientIdError
from django.shortcuts import redirect
from re import sub

class HostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        query_dict = (self.request.POST if self.request.method == 'POST'
                      else self.request.GET)
        
        host = query_dict.get('host', '')
        redirect_uri = query_dict.get('redirect_uri', '')
        client_id = query_dict.get('client_id', '')
        if (host and redirect_uri) and host != redirect_uri:
            try:
                client = Client.objects.get(client_id=client_id)
                for uri in client._redirect_uris.split("\n"):
                    if host in uri:
                        return redirect(sub(r"^http(s?):\/\/([^\/]+)(.+)", r"http\1://"+host, uri)+request.get_full_path())
            except Client.DoesNotExist:
                raise ClientIdError()
        response = self.get_response(request)
        return response