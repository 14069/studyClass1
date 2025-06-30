from django.http import HttpResponse, HttpResponseNotModified
from django.utils.http import http_date
import os
import stat
import time

class MediaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Verifica se é uma solicitação de mídia e se o arquivo existe
        if request.path.startswith('/media/') and response.status_code == 404:
            from django.conf import settings
            import os
            
            # Obtém o caminho completo do arquivo de mídia
            file_path = os.path.join(settings.MEDIA_ROOT, request.path.replace('/media/', '', 1))
            
            # Verifica se o arquivo existe
            if os.path.exists(file_path):
                # Lê o conteúdo do arquivo
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                # Define o tipo de conteúdo com base na extensão do arquivo
                from mimetypes import guess_type
                content_type, _ = guess_type(file_path)
                content_type = content_type or 'application/octet-stream'
                
                # Cria a resposta com o conteúdo do arquivo
                response = HttpResponse(content, content_type=content_type)
                
                # Define os cabeçalhos de cache
                response['Last-Modified'] = http_date(os.stat(file_path)[stat.ST_MTIME])
                response['Content-Length'] = os.path.getsize(file_path)
                
                return response
        
        return response
