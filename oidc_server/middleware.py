from oidc_provider.models import Client
from oidc_provider.lib.errors import ClientIdError
from django.shortcuts import redirect
import re

class HostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        query_dict = (request.POST if request.method == 'POST'
                      else request.GET)
        
        host = query_dict.get('host', '')
        redirect_uri = query_dict.get('redirect_uri', '')
        client_id = query_dict.get('client_id', '')
        print("Got request")
        try:
            redirect_uri_host = re.match(r"^http(s?):\/\/([^\/]+)", redirect_uri).group(2)
        except:
            redirect_uri_host = None
        if (host and redirect_uri) and host != redirect_uri_host:
            print(f"Host and redirect URI don't match {host} {redirect_uri_host}")
            try:
                client = Client.objects.get(client_id=client_id)
                print(f"Client found {client_id}")
                for uri in client._redirect_uris.split("\n"):
                    print(f"Checking URI {uri}")
                    if host in uri:
                        print(f"Host {host} is in {uri}")
                        redirect_to = re.sub(r"^http(s?):\/\/([^\/]+)(.+)", request.scheme+r"://\2", uri)+re.sub(r"^(.+)(redirect_uri=[^&]+)(.+)?$", r"\1redirect_uri="+uri+r"\3", request.get_full_path())
                        print(f"Redirecting to {redirect_to}")
                        return redirect(redirect_to)
            except Client.DoesNotExist:
                raise ClientIdError()
        response = self.get_response(request)
        return response