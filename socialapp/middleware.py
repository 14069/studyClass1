import os
import stat
from django.http import FileResponse, HttpResponseNotModified
from django.utils.http import http_date, parse_http_date_safe
from mimetypes import guess_type
from django.conf import settings

class MediaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path.startswith('/media/') and response.status_code == 404:
            file_path = os.path.join(settings.MEDIA_ROOT, request.path.lstrip('/media/'))

            if os.path.exists(file_path):
                last_modified = os.stat(file_path)[stat.ST_MTIME]
                if_modified_since = request.META.get('HTTP_IF_MODIFIED_SINCE')
                if if_modified_since:
                    if_modified_since = parse_http_date_safe(if_modified_since)
                    if if_modified_since is not None and int(last_modified) <= if_modified_since:
                        return HttpResponseNotModified()

                content_type, _ = guess_type(file_path)
                content_type = content_type or 'application/octet-stream'

                response = FileResponse(open(file_path, 'rb'), content_type=content_type)
                response['Last-Modified'] = http_date(last_modified)
                return response

        return response
