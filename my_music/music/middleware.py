from django.utils.deprecation import MiddlewareMixin


class NoCacheForAuthenticatedMiddleware(MiddlewareMixin):
    """
    Añade headers Cache-Control para evitar que el navegador cachee
    páginas de usuarios autenticados, así evitamos que al hacer "back"
    después de logout se muestre contenido antiguo.
    """
    def process_response(self, request, response):
        if request.user.is_authenticated:
            # Añade headers anti-cache para usuarios logneados
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response

